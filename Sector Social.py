import os
import json
import sys
import requests

# Notion Key and Headers
notion_api_key = 'secret_iVyHhWq151i1PR605FxY4xivJ2SbxSIl9sY6RroJD4h'
notion_headers = {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer {}'.format(notion_api_key),
    'Content-Type': 'application/json', 
}


# Send a requests that retrives all the pages to search
database_id = 'cde1411dd6944e33a4e77ef0e4403bb4'
query_url = f'https://api.notion.com/v1/databases/{database_id}/query'
filter = {}

response = requests.post(query_url, json=filter, headers=notion_headers)
print(response.status_code)
response = response.json()

i=0
pages_id = []
for page in response:
    page_id = response['results'][i]['id']
    page_name = response ['results'][i]['properties']['Name']['title'][0]['text']['content']
    pages_id.append(page_id)
    i = i + 1
    print(f'\n La pagina  que encontramos es: {page_id} con nombre: {page_name}')


# Set up the Notion API endpoints and headers
notion_page_url = 'https://api.notion.com/v1/pages'

# Send the request to retrieve the callout blocks for each page
callouts=[]
for page in pages_id:
    notion_url = 'https://api.notion.com/v1/blocks/{}/children'.format(page)
    response = requests.get(notion_url, headers=notion_headers)
    print(f' \n The answer that Notion url sent is this: {response}')
    print('')

    # Parse the response and extract the callout blocks
    if response.status_code == 200:
        result = response.json()
        callouts_page = [block for block in result['results'] if block['type'] == 'callout']
        # print(callouts_page)
        # print(callouts)
        callouts.extend(callouts_page)
        # print(callouts)
        print(" \n************************************************************")
        print(' \n Retrieved {} callout blocks.'.format(len(callouts_page)))
    else:
        print('Failed to retrieve page: {} {}'.format(response.status_code, response.text))

print(' \n Retrieved {} callout blocks.'.format(len(callouts)))


# Create a new page called "Ejemplo"
new_page_data = {
    'parent': {
        'page_id': 'a6d62782a1324610a6647f056395fa44'
    },
    'properties': {
        'title': {
            "type":"title",
            "title": [
                {
                    'text': {
                        'content': 'Summary of Callouts '
                    }
                }
            ]
        }
    }
}


response = requests.post(notion_page_url, headers=notion_headers, json=new_page_data)

if response.status_code == 200:
    result = response.json()
    new_page_id = result['id']
    print('Created new page with ID: {}'.format(new_page_id))
else:
    print('Failed to create new page: {} {}'.format(response.status_code, response.text))

# Add the callout blocks to the new page
for callout in callouts:
    # block_data = {
    #     'object': 'block',
    #     'type': 'callout',
    #     'callout': callout['callout'],
    #     # 'color': callout['color']
    # }

    block_data = {
        "children":[{
            "type": "callout",
            "callout": callout["callout"]
        }]}
    block_url = 'https://api.notion.com/v1/blocks/{}/children'.format(new_page_id)
    response = requests.patch(block_url, headers=notion_headers, json=block_data)

    # print(response.json())
 
 
 
    if response.status_code == 200:
        print('Added callout block to new page.')
    else:
        print('Failed to add callout block: {} {}'.format(response.status_code, response.text))
        delete = {"archived":True}
        delete_url = "https://api.notion.com/v1/pages/{}".format(new_page_id)
        response = requests.patch(delete_url, headers=notion_headers, json=delete)
        print("La pagina con id: {} ha sido borrada con exito".format(new_page_id))
        