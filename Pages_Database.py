import requests
import json

def run():            
    notion_api_key = 'secret_iVyHhWq151i1PR605FxY4xivJ2SbxSIl9sY6RroJD4h'
    search_pages_url = 'https://api.notion.com/v1/search'
    notion_headers = {
        'Notion-Version': '2022-06-28',
        'Authorization': 'Bearer {}'.format(notion_api_key),
        'Content-Type': 'application/json', 
    }


    data_search = {
        'query':'Notas',
        'filter': {
            'value': 'database',
            'property': 'object'
        }
        }


    response = requests.post(search_pages_url, json=data_search, headers=notion_headers)
    response = response.json()
    results = int(len(response['results']))
    print('The number of results of your petition is: {}'.format(results))
    # print(response)
    has_more = response['has_more']

# It retrives each of the databases that functions as Notebooks
    i=0
    for result in response['results']:
        book_title = response['results'][i]['title'][0]['text']['content']
        content = response['results'][i]
        i = i + 1
        print(f'El cuaderno que encontramos es: {book_title}')
        print(f'El contenido de este libro es: \n {content} \n')
        




    while has_more == True:
        if has_more== True:
            filter = {'start_cursor': response ['next_cursor']}
            response = requests.post(search_pages_url, json=data_search, headers=notion_headers)
            print('\n \n \n ***************************************************************************************************' )
            response = response.json()
            # print(response)
            add = len(response['results'])
            print(f'The value of add equals to: {add}')
            results =  results + add
            print (f'Los resultados Totales hasta ahora son: {results}')
            has_more = response['has_more']
        elif has_more == False:
            break


    print('\n El TOTAL de tus resultados es: {}'.format(results))
    print('The number of results of your petition is: {}'.format(results))


if __name__ == '__main__':
    run()