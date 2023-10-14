# Arxiv Paper Notifier

Automate your daily Arxiv paper discovery! This Python script fetches the latest papers from Arxiv, filters them based on specific keywords and authors, and then sends a daily digest email to specified users.  

**This project is mainly developed by ChatGPT (GPT-4) under human supervision.**

## Features

- Fetch papers from multiple Arxiv categories/subjects.
- Filter papers based on a list of authors and/or keywords.
- Sends a daily email digest for matched papers.
- Stores a local collection of matched papers in JSON format.

## Setup

### 1. Prerequisites

- Python 3.x
- Required Python libraries: `beautifulsoup4`, `requests`.
- (Optional) Cloud service (the author uses `OCI free-tier`)

To install the libraries, use:

```bash
pip install beautifulsoup4 requests
```

### 2. Configuration

Rename the provided `config_sample.json` to `config.json`. This JSON file is used to specify user profiles and email sending credentials.

Sample configuration:

```json
{
  "sender_email": "your.assistant@example.com",
  "sender_password": "XXXX XXXX XXXX XXXX", // Gmail App password
  "users": [
    {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "arxiv_url": ["https://arxiv.org/list/cs.CV/pastweek?show=1000"],
      // use a url like this for your subject, a silly but simple method to make sure today's papers are collected
      "authors": ["Author Name 1", "Author Name 2"],
      "keywords": ["neural networks", "deep learning"]
    },
    ...  // Add more users as needed
  ],
}
```

- Configuration: The script uses a JSON configuration file (config.json). You can specify:
The sender's email and its app password for sending emails.
- A list of users (recipients), along with:
Their preferred Arxiv URLs/categories.
A list of interesting authors.
A list of keywords to filter the papers.
- Fetching and Filtering: For each user, the script will:
Fetch the latest papers from the specified Arxiv URLs.
Filter out the papers which are either authored by one of the interesting authors or contain one of the keywords in their title.
- Email Digest: The filtered papers are then emailed to the respective users as a daily digest.
- Local Collection: The matched papers are also saved locally in the paper_collections directory in JSON format.
- For sender_email, the author uses Gmail and its APP password. They worked quite well.

### 3. Running the Script
In your terminal or command prompt, navigate to the project directory and execute:
```bash
python main.py
```

### 4. Schedule a daily email-sending service
To automatically send emails at a particular time daily, you can use the ```cron``` scheduler in Unix-based systems.  
  
**Open the Crontab for Editing**  
```bash
crontab -e
```
  
**Add the following line**
```bash
0 8 * * * /path/to/your/python3 /path/to/your/script/main.py
```
Here's a breakdown of the cron timing format:  
```0``` stands for the ```minute``` (0th minute)  
```8``` stands for the ```hour``` (8th hour or 8 AM)  
The three ```*``` symbols mean every day of the month, every month, and every day of the week, respectively.  
Ensure you replace ```/usr/bin/python3``` with the path to your Python interpreter (you can get this by running which python3 command) and ```/path/to/your/script/main.py``` with the full path to your main.py script.  
  
**Important Notes**  
Ensure your script is executable:  
```bash
chmod +x /path/to/your/script/main.py
```
Scripts run by cron often don't recognize environment variables in the same way your interactive shell does. Always use full paths in your scripts and in your crontab to avoid issues.  
To keep a log of script outputs and errors, append the output to a log file:  
```bash
0 8 * * * /usr/bin/python3 /path/to/your/script/main.py >> /path/to/your/script/logname.log 2>&1  
```
