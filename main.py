import random
import pandas as pd
import os
from datetime import datetime
from Event import *
from PIL import Image, ImageDraw, ImageFont  # Requires: pip install pillow
from sender import *

# Ensure sheets directory exists
os.makedirs("sheets", exist_ok=True)

master = pd.read_csv("duties_id.csv")

def create_sheet_image(sheet, event_type):
    """Create a PNG image of the duty sheet with dynamic sizing"""
    # Calculate dimensions
    font_size = 24
    padding = 20
    line_height = 40
    col_width = 200  # Fixed width for position column
    time_col_width = 150  # Width for time slot columns
    
    # Calculate image width (add all columns)
    img_width = col_width + (len(sheet.columns[1:]) * time_col_width) + (padding * 2)
    
    # Calculate image height (add all rows + header + title)
    img_height = ((len(sheet) + 1) * line_height) + (padding * 3) + 30  # +30 for title
    
    # Create image
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Load fonts (fallback to default if needed)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        bold_font = ImageFont.truetype("arialbd.ttf", font_size)
    except:
        font = ImageFont.load_default()
        bold_font = ImageFont.load_default()
    
    # Draw title
    title = f"{event_type.upper()} DUTY SHEET - {datetime.now().strftime('%m/%d/%Y')}"
    title_width = draw.textlength(title, font=bold_font)
    draw.text(((img_width - title_width) // 2, padding), title, fill=(0, 0, 0), font=bold_font)
    
    # Draw header
    y_offset = padding * 2 + 30  # Start below title
    x_offset = padding
    
    # Position column
    draw.rectangle([x_offset, y_offset, x_offset + col_width, y_offset + line_height], 
                  outline=(0, 0, 0), fill=(220, 220, 220))
    draw.text((x_offset + 10, y_offset + 10), "Position", fill=(0, 0, 0), font=bold_font)
    
    # Time slot columns
    x_offset += col_width
    for col in sheet.columns[1:]:
        draw.rectangle([x_offset, y_offset, x_offset + time_col_width, y_offset + line_height], 
                      outline=(0, 0, 0), fill=(220, 220, 220))
        draw.text((x_offset + 10, y_offset + 10), str(col), fill=(0, 0, 0), font=bold_font)
        x_offset += time_col_width
    
    # Draw rows
    y_offset += line_height
    for _, row in sheet.iterrows():
        x_offset = padding
        
        # Position cell
        draw.rectangle([x_offset, y_offset, x_offset + col_width, y_offset + line_height], 
                      outline=(0, 0, 0))
        draw.text((x_offset + 10, y_offset + 10), str(row['position']), fill=(0, 0, 0), font=font)
        
        # Time slot cells
        x_offset += col_width
        for col in sheet.columns[1:]:
            val = str(row[col]) if pd.notna(row[col]) and str(row[col]) not in ["0", ""] else "—"
            draw.rectangle([x_offset, y_offset, x_offset + time_col_width, y_offset + line_height], 
                          outline=(0, 0, 0))
            draw.text((x_offset + 10, y_offset + 10), val, fill=(0, 0, 0), font=font)
            x_offset += time_col_width
        
        y_offset += line_height
    
    # Save image
    filename = f"sheets/{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(filename)
    return filename

def print_mentioned_names(sheet):
    """Print all assigned names in @mention format with full names"""
    names = set()
    for col in sheet.columns[1:]:
        for name in sheet[col].unique():
            if pd.notna(name) and str(name) not in ["0", "", "—"]:
                names.add(name)  # Use full name
    
    if names:
        print("\nDuties for today:")
        print(" ".join(sorted([f"@{name}" for name in names])))
    else:
        print("\nNo members assigned to notify.")

def print_pretty_sheet(sheet):
    """Print the duty sheet to console"""
    # Create display version
    display_df = sheet.copy()
    for col in display_df.columns[1:]:
        display_df[col] = display_df[col].replace(["0", 0, ""], "—").fillna("—")
    
    # Print with borders
    print("\n" + "=" * 80)
    print("DUTY ASSIGNMENTS".center(80))
    print("=" * 80)
    print(display_df.to_string(index=False, justify='center'))
    print("=" * 80)

def main():
    global sheet
    event_type = input("What type of event do you need?\n").lower().strip()
    valid_events = ["tails", "registered", "double", "setup", "rush", "greenkey", "semi", "other", "weird"]
    if event_type not in valid_events:
        raise TypeError(f"Input must be one of: {', '.join(valid_events)}")

    # Initialize event sheet
    if event_type == "tails":
        sheet = Tails().make_sheet()
    elif event_type == "registered":
        sheet = Registered().make_sheet()
    elif event_type == "double":
        sheet = Double().make_sheet()
    elif event_type == "setup":
        sheet = Setup().make_sheet()
    elif event_type == "rush":
        sheet = RushEvent().make_sheet()
    elif event_type == "greenkey":
        sheet = Greenkey().make_sheet()
    elif event_type == "semi":
        sheet = Semi().make_sheet()
    elif event_type == "other":
        sheet = Other().make_sheet()
    elif event_type == "weird":
        sheet = Weird().make_sheet()

    # Process sheet
    sheet = sheet.replace({0: "0", "": "—"}).fillna("—")
    for col in sheet.columns[1:]:
        sheet[col] = sheet[col].astype(str)

    df = clean(master)

    # Handle assignments
    if any(pos.startswith('bar_') for pos in sheet['position']):
        assign_bar(df)
    assign_positions(df)

    # Save and output
    master.to_csv('duties_id.csv', index=False)
    
    # Create and save image
    image_path = create_sheet_image(sheet, event_type)
    print(f"\nDuty sheet saved to: {image_path}")
    
    # Print console output
    print_pretty_sheet(sheet)
    
    # ===== NEW GROUPME MENTION CODE STARTS HERE =====
    # Get list of assigned members
    names = {str(name) for col in sheet.columns[1:] 
             for name in sheet[col].unique() 
             if pd.notna(name) and str(name) not in ["0", "", "—"]}
    
    # Only proceed if there are assignments
    if names and input("\nSend to GroupMe? (y/n): ").lower() == 'y':
        if not validate_groupme_ids():
            if input("Continue anyway? (y/n): ").lower() != 'y':
                return
        try:
            # Upload image
            image_url = upload_image_to_groupme(image_path)
            
            # Create mention text and data (uses fixed function from sender.py)
            mention_text, mentions = create_groupme_mention_text(names)
            message_text = (f"{event_type.upper()} Duty Assignments\n\n"
                          f"Members to notify: {mention_text}")
            
            # Send message with mentions
            if send_groupme_message(message_text, mentions, image_url):
                print("✅ Successfully sent to GroupMe with active @mentions!")
            else:
                print("❌ Failed to send to GroupMe")
        
        except Exception as e:
            print(f"⚠️ Error sending to GroupMe: {str(e)}")

def clean(dataframe):
    df = dataframe.copy()
    df = df[df["is_exempt"] != 1]
    df = df[df["is_on"] == 1]
    df = df[df["year"] != 3]
    return df.reset_index(drop=True)

def assign_bar(df):
    tips_df = df[df["is_tips"] == 1].copy()
    tips_df['num_duties'] = pd.to_numeric(tips_df['num_duties'], errors='coerce').fillna(0).astype(int)

    # Sort by num_duties and shuffle ties
    tips_df = shuffle_ties(
        tips_df.sort_values('num_duties', ascending=True),
        ['num_duties']
    )

    bar_positions = [pos for pos in sheet['position'] if pos.startswith('bar_')]
    assigned_counts = {}     # (person, position) → # slots assigned in that row
    assigned_people = set()  # prevent reuse across bar rows

    for position in bar_positions:
        for col in sheet.columns[1:]:
            current_value = sheet.loc[sheet['position'] == position, col].values[0]
            if current_value != "0":
                continue  # already filled

            for _, member in tips_df.iterrows():
                person = member['name']
                if person in assigned_people and (person, position) not in assigned_counts:
                    continue  # already assigned to a different bar row

                current_double = int(master.loc[master['name'] == person, 'is_double'].values[0])
                assigned_in_row = assigned_counts.get((person, position), 0)

                max_slots = 1 + current_double
                if assigned_in_row >= max_slots:
                    continue

                # Assign this slot
                sheet.loc[sheet['position'] == position, col] = person

                # Bookkeeping
                if assigned_in_row == 0:
                    master.loc[master['name'] == person, 'num_duties'] += 1
                    assigned_people.add(person)
                if assigned_in_row >= 1:
                    master.loc[master['name'] == person, 'is_double'] = max(0, current_double - 1)

                assigned_counts[(person, position)] = assigned_in_row + 1
                break  # go to next slot

def assign_positions(df):
    regular_df = df[df["is_tips"] != 1].copy()
    regular_df['num_duties'] = pd.to_numeric(regular_df['num_duties'], errors='coerce').fillna(0).astype(int)

    regular_df = shuffle_ties(
        regular_df.sort_values('num_duties', ascending=True),
        ['num_duties']
    )

    assigned_counts = {}     # (person, position) → # of times assigned in that row
    assigned_people = set()  # person → has been used in any row

    for idx, row in sheet.iterrows():
        position = row['position']
        if position.startswith('bar_'):
            continue

        for col in sheet.columns[1:]:
            if sheet.at[idx, col] != "0":
                continue

            for _, member in regular_df.iterrows():
                person = member['name']
                if person in assigned_people and (person, position) not in assigned_counts:
                    continue  # already assigned to a different row

                current_double = int(master.loc[master['name'] == person, 'is_double'].values[0])
                assigned_in_row = assigned_counts.get((person, position), 0)

                max_slots = 1 + current_double
                if assigned_in_row >= max_slots:
                    continue

                # Assign this slot
                sheet.at[idx, col] = person

                # Bookkeeping
                if assigned_in_row == 0:
                    master.loc[master['name'] == person, 'num_duties'] += 1
                    assigned_people.add(person)
                if assigned_in_row >= 1:
                    master.loc[master['name'] == person, 'is_double'] = max(0, current_double - 1)

                assigned_counts[(person, position)] = assigned_in_row + 1
                break  # go to next slot

def shuffle_ties(df, sort_columns):
    if len(df) == 0:
        return df

    df['_group'] = df[sort_columns].apply(tuple, axis=1)
    groups = []
    for _, group in df.groupby('_group'):
        if len(group) > 1:
            group = group.sample(frac=1)
        groups.append(group)

    return pd.concat(groups).drop(columns=['_group']).reset_index(drop=True)

if __name__ == "__main__":
    main()