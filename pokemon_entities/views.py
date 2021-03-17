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
        current_pokemon = pokemon_entity.pokemon
        image = current_pokemon.image.url if current_pokemon.image else DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon, request.build_absolute_uri(
                image
            ))

    pokemons_on_page = []

    for pokemon in Pokemon.objects.all():
        image = pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL
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
    raw_pokemon = Pokemon.objects.get(id=pokemon_id)
    evalution = raw_pokemon.evalution.all()
    print(evalution.first())
    progenitor = {} if not raw_pokemon.progenitor else {
        'title_ru': raw_pokemon.progenitor.title,
        'pokemon_id': raw_pokemon.progenitor.id,
        'img_url': request.build_absolute_uri(
            raw_pokemon.progenitor.image.url
        )
    }
    descendent = {} if not evalution.first() else {
        'title_ru': evalution.first().title,
        'pokemon_id': evalution.first().id,
        'img_url': request.build_absolute_uri(
            evalution.first().image.url
        )
    }

    pokemon = {
        'pokemon_id': raw_pokemon.id,
        'title_ru': raw_pokemon.title,
        'title_en': raw_pokemon.en_title,
        'title_jp': raw_pokemon.jp_title,
        'previous_evolution': progenitor,
        'next_evolution': descendent,
        'description': raw_pokemon.description,
        'img_url': request.build_absolute_uri(
                        raw_pokemon.image.url
                    )
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=raw_pokemon):
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon, request.build_absolute_uri(
                pokemon_entity.pokemon.image.url
            ))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
