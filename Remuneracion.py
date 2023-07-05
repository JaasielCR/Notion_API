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
database_id = '1e7fc1e73ae040bca3fade3114558405'
query_url = f'https://api.notion.com/v1/databases/{database_id}/query'
filter = {}

response = requests.post(query_url, json=filter, headers=notion_headers)
print(response.status_code)
response = response.json()

i=0
pages_id = []
for page in response:
    page_id = response['results'][i]['id']
    page_name = response ['results'][i]['properties']['Title']['title'][0]['text']['content']
    pages_id.append(page_id)
    i = i + 1
    print(f'\n La pagina  que encontramos es: {page_id} con nombre: {page_name}')


# Set up the Notion API endpoints and headers
notion_page_url = 'https://api.notion.com/v1/pages'


new_page_data = {
    'parent': {
        'page_id': '9f024c0a837a41d6a2d59f15eee74f2c'
    },
    'properties': {
        'title': {
            "type":"title",
            "title": [
                {
                    'text': {
                        'content': 'Summary of Callouts'
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


# Send the request to retrieve the callout blocks for each page
callouts=[]
nonchildren_callouts = []
i = 0
for page in pages_id:
    retrive_block_children_url = 'https://api.notion.com/v1/blocks/{}/children'.format(page)
    filter_properties = {
        'filter':{
            'property':'object',
            'type':'callout'
    }}
    response = requests.get(retrive_block_children_url, headers=notion_headers,)
    response = response.json()
    results = []
    for result in response["results"]:
        print(' Hemos encontrado un bloque en la pagina')
        results.append(result)
    print (' \nEl numero de bloques encontrados es: {} \n \n'.format(len(response['results'])))


    #ADD THE NON CHILDREM CALLOUTS TO nonchildren_items
    nonchildren_callout = [result for result in response['results'] if result['has_children'] == False and result['type'] == 'callout']
    nonchildren_callouts.append(nonchildren_callout)
    print('Estos son los bloques {} que no tienen children:\n {}'.format(len(nonchildren_callouts),nonchildren_callouts))

    #Print the Children items of the block before
    for result in results:
        if result['type']=='callout' and result['has_children'] == True:
            parent_id = result['id']
            response = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(parent_id), headers=notion_headers)
            response = response.json()
            print ('\n  Estos son los children encontrados en los bloques parent: \n \n', response)
            children_items = len(response['results'])
            print('\n El bloque parent tiene: {} bloques children \n ' .format(children_items))
            children_callouts = [result for result in response['results']]

            block_url = 'https://api.notion.com/v1/blocks/{}/children'.format(new_page_id)
            callout_data = {
            "children":[{
                "type": "callout",
                "callout": result["callout"]
            }]}
            response = requests.patch(block_url, headers=notion_headers, json=callout_data )   
            response = response.json()
            parent_id = str(response['results'][0]['id']).replace('-','')
            for callout in children_callouts:
                if callout['type'] == 'bulleted_list_item':
                    childrencallout_data = {
                        "children":[{
                            "type": callout['type'],
                            'bulleted_list_item':callout['bulleted_list_item']
                        }]}
                    childrenblock_url = 'https://api.notion.com/v1/blocks/{}/children'.format(parent_id)
                    response = requests.patch(childrenblock_url, headers=notion_headers, json=childrencallout_data)
                elif callout['type'] == 'paragraph':
                    childrencallout_data = {
                        "children":[{
                            "type": callout['type'],
                            'paragraph':callout['paragraph']
                        }]}
                    childrenblock_url = 'https://api.notion.com/v1/blocks/{}/children'.format(parent_id)
                    response = requests.patch(childrenblock_url, headers=notion_headers, json=childrencallout_data)


nonchildren_callouts = [callout for callout in nonchildren_callouts if callout]
for callout in nonchildren_callouts:
    callout_data = {
        "children":[{
            "type": 'callout',
            "callout": callout[0]["callout"]
        }]}
    childrenblock_url = 'https://api.notion.com/v1/blocks/{}/children'.format(new_page_id)
    response = requests.patch(childrenblock_url, headers=notion_headers, json=callout_data)        