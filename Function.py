# from . import Tests
import requests
import json

# Constants
NOTION_API_KEY = 'secret_iVyHhWq151i1PR605FxY4xivJ2SbxSIl9sY6RroJD4h'
NOTION_HEADERS = {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer {}'.format(NOTION_API_KEY),
    'Content-Type': 'application/json', 
}
page = '222c1e867f794b65b233ad1afa9409d9'
block_url = 'https://api.notion.com/v1/blocks/222c1e867f794b65b233ad1afa9409d9/children'
retrive_block_children_url = 'https://api.notion.com/v1/blocks/{}/children'.format(page)

def children(parent_id,has_children):
    # has_children = response['results'][has_children]['has_children']
    while has_children == True:
        response = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(parent_id), headers=NOTION_HEADERS)
        if response.status_code == 200:          
            response = response.json()
            # print(response)
            childrens = [child for child in response['results']]
            print('\n Found {} children blocks: {} \n\n on the first level parent id {} \n\n'.format(len(childrens),childrens,parent_id))
            if len(childrens)<=0:
                break
            elif len(childrens)>0:
                childrens_id = [result['id'] for result in childrens]
                print(' \n Childrens_id found {} : {}  on the second level block id \n'.format(len(childrens_id),childrens_id))
                i=0
                print('\n\n Este es el valor de la variable RESPONSE: {}\n\n'.format(response))
                for ida in childrens_id:
                    has_children_child = childrens[i]['has_children']
                    print('\n\n {} on the value of the block id: {} \n\n'.format(has_children,childrens[i]['id']))
                    children_child(ida,has_children_child)
                    print('\n\n FUNCTION CHILDREN_CHILD HAS BEEN LOOP ONCE \n\n')
                    i =  1+i
            print('\n\n Este es el valor de la variable RESPONSE: {}\n\n'.format(response))
            has_children = response['results'][0]['has_children']
        else:
            print('Failed to retrive child blocks: {} {}'.format(response.status_code, response.text))
    if has_children == False:
        print('There are no childs on {}'.format(parent_id))


def children_child(parent_id_child,has_children_child):
    while has_children_child == True:
        response_child = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(parent_id_child), headers=NOTION_HEADERS)
        if response_child.status_code == 200:
            response_child = response_child.json()
            # print (response)
            childrens = [child for child in response_child['results']]
            print('\n Found {} children blocks: {} \n\n on the first level parent id {} \n\n'.format(len(childrens),childrens,parent_id_child))
            if len(childrens)<=0:
                break
            elif len(childrens)>0:
                childrens_id = [result['id'] for result in childrens]
                print(' \n Childrens_id found {} : {}  on the second level block id \n'.format(len(childrens_id),childrens_id))
                i=0
                for ida in childrens_id:
                    has_children_child = childrens[i]['has_children']
                    print('\n\n {} on the value of the block id: {} \n\n'.format(has_children_child,childrens[i]['id']))
                    children_child_child(ida,has_children_child)
                    print('\n\n FUNCTION CHILDREN_CHILD HAS BEEN LOOP ONCE \n\n')
                    i =  1+i
            # print('Esto es el valor de RESPONSE: \n {}'.format(response_child))

            has_children_child = response_child['results'][0]['has_children']
        else:
            print('\n There has been a error with the request {}{}\n'.format(response_child.status_code, response_child.text))
    if has_children_child == False:
         print('\n The block {} has no children in it \n'.format(parent_id_child))


