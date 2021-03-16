import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon, request.build_absolute_uri(
                pokemon_entity.pokemon.image.url
            ))

    pokemons_on_page = []

    for pokemon in Pokemon.objects.all():
        image = pokemon.image.url if pokemon.image else None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image,
            'title_ru': pokemon.title,
        })
    
    pockemons = Pokemon.objects.all()

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_object = Pokemon.objects.get(id=pokemon_id)

    pokemon = {
        'pokemon_id': pokemon_object.id,
        'title_ru': pokemon_object.title,
        'img_url': request.build_absolute_uri(
                        pokemon_object.image.url
                    )
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon_object):
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon, request.build_absolute_uri(
                pokemon_entity.pokemon.image.url
            ))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
