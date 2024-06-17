from django.shortcuts import render
import urllib.request
import json
from django.contrib import messages
from urllib.error import HTTPError

def IndexView(request):
    try:
        if request.method == 'POST':
            pokemon = request.POST['pokemon'].lower()
            pokemon = pokemon.replace(' ', '%20')
            url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
            url_pokeapi.add_header('User-Agent', 'pokeapi')

            source = urllib.request.urlopen(url_pokeapi).read()

            list_data = json.loads(source)

            converted_height = (float(list_data['height'])*0.1)
            rounded_height = round(converted_height, 2)

            converted_weight = (float(list_data['weight'])*0.1)
            rounded_weight = round(converted_weight, 2)

            data = {
                'number': str(list_data['id']),
                'name': str(list_data['name']).capitalize(),
                'height': str(rounded_height) + ' m',
                'weight': str(rounded_weight) + ' kg',
                'sprite': str(list_data['sprites']['front_default']),
                'type': str(list_data['types'][0]['type']['name']).capitalize()
            }
            print(data)
        else:
            data = {}
        return render(request, 'index.html', data)
    except HTTPError as e:
        if e.code == 404:
            messages.error(request, 'El pokémon no se ha encontrado! :(')
            return render(request, 'index.html', {'error_message': messages})
