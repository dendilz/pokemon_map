import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon):
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon.title_ru, request.build_absolute_uri(pokemon.image.url) if pokemon.image else '')

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else '',
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_on_page = {
        'pokemon_id': pokemon_id,
        'img_url': pokemon.image.url if pokemon.image else '',
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description
    }

    if pokemon.next_evolution:
        pokemon_on_page['next_evolution'] = {
            'pokemon_id': pokemon.next_evolution.id,
            'title_ru': pokemon.next_evolution.title_ru,
            'img_url': pokemon.next_evolution.image.url
            if pokemon.next_evolution.image else ''
        }

    if pokemon.previous_evolution:
        pokemon_on_page['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': pokemon.previous_evolution.image.url
            if pokemon.previous_evolution.image else ''
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title_ru, request.build_absolute_uri(pokemon.image.url) if pokemon.image else '')

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_on_page})
