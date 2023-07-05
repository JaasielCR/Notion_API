import os
import json
import sys
import requests

# Notion Key and Headers
NOTION_API_KEY = 'secret_iVyHhWq151i1PR605FxY4xivJ2SbxSIl9sY6RroJD4h'
NOTION_HEADERS = {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer {}'.format(NOTION_API_KEY),
    'Content-Type': 'application/json', 
}

# ID'S A LOS QUE SE LES VA A ENVIAR LAS REQUESTS
page = '222c1e867f794b65b233ad1afa9409d9'
block = 'cb3cda449ead434dbd5eda08c8a6fc08'



# URL'S PARA ENVIAR REQUESTS
# Patch
append_block_children = 'https://api.notion.com/v1/blocks/{block_id}/children'
# Get
retrive_block = 'https://api.notion.com/v1/blocks/{block_id}'
retrive_block_children_url = 'https://api.notion.com/v1/blocks/{}/children'.format(page)
retrive_parent_id_url = 'https://api.notion.com/v1/parent_ids/{parent_id_id}'
retrive_database_url = 'https://api.notion.com/v1/databases/{database_id}'
#Post
create_parent_id_url = 'https://api.notion.com/v1/parent_ids'
query_database_url = 'https://api.notion.com/v1/databases/{database_id}/query'


# Search for the blocks on Tests.py Notion parent_id
response = requests.get(retrive_block_children_url, headers=NOTION_HEADERS)
response = response.json()
parent_block = response['results'][0]
results = []
for result in response["results"]:
    print(f'\n Hemos encontrado un bloque en la pagina')
    results.append(result)
print('\n The value of the retrived list RESULTS with {} blocks is: \n \n {} '.format(len(response['results']),results))
# print (' \nEl numero de bloques encontrados es: {} \n \n'.format(len(response['results'])))


#ADD THE NON CHILDREM CALLOUTS TO nonchildren_items
# print('\n El valor del diccionario RESPONSE es: \n \n {} '.format(response))
nonchildren_callouts = [result for result in response['results'] if result['has_children'] == False and result['type'] == 'callout']
print(len(nonchildren_callouts))
print('Estos son los bloques que no tienen children {}'.format(nonchildren_callouts))

def children(parent_block,children):
    retrive_block_children_url = 'https://api.notion.com/v1/blocks/{}/children'.format(parent_block)
    response = requests.get( retrive_block_children_url, headers=NOTION_HEADERS)
    response = response.json()
    children = []
    children = [child for child in response]
    return children 
    # While True:
    #     if result['type'] =='callout':
    #         break


#Print the Children items of the block before
i = 0
for result in results:
    has_children = results[i]['has_children']
    if has_children == True:
        parent_id= result['id']
        response = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(parent_id), headers=NOTION_HEADERS)
        print ('\n  Estos son los children encontrados en los bloques parent: \n \n', response)
        children_items = len(response['results'])
        print('\n El bloque parent tiene: {} bloques children \n ' .format(children_items))

        children_callouts = [item for item in response['results']]


        block_url = 'https://api.notion.com/v1/blocks/222c1e867f794b65b233ad1afa9409d9/children'
        test_resultspy = 'https://api.notion.com/v1/blocks/9715bacd086f471a9c7a5ed106c5d915/children'
        print("\n {}".format(result['type']))
        if result['type'] =='callout':
            callout_data = {
            "children":[{
                "type": "callout",
                "callout": result["callout"]
            }]}
            response = requests.patch(block_url, headers=NOTION_HEADERS, json=callout_data ) 
            response = response.json() 
        elif result['type'] == 'column_list':
            # for child in children_callouts:
            parent_id = response['results'][0]['id']
            print("\n {}".format(parent_id))
            response = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(parent_id), headers=NOTION_HEADERS)
            if response.status_code == 200:
                response = response.json()
                children_column = response['results']
                print('\n Found {} children blocks {}: '.format(len(children_column),children_column))
            else:
                print('Failed to retrive child blocks: {} {}'.format(response.status_code, response.text))
            # print(children_column)
            children(parent_id,)
            column_data=[]
            # for callout in children_callouts:
            column_data = [child for child in children_callouts if child['type']=='column']
            print("\n\n Los bloques del tipo column encontrados son: {} \n {}".format(len(column_data),column_data))
            columnlist_data = {
                'type':"column_list",
                'children':[]}
            column_data[0]['children']=children_column
            columnlist_data['children']=column_data[0]
            print('\n',column_data)
            print('\n',columnlist_data)
            # update_block = 'https://api.notion.com/v1/blocks/{}/children'.format(column_id)
            # response = requests.patch(update_block,headers=NOTION_HEADERS,json={column_data})        
            
            response = requests.patch(test_resultspy, headers=NOTION_HEADERS, json=columnlist_data) 
            response = response.json()
            print(response)
            column_id = response['results'][0]['id']
        elif result["type"] == 'quote':
            pass
        else:
            print('The retrived blocked is not either a type callout or column_list parent')
            print ('\n It is type {} \n '.format(result['type']))     
        parent_id = str(response['results'][0]['id']).replace('-','')
        for callout in children_callouts:
            if callout['type'] == 'bulleted_list_item':
                childrencallout_data = {
                    "children":[{
                        "type": callout['type'],
                        'bulleted_list_item':callout['bulleted_list_item']
                        # "callout": callout["callout"]
                    }]}
                childrenblock_url = 'https://api.notion.com/v1/blocks/{}/children'.format(parent_id)
                response = requests.patch(childrenblock_url, headers=NOTION_HEADERS, json=childrencallout_data)
            elif callout['type'] == 'paragraph':
                childrencallout_data = {
                    "children":[{
                        "type": callout['type'],
                        'paragraph':callout['paragraph']
                        # "callout": callout["callout"]
                    }]}
                childrenblock_url = 'https://api.notion.com/v1/blocks/{}/children'.format(parent_id)
                response = requests.patch(childrenblock_url, headers=NOTION_HEADERS, json=childrencallout_data)
            elif callout['type'] == 'column':
                pass
                # column_data['children'].append(child for child in children_callouts if child['type']=='column')
                # update_block = 'https://api.notion.com/v1/blocks/{}/children'.format(column_id)
                # response = requests.patch(update_block,headers=NOTION_HEADERS,json={})
    i = i + 1   



i = 0
while i<children_items:
    # print('\n \n Los callouts hijos son: {} \n'.format(children_callouts[i]))
    i= i+1

#ADD THE BLOCKS RETRIVED TO THE SELECTED parent_id



#ADD THE RETRIVED NON CHILDREM CALLOUTS TO THE SELECTED parent_id
for callout in nonchildren_callouts:
    callout_data = {
        "children":[{
            "type": 'callout',
            "callout": callout["callout"]
        }]}
    childrenblock_url = 'https://api.notion.com/v1/blocks/{}/children'.format(page)
    response = requests.patch(childrenblock_url, headers=NOTION_HEADERS, json=callout_data)


