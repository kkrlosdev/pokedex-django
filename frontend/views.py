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

            data = {
                'number': str(list_data['id']),
                'name': str(list_data['name']).capitalize(),
                'height': str(list_data['height']),
                'weight': str(list_data['weight']),
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
