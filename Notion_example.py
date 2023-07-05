import os
import requests
import json

#NOTION_KEY = os.environ.get("secret_iVyHhWq151i1PR605FxY4xivJ2SbxSIl9sY6RroJD4h")
headers = {"Authorization": "Bearer secret_iVyHhWq151i1PR605FxY4xivJ2SbxSIl9sY6RroJD4h",
          "Content-Type": "application/json",
          "Notion-Version": "2022-06-28"}


search_params = {"filter":{"value":"database","property": "object", }}
search_response = requests.post(f'https://api.notion.com/v1/search',json=search_params, headers=headers)

print (search_response.json())

search_results = search_response.json()["results"]
page_id = search_results[0]["id"]

create_blank_page_body = {"parent":{"page_id":page_id}, "properties":{}}
create_blank_page_response = requests.post ("https://api.notion.com/v1/pages", json=create_blank_page_body, headers=headers)