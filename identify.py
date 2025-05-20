# Simple file to get IDs, run seperately
from sender import *

def print_groupme_members(access_token, group_id):
    """Print all GroupMe members with their IDs"""
    url = f"https://api.groupme.com/v3/groups/{group_id}?token={access_token}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            members = response.json()['response']['members']
            print("\nGroupMe Members:")
            print("-" * 40)
            for member in sorted(members, key=lambda x: x['nickname']):
                print(f"{member['nickname']}: {member['user_id']}")
            print("-" * 40)
            print(f"Total members: {len(members)}")
        else:
            print(f"Error fetching members: {response.status_code}")
    except Exception as e:
        print(f"API request failed: {str(e)}")

# Usage:
ACCESS_TOKEN = "vo8yW6ulaGBDGXgomcpeuRq7IaBeToN0zrpy0qRq"  # From dev.groupme.com
GROUP_ID = "97100255"          # From group URL
print_groupme_members(ACCESS_TOKEN, GROUP_ID)