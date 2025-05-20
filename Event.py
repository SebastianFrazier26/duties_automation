import pandas as pd
from datetime import date

class Event:
    def __init__(self):
        self.date = date.today().strftime("%m/%d")

class Tails(Event):
    def make_sheet(self):
        start = float(input("Start time (e.g. 5.0 for 5:00, 5.5 for 5:30)?\n"))
        end = float(input("End time?\n"))
        
        # Generate time slots
        time_slots = []
        current = start
        while current < end:
            next_time = current + 1 if current % 1 == 0 else current + 0.5
            start_str = f"{int(current)}:30" if current % 1 else f"{int(current)}:00"
            end_str = f"{int(next_time)}:30" if next_time % 1 else f"{int(next_time)}:00"
            time_slots.append(f"{start_str}-{end_str}")
            current = next_time
        
        # Create DataFrame with only balc position
        data = [["balc"] + [0]*len(time_slots), ["door"] + [0]*len(time_slots), ["batch"] + [0]*len(time_slots)]  # 0 for assignable slots
        columns = ["position"] + time_slots
        
        return pd.DataFrame(data, columns=columns).astype(
            dtype={col: 'object' for col in columns}  # Ensure consistent dtype
        )

class Semi(Event):
    def make_sheet(self):
        start = float(input("Start time (e.g. 5.0 for 5:00, 5.5 for 5:30)?\n"))
        end = float(input("End time?\n"))
        
        # Generate time slots
        time_slots = []
        current = start
        while current < end:
            next_time = current + 1 if current % 1 == 0 else current + 0.5
            start_str = f"{int(current)}:30" if current % 1 else f"{int(current)}:00"
            end_str = f"{int(next_time)}:30" if next_time % 1 else f"{int(next_time)}:00"
            time_slots.append(f"{start_str}-{end_str}")
            current = next_time
        
        # Create DataFrame with only balc position
        data = [["balc"] + [0]*len(time_slots), ["door"] + [0]*len(time_slots), ["bar_1"] + [0]*len(time_slots), ["bar_2"] + [0]*len(time_slots)]  # 0 for assignable slots
        columns = ["position"] + time_slots
        
        return pd.DataFrame(data, columns=columns).astype(
            dtype={col: 'object' for col in columns}  # Ensure consistent dtype
        )

class Other(Event):
    def make_sheet(self):
        start = float(input("Start time (e.g. 5.0 for 5:00, 5.5 for 5:30)?\n"))
        end = float(input("End time?\n"))
        
        # Generate time slots
        time_slots = []
        current = start
        while current < end:
            next_time = current + 1 if current % 1 == 0 else current + 0.5
            start_str = f"{int(current)}:30" if current % 1 else f"{int(current)}:00"
            end_str = f"{int(next_time)}:30" if next_time % 1 else f"{int(next_time)}:00"
            time_slots.append(f"{start_str}-{end_str}")
            current = next_time
        
        # Create DataFrame with only balc position
        data = [["balc"] + [0]*len(time_slots), ["door"] + [0]*len(time_slots)]  # 0 for assignable slots
        columns = ["position"] + time_slots
        
        return pd.DataFrame(data, columns=columns).astype(
            dtype={col: 'object' for col in columns}  # Ensure consistent dtype
        )

class Registered(Event):
    def make_sheet(self):
        columns = ["position", "11:00-12:00", "12:00-1:00"]

        if input("Do you need a backdoor (y/n)?\n") == "y":
            data = [
                ["balc", 0, 0],
                ["door_1", 0, 0],
                ["door_2", 0, 0],
                ["backdoor", 0, 0],
                ["stairs_1", 0, 0],
                ["stairs_2", 0, 0],
                ["bar_1", 0, 0],
                ["bar_2", 0, 0]
            ]
        else:
            data = [
                ["balc", 0, 0],
                ["door_1", 0, 0],
                ["door_2", 0, 0],
                ["stairs_1", 0, 0],
                ["stairs_2", 0, 0],
                ["bar_1", 0, 0],
                ["bar_2", 0, 0]
            ]
        return pd.DataFrame(data, columns=columns)