def children_child_child(parent_id_child_child,has_children_child_child):
    while has_children_child_child == True:
        response_child_child = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(parent_id_child_child), headers=NOTION_HEADERS)
        if response_child_child.status_code == 200:
            response_child_child = response_child_child.json()
            # print (response)
            childrens = [child for child in response_child_child['results']]
            print('\n Found {} children blocks: {} \n\n on the first level parent id {} \n\n'.format(len(childrens),childrens,parent_id_child_child))
            if len(childrens)<=0:
                break
            elif len(childrens)>0:
                childrens_id = [result['id'] for result in childrens]
                print(' \n Childrens_id found {} : {}  on the second level block id \n'.format(len(childrens_id),childrens_id))
                i=0
                # for ida in childrens_id:
                #     has_children_child_child = childrens[i]['has_children']
                #     print('\n\n {} on the value of the block id: {} \n\n'.format(has_children_child_child,childrens[i]['id']))
                #     # children_child(ida,has_children_child_child)
                #     print('\n\n FUNCTION CHILDREN_CHILD HAS BEEN LOOP ONCE \n\n')
                #     i =  1+i
            # print('Esto es el valor de RESPONSE: \n {}'.format(response_child_child))
            has_children_child_child = response_child_child['results'][0]['has_children']
        else:
            print('\n There has been a error with the request {}{}\n'.format(response_child_child.status_code, response_child_child.text))
    if has_children_child_child == False:
        print('\n The block {} has no children in it \n'.format(parent_id_child_child))       


def children_b(parent_id,response,has_children):
    # has_children = response['results'][has_children]['has_children']
    while has_children == True:
        response = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(parent_id), headers=NOTION_HEADERS)
        if response.status_code == 200:
                response = response.json()
                childrens = [child for child in response['results']]
                print('\n Found {} children blocks: {} \n\n on the first level parent id {} \n\n'.format(len(childrens),childrens,parent_id))
                if len(childrens)<=0:
                    pass
                elif len(childrens)>0:

                    childrens_id = [result['id'] for result in childrens]
                    print(' \n Found {} childrens_id: {}  on the second level block id \n'.format(len(childrens_id),childrens_id))
                    parent_id = childrens_id
        else:
                print('Failed to retrive child blocks: {} {}'.format(response.status_code, response.text))
        if response['results'][0]['type']=='callout':
            child_id = response["results"][0]['id']
            if response['results'][0]['has_children']:
                print('\n\n el valor de child_id es: "{}" de tipo: {}'.format(child_id,type(child_id)))
                children(child_id,response,response['results'][0]['has_children'])
            else:
                callout_data = {
            "children":[{
                "type": "callout",
                "callout": response["results"][0]["callout"]
            }]}
                response = requests.patch(block_url, headers=NOTION_HEADERS, json=callout_data ) 
                pass
            break
        has_children = response['results'][0]['has_children']


def children_a(parent_id,response):
    print (response)
    i = 0
    for ideal in parent_id:     
        has_children = response['results'][i]['has_children']
        print(ideal)
        while has_children == True:
            response = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(ideal), headers=NOTION_HEADERS)
            if response.status_code == 200:
                    response = response.json()
                    childrens = [child for child in response['results']]
                    print('\n Found {} children blocks {}: '.format(len(childrens),childrens))
                    ideal = response['results'][0]['id']
            else:
                    print('Failed to retrive child blocks: {} {}'.format(response.status_code, response.text))
            if response['results'][0]['type']=='callout':
                child_id = response["results"][0]['id']
                if response['results'][0]['has_children']:
                    print('\n\n el valor de child_id es: "{}" de tipo: {}'.format(child_id,type(child_id)))
                    children(child_id,response)
                else:
                    callout_data = {
                "children":[{
                    "type": "callout",
                    "callout": response["results"][0]["callout"]
                }]}
                    response = requests.patch(block_url, headers=NOTION_HEADERS, json=callout_data ) 
                    pass
                break
            has_children = response['results'][0]['has_children']
            i =i+1

        pass


if __name__ == "__main__":
    response = requests.get(retrive_block_children_url, headers=NOTION_HEADERS)
    response = response.json()

    results = [result['id'] for result in response['results']]
    print (results)   

    children(results[0],response['results'][0]['has_children'])
    print('\n FUCTION CHILDREN ONCE \n \n')
    children(results[1],response['results'][1]['has_children'])
    print('\n FUCTION CHILDREN ONCE \n \n')     