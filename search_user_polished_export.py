# This script takes most functions from search_user_raw.py and displays the results in more structured form and exports by appending to CSV output_users.csv
import requests
import json
import csv
from search_user_raw import load_env_variables, get_user_input, create_search_payload

def make_post_request(search_payload, api_url, username, password):
    '''returns None, makes API request, prints response statuses, in case of success (2OO), prints the full response in cleaned form'''
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
        users_list = []
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
                    users_list.append((name, full_name, email))
        elif response.status_code == 400:
            print("Bad search request.")
            print(response.text)
        else:
            print("Search failed.")
            print(response.text)
        return users_list
    
    except Exception as e:
        print(f"Connection error occured while searching.")
        print(f"Error: {e}")
        return []

def write_users_to_csv(file_name, users_list):
    '''appends users to a CSV file, assuming users_list is a list of (name, full_name, email) tuples.'''
    with open(file_name, mode="a", encoding="utf-8", newline="") as output_file:
        fieldnames = ["name", "full_name", "email"]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        output_file.seek(0, 2)

        if output_file.tell() == 0:
            writer.writeheader()
        
        for name, full_name, email in users_list:
            writer.writerow({
                "name": name,
                "full_name": full_name,
                "email": email
            })


def main():
    api_url, username, password = load_env_variables()
    search_type, user_input = get_user_input()
    search_payload = create_search_payload(search_type, user_input)
    users_list = make_post_request(search_payload, api_url, username, password)
    write_users_to_csv("output_users.csv", users_list)

if __name__ == "__main__":
    main()
