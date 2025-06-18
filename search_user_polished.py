import requests
import json
from search_user_raw import load_env_variables, get_user_input, create_search_payload

def make_post_request(search_payload, api_url, username, password):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"    
    }
    
    try:
        response = requests.post(
            api_url,
            auth=(username, password),
            headers=headers,
            data=json.dumps(search_payload),
            timeout=15
        )

        if response.status_code == 200:
            print("Search successful.")
            result = response.json()
            users = result.get("object", {}).get("object", [])
            if not users:
                print("No users found.")
            else:
                for user in users:
                    name = user.get("name", "(no name)")
                    email = user.get("emailAddress", "(no email)")
                    full_name = user.get("fullName", "(no full name)")
                    print(f"- {full_name} ({name}) {email}")
        elif response.status_code == 400:
            print("Bad search request.")
            print(response.text)
        else:
            print("Search failed.")
            print(response.text)
    
    except Exception as e:
        print(f"Connection error occured while searching.")
        print(f"Error: {e}")    

def main():
    api_url, username, password = load_env_variables()
    search_type, user_input = get_user_input()
    search_payload = create_search_payload(search_type, user_input)
    make_post_request(search_payload, api_url, username, password)

main()
