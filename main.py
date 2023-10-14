import os
import json
from datetime import datetime
from collect_today import extract_arxiv_data, find_interesting_papers, extract_data_from_multiple_urls, save_papers_to_local
from send_email import load_papers_from_local, generate_html_from_papers, send_email

# Use a relative path, where to store your daily papers
base_path = "paper_collections"

# Ensure the directory exists, if not, create it
if not os.path.exists(base_path):
    os.makedirs(base_path)
    print("Making a new forder for paper collection ...")

def is_weekday():
    # 0 is Monday and 6 is Sunday
    today = datetime.today().weekday()
    return 0 <= today <= 4  # This will return True for Monday to Friday and False for Saturday and Sunday
    # return True  # test


def load_user_profiles(filename="config.json"):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config["users"]

def load_config(filename="config.json"):
    with open(filename, 'r') as f:
        return json.load(f)


def main():
    print(datetime.today().weekday())

    if is_weekday():

        config = load_config()
        users = config["users"]
        sender_email = config["sender_email"]
        sender_password = config["sender_password"]

        for user in users:
            print(f"Processing data for: {user['name']} ({user['email']})")            
            all_matched_papers_for_user = extract_data_from_multiple_urls(user["arxiv_url"], user["authors"], user["keywords"])

            if len(all_matched_papers_for_user) != 0:

                file_name = f"matched_papers_{user['name']}_{datetime.now().strftime('%Y-%m-%d')}.json"
                save_path = f"{base_path}/{file_name}"
                save_papers_to_local(all_matched_papers_for_user, save_path)

                html_body = generate_html_from_papers(all_matched_papers_for_user, user["authors"], user["keywords"])

                send_email(f"test 3 Today's arxiv selection for {user['name']}", html_body, user["email"], sender_email, sender_password)

                print(f"Email sent to {user['name']} ({user['email']}).\n")

            else:
                print("No matched paper")

    else:
        print("It's a weekend. Skipping Arxiv updates.")


if __name__ == "__main__":
    main()
