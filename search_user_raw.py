import os
from dotenv import load_dotenv
import requests
import json

def load_env_variables():
    load_dotenv()

    API_URL = os.getenv("API_URL")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")

    if not all([API_URL, USERNAME, PASSWORD]):
        raise EnvironmentError("Missing one or more required environment variables - API_URL, USERNAME or PASSWORD")

    return (API_URL, USERNAME, PASSWORD)


def get_user_input():
    while True:
        user_input = input("Please enter the user email or beginning letters of the user you are looking for: ").strip()
        if user_input != "":
            if "@" in user_input and "." in user_input:
                search_type = "email"
            else:
                search_type = "letters"
            break
    return (search_type, user_input)

def create_search_payload(search_type, user_input):
    if search_type == "email":
        search_payload = {
            "query": {
                "filter": {
                    "equal": {
                        "path": "emailAddress",
                        "value": user_input
                    }
                }
            }
        }
    
    else:
        search_string = f"name startsWith \"{user_input}\""
        search_payload = {
            "query": {
                "filter": {
                    "text": search_string
                }
            }
        }
    return search_payload

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
            print(response.text)
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

if __name__ == "__main__":
    main()