class Double(Event):
    def make_sheet(self):

        if input("Start early (y/n)?\n").lower().strip() == "n":

            columns = ["position", "10:00-11:00", "11:00-12:00", "12:00-1:00"]

            if input("Do you need a backdoor (y/n)?\n").lower().strip() == "y":
                data = [
                    ["balc", 0, 0, 0],
                    ["backdoor", 0, 0, 0],
                    ["door_1", "", 0, 0],
                    ["door_2", "", 0, 0],
                    ["stairs_1/batch", 0, 0, 0],
                    ["stairs_2", "", 0, 0],
                    ["bar_1", "", 0, 0],
                    ["bar_2", "", 0, 0]
                ]
            else:
                data = [
                    ["balc", 0, 0, 0],
                    ["door_1", 0, 0, 0],
                    ["door_2", "", 0, 0],
                    ["stairs_1/batch", 0, 0, 0],
                    ["stairs_2", "", 0, 0],
                    ["bar_1", "", 0, 0],
                    ["bar_2", "", 0, 0]
                ]
        else:
            columns = ["position", "9:30-10:15", "10:15-11:00", "11:00-12:00", "12:00-1:00"]

            if input("Do you need a backdoor (y/n)?\n").lower().strip() == "y":
                data = [
                    ["balc", 0, 0, 0, 0],
                    ["backdoor", "", "", 0, 0],
                    ["door_1", 0, 0, 0, 0],
                    ["door_2", "", "", 0, 0],
                    ["stairs_1/batch", 0, 0, 0, 0],
                    ["stairs_2", "", "", 0, 0],
                    ["bar_1", "", "", 0, 0],
                    ["bar_2", "", "", 0, 0]
                ]
            else:
                data = [
                    ["balc", 0, 0, 0, 0],
                    ["door_1", 0, 0, 0, 0],
                    ["door_2", "", "", 0, 0],
                    ["stairs_1/batch", 0, 0, 0, 0],
                    ["stairs_2", "", "", 0, 0],
                    ["bar_1", "", "", 0, 0],
                    ["bar_2", "", "", 0, 0]
                ]
        return pd.DataFrame(data, columns=columns)
    
class Setup(Event):
    def make_sheet(self):
        start = float(input("Start time (e.g. 5.0 for 5:00, 5.5 for 5:30)?\n"))
        end = float(input("End time?\n"))
        num_needed = int(input("Number of setup crew needed?\n"))
        
        # Generate time slots
        time_slots = []
        current = start
        while current < end:
            next_time = current + 1 if current % 1 == 0 else current + 0.5
            start_str = f"{int(current)}:30" if current % 1 else f"{int(current)}:00"
            end_str = f"{int(next_time)}:30" if next_time % 1 else f"{int(next_time)}:00"
            time_slots.append(f"{start_str}-{end_str}")
            current = next_time
        
        # Create DataFrame with numbered setup positions
        data = [
            [f"setup_{i+1}"] + [0]*len(time_slots)  # 0 for assignable slots
            for i in range(num_needed)
        ]
        columns = ["position"] + time_slots
        
        return pd.DataFrame(data, columns=columns).astype(
            dtype={col: 'object' for col in columns}  # Ensure consistent dtype
        )

class RushEvent(Event):
    def make_sheet(self):
        start = float(input("Start time (e.g. 5.0 for 5:00, 5.5 for 5:30)?\n"))
        end = float(input("End time?\n"))
        
        # Generate time slots
        time_slots = []
        current = start
        while current < end:
            next_time = current + 1 if current % 1 == 0 else current + 0.5
            start_str = f"{int(current)}:30" if current % 1 else f"{int(current)}:00"
            end_str = f"{int(next_time)}:30" if next_time % 1 else f"{int(next_time)}:00"
            time_slots.append(f"{start_str}-{end_str}")
            current = next_time
        
        # Create DataFrame with only balc position
        data = [["balc"] + [0]*len(time_slots)]  # 0 for assignable slots
        columns = ["position"] + time_slots
        
        return pd.DataFrame(data, columns=columns).astype(
            dtype={col: 'object' for col in columns}  # Ensure consistent dtype
        )

class Greenkey(Event):
    def make_sheet(self):
        columns = ["position", "4:00-5:00", "5:00-6:00"]
        data = [
            ["balc", 0, 0],
            ["front_door_1", 0, 0],
            ["front_door_2", 0, 0],
            ["porch_1", 0, 0],
            ["porch_2", 0, 0],
            ["balc_1", 0, 0],
            ["balc_2", 0, 0],  # Fixed missing comma
            ["stairs", 0, 0]
        ]
        return pd.DataFrame(data, columns=columns)
    
class Weird(Event):
    def make_sheet(self):
        columns = ["position", "9:00-9:45", "9:45-10:45", "10:45-11:45", "11:45-12:30"]
        data = [
            ["balc", 0, 0, 0, 0],
            ["door_1", 0, 0, 0, 0],
            ["door_2", "", "", 0, 0],
            ["bar_1", "Ahron", "Ahron", 0, 0],
            ["bar_2", "Sharpe", "Duffield", 0, 0],
            ["bar_3", "", "", "Zuo", "Zuo"],
            ["bar_4", "", "", "Nikhil", "Nikhil"],
            ["stairs_1/batch", 0, 0, 0, 0],
            ["stairs_2", "", "", 0, 0],
            ["backstairs", "", "", 0, 0]
        ]
        return pd.DataFrame(data, columns=columns)