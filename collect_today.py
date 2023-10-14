from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

def get_formatted_today():
    # '%a' gets the abbreviated weekday, '%d' gets the day of the month, and '%b' gets the abbreviated month name
    return datetime.now().strftime('%a, %d %b %Y')

def extract_arxiv_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Dictionary to store the data
    papers_by_date = {}

    current_date = None
    today_str = get_formatted_today()
    # today_str = 'Thu, 12 Oct 2023' # test

    # Check if today's date exists in the fetched arXiv data (weekends?)
    if not soup.find('h3', text=today_str):
        print(f"No updates on arXiv for {today_str}")
        return {}

    for item in soup.find_all(['h3', 'dt', 'dd']):
        if item.name == 'h3':
            # Extract the date and use it as the current key
            current_date = item.text.strip()
            papers_by_date[current_date] = []
        elif item.name == 'dt':
            # Extract the identifier from the link
            identifier = item.find('a', href=True)['href']
        elif item.name == 'dd':
            title = item.select_one('.list-title.mathjax').text.replace('Title:', '').strip()
            authors = [a.text for a in item.select('.list-authors a')]
            papers_by_date[current_date].append({
                'title': title,
                'authors': authors,
                'identifier': identifier
            })
    return papers_by_date


def find_interesting_papers(papers, interesting_authors, interesting_keywords):
    matched_papers = []

    # Convert keywords to lowercase for case-insensitive search
    interesting_keywords = [keyword.lower() for keyword in interesting_keywords]
    interesting_authors = [author.lower() for author in interesting_authors]

    for paper in papers:
        # Check if any author from the interesting_authors list is an author of the paper
        if any(author in [a.lower() for a in paper['authors']] for author in [ia.lower() for ia in interesting_authors]):
            matched_papers.append(paper)
            continue  # Skip to the next iteration if a match is found

        # Check if any keyword from the interesting_keywords list is in the title of the paper
        if any(keyword in paper['title'].lower() for keyword in interesting_keywords):
            matched_papers.append(paper)

    return matched_papers

def remove_duplicates(papers):
    seen = set()
    unique_papers = []

    for paper in papers:
        if paper['identifier'] not in seen:
            seen.add(paper['identifier'])
            unique_papers.append(paper)

    return unique_papers


def extract_data_from_multiple_urls(urls, interesting_authors, interesting_keywords):
    all_matched_papers = []
    
    for url in urls:
        papers_from_url = extract_arxiv_data(url)
        todays_papers = papers_from_url.get(get_formatted_today(), [])
        # todays_papers = papers_from_url.get('Thu, 12 Oct 2023', []) # test
        matched_papers = find_interesting_papers(todays_papers, interesting_authors, interesting_keywords)
        all_matched_papers.extend(matched_papers)

    unique_matched_papers = remove_duplicates(all_matched_papers)
    
    return unique_matched_papers


# Modify the save_papers_to_local function to accept filename as parameter
def save_papers_to_local(matched_papers, filename):
    with open(filename, 'w') as file:
        json.dump(matched_papers, file)

    print(f'Successful: Matched papers saved to {filename}.')
