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
   

target_user = args.u
user_info = get_user_info(target_user)
user_events = get_user_events(target_user)

if user_info is not None:
    print(f"Username: {user_info['login']}")
    print(f"Email: {user_info['email']}")
    print(f"ID: {user_info['id']}")
    print(f"Company: {user_info['company']}")
    print("-------------- Stats --------------")
    print(f"Followers: {user_info['followers']} --- Public repos: {user_info['public_repos']} --- Creation date: {user_info['created_at']}")

if user_events is not None:
    print("---------- Recent events ----------")
    try:
        for event in user_events[:5]:
            print(f"{event['type']} at {event['created_at']} to repository {event['repo']['name']}")
            
            if event['type'] == "PushEvent":
                commits = event['payload'].get('commits')
                if commits:
                    print(f"  - Pushed {len(commits)} commits to {event['repo']['name']}")
                else:
                    print(f"  - Pushed to {event['repo']['name']}")
                    
            elif event['type'] == "CreateEvent":
                print(f"  - Created {event['payload']['ref_type']} {event['payload']['ref']} in {event['repo']['name']}")
            elif event['type'] == "DeleteEvent":
                print(f"  - Deleted {event['payload']['ref_type']} {event['payload']['ref']} in {event['repo']['name']}")
            elif event['type'] == "WatchEvent":
                print(f"  - Started watching {event['repo']['name']}")
            elif event['type'] == "ForkEvent":
                print(f"  - Forked {event['repo']['name']} to {event['payload']['forkee']['full_name']}")
            elif event['type'] == "IssuesEvent":
                print(f"  - {event['payload']['action']} issue #{event['payload']['issue']['number']} in {event['repo']['name']}")
            elif event['type'] == "IssueCommentEvent":
                print(f"  - {event['payload']['action']} comment on issue #{event['payload']['issue']['number']} in {event['repo']['name']}")
            elif event['type'] == "PullRequestEvent":
                print(f"  - {event['payload']['action']} pull request #{event['payload']['number']} in {event['repo']['name']}")
            elif event['type'] == "PullRequestReviewEvent":
                print(f"  - {event['payload']['action']} review on pull request #{event['payload']['pull_request']['number']} in {event['repo']['name']}")
            elif event['type'] == "PullRequestReviewCommentEvent":
                print(f"  - {event['payload']['action']} comment on pull request #{event['payload']['pull_request']['number']} in {event['repo']['name']}")
            elif event['type'] == "CommitCommentEvent":
                print(f"  - {event['payload']['action']} comment on commit {event['payload']['comment']['commit_id']} in {event['repo']['name']}")
            elif event['type'] == "GollumEvent":
                print(f"  - Updated wiki pages in {event['repo']['name']}")
            elif event['type'] == "MemberEvent":
                print(f"  - {event['payload']['action']} member {event['payload']['member']['login']} to {event['repo']['name']}")
            elif event['type'] == "PublicEvent":
                print(f"  - Made {event['repo']['name']} public")
            elif event['type'] == "ReleaseEvent":
                print(f"  - Published release {event['payload']['release']['tag_name']} in {event['repo']['name']}")
            else:
                print(f"  - Unknown event type {event['type']} in {event['repo']['name']}")
    
    except Exception as e:
        print(f"An error occurred while processing events: {e}")
            
print("-------------------------------------------------------------------------")
