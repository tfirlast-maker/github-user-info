import requests as req
import argparse
import sys

parser = argparse.ArgumentParser(description="Username")
parser.add_argument("-u")
args = parser.parse_args()

def get_user_info(username):
    url = "https://api.github.com/users"
    try:
        response = req.get(f"{url}/{username.lower()}", timeout=10)
    except:
        print("Coud not reach github servers")
        return None
        
    if response.status_code == 404:
        print("User not found")
        return None
    elif response.status_code == 200:
        response = response.json()
        if response == None:
            print("An error occurred while fetching user data")
            return None
        return response
    else:
        print("An error occurred while fetching user data")
        return None
    
def format_response(response):
    print(f"Username: {response["login"]}")
    print(f"Email: {response["email"]}")
    print(f"ID: {response["id"]}")
    print(f"Company: {response["company"]}")
    print("-------------- Stats --------------")
    print(f"Followers: {response["followers"]} --- Public repos: {response["public_repos"]} --- Creation date: {response["created_at"]}")
   
def get_user_events(username):
    url = "https://api.github.com/users"
    try:
        response = req.get(f"{url}/{username.lower()}/events", timeout=10)
    except:
        print("Coud not reach github servers")
        return None
        
    if response.status_code == 404:
        print("User not found")
        return None
    elif response.status_code == 200:
        response = response.json()
        if response == None:
            print("An error occurred while fetching user data")
            return None
        return response
    else:
        print("An error occurred while fetching user data")
        return None
   
if len(sys.argv) == 1:
    args = False
else:
    target_user = args.u
    args == True
    
while True:
    if args == False:
        target_user = input("What user is your target?: ")
    else:
        args = False
        
    if target_user.lower() == "exit":
        break
    
    user_info = get_user_info(target_user)
    user_events = get_user_events(target_user)

    if user_info is not None:
        format_response(user_info)
    if user_events is not None:
        print("---------- Recent events ----------")
        for event in user_events[:5]:
            print(f"{event['type']} at {event['created_at']} to repository {event['repo']['name']}")

    print("-------------------------------------------------------------------------")
    