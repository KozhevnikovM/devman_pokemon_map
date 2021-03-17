import folium

from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def get_pokemon_image_url(request, pokemon):
    """Get absolute pokemon image url or default image url"""
    if not pokemon.image:
        return DEFAULT_IMAGE_URL

    return request.build_absolute_uri(pokemon.image.url)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    """Add one pokemon on map"""
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_pokemons_map(request, pokemon_entities):
    """Add pokemon_entities on folium map"""
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            get_pokemon_image_url(request, pokemon_entity.pokemon)
        )
    return folium_map


def show_all_pokemons(request):
    """Main page with pokemons and map"""
    folium_map = show_pokemons_map(request, PokemonEntity.objects.all())

    pokemons_on_page = [
        {
            'pokemon_id': pokemon.id,
            'img_url': get_pokemon_image_url(request, pokemon),
            'title_ru': pokemon.title,
        }
        for pokemon in Pokemon.objects.all()
    ]

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    """Pokemon personal page"""
    raw_pokemon = Pokemon.objects.get(id=pokemon_id)
    raw_descendent = raw_pokemon.evalution.first()

    progenitor = {} if not raw_pokemon.progenitor else {
        'title_ru': raw_pokemon.progenitor.title,
        'pokemon_id': raw_pokemon.progenitor.id,
        'img_url': get_pokemon_image_url(request, raw_pokemon.progenitor)
    }
    descendent = {} if not raw_descendent else {
        'title_ru': raw_descendent.title,
        'pokemon_id': raw_descendent.id,
        'img_url': request.build_absolute_uri(
            raw_descendent.image.url
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
        'img_url': get_pokemon_image_url(request, raw_pokemon)
    }
    folium_map = show_pokemons_map(
        request,
        PokemonEntity.objects.filter(pokemon=raw_pokemon)
    )
    return render(
        request,
        "pokemon.html",
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon
        }
    )
