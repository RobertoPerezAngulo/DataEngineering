import requests
from decouple import config
import logging

# Deficion de la funcion get
def get():
    try:
        url = config('URL')
        data = requests.get(url).json()
        collections = []
        offset = 2
        for index, item in enumerate(data.get('results'), start=offset):
            collections.append({'name': item.get('name'),
                                'img': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{index}.png'})       
        return collections
    except Exception as e:
        logging.error(f'Fix on {e}')
        

# Ejecucion de la funcion get
print(get())