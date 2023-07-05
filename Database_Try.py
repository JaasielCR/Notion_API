import os
import json
import requests

# Replace with your Notion API key
notion_api_key = 'secret_iVyHhWq151i1PR605FxY4xivJ2SbxSIl9sY6RroJD4h'

# Replace with the database ID of the selected database
database_id = '8dd37de80df9472cbeb109fe02d5286d'

# Set up the Notion API endpoint and headers
notion_url = 'https://api.notion.com/v1/databases/{}/query'.format(database_id)
notion_headers = {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer {}'.format(notion_api_key),
    'Content-Type': 'application/json',
}

# Set up the filter to retrieve only the callouts
filter_params = {
    'property': "database", "value":"object" 
    
}

# Set up the query parameters
query_params = {
    'filter': filter_params
}

# Send the request to the Notion API
response = requests.post(notion_url, headers=notion_headers, json=query_params)
print(response)

# Parse the response
if response.status_code == 200:
    results = response.json()['results']
    print('Retrieved {} callouts from the database.'.format(len(results)))
else:
    print('Failed to retrieve callouts: {} {}'.format(response.status_code, response.text))
