# Use this file to automatically send our POST to groupme
import requests
from io import BytesIO
import pandas as pd
import os

# Credentials are mine, please fill in your own if using this service
GROUPME_ACCESS_TOKEN = "vo8yW6ulaGBDGXgomcpeuRq7IaBeToN0zrpy0qRq"
GROUPME_GROUP_ID = "102404136"
GROUPME_BOT_ID = "9cff3a23d5ae55944ce611280f"
'''
# Testing Creds
GROUPME_GROUP_ID = "106848271"
GROUPME_BOT_ID = "4d24511ed81ac659977ca2c257"
'''
GROUPME_API_URL = "https://api.groupme.com/v3/bots/post"

# Read groupme IDs
master = pd.read_csv("duties_id.csv")

def upload_image_to_groupme(image_path):
    """Upload image to GroupMe's image service"""
    with open(image_path, 'rb') as img_file:
        files = {'file': (os.path.basename(image_path), img_file.read())}
        headers = {'X-Access-Token': GROUPME_ACCESS_TOKEN}  # Get from GroupMe developer portal
        response = requests.post('https://image.groupme.com/pictures', 
                               files=files, 
                               headers=headers)
        return response.json().get('payload', {}).get('picture_url')

def send_groupme_message(text_message, mentions=None, image_url=None):
    """Send message with proper @mentions"""
    payload = {
        'bot_id': GROUPME_BOT_ID,
        'text': text_message,
        'attachments': []
    }
    
    if mentions:
        payload['attachments'].extend(mentions)
    
    if image_url:
        payload['attachments'].append({
            'type': 'image',
            'url': image_url
        })
    
    response = requests.post(GROUPME_API_URL, json=payload)
    return response.status_code == 202

def get_current_members():
    """Fetch current group members with their user_ids and nicknames"""
    url = f"https://api.groupme.com/v3/groups/{GROUPME_GROUP_ID}?token={GROUPME_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('response', {}).get('members', [])
    return []

def create_groupme_mention_text(names):
    """Generate mentions using user_ids (immune to nickname changes)"""
    current_members = get_current_members()
    master_list = pd.read_csv("duties_id.csv")
    mentions = []
    text = ""
    
    for name in sorted(names):
        # Find user_id from CSV (must exist)
        try:
            user_id = str(master_list[master_list['name'].str.lower() == name.lower()]['groupme_id'].values[0])
        except IndexError:
            print(f"⚠️ No GroupMe ID found for: {name}")
            text += f"@{name} "  # Fallback to plain text
            continue
        
        # Verify user is still in group (even if nickname changed)
        if any(str(m['user_id']) == user_id for m in current_members):
            mention_tag = f"@{name}"
            mentions.append({
                "type": "mentions",
                "user_ids": [user_id],
                "loci": [[len(text), len(mention_tag)]]
            })
            text += mention_tag + " "
        else:
            print(f"⚠️ {name} (ID: {user_id}) not in group - mention won't work")
            text += f"@{name} "  # Fallback
    
    return text.strip(), mentions

def validate_groupme_ids():
    """Check for missing/invalid GroupMe IDs before sending"""
    missing_ids = []
    for _, row in master.iterrows():
        if pd.isna(row.get('groupme_id')) or str(row['groupme_id']).strip() == "":
            missing_ids.append(row['name'])
    
    if missing_ids:
        print("\n⚠️ Missing GroupMe IDs for:")
        for name in missing_ids:
            print(f"- {name}")
        return False
    return True