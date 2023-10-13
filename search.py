from datetime import datetime, timedelta
import json
import requests
import os

def search(query):
    # Calculate the date 6 months ago from today
    six_months_ago = datetime.now() - timedelta(days=36*30)  # approximating 3 years
    date_str = six_months_ago.strftime('%Y-%m-%d')

    # Append the date filter to the query
    query = f"{query} after:{date_str}"

    url = "https://google.serper.dev/search"

    # Get the API key from an environment variable
    api_key = os.environ.get('GOOGLE_SERPER_API_KEY')

    if not api_key:
        raise ValueError("Environment variable 'GOOGLE_SERPER_API_KEY' not set!")

    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

# for result in search('Bill Gates')['organic']:
#     title = result['title']
#     link = result['link']
#     snippet = result['snippet']

#     print(f"Tit: {title}")
#     print(f"Link: {link}")
#     print(f"Snippet: {snippet}\n")