import aiohttp
import asyncio
import random

POKEMON_NAMES = ['pikachu', 'bulbasaur', 'charmander', 'squirtle', 'jigglypuff', 'meowth', 'psyduck', 'snorlax',
                 'machop', 'cubone']


async def fetch_pokemon_data(session, name):
    async with session.get(f'https://pokeapi.co/api/v2/pokemon/{name}') as response:
        return await response.json()


async def fetch_all_pokemon_data():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon_data(session, name) for name in POKEMON_NAMES]
        return await asyncio.gather(*tasks)


def calculate_strength(pokemon):
    stats = pokemon['stats']
    attack = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'attack')
    defense = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'defense')
    speed = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'speed')
    return attack + defense + speed


def simulate_battle(pokemon1, pokemon2):
    strength1 = calculate_strength(pokemon1)
    strength2 = calculate_strength(pokemon2)

    if strength1 > strength2:
        winner = pokemon1['name']
        winner_stats = strength1
        loser = pokemon2['name']
        loser_stats = strength2
    else:
        winner = pokemon2['name']
        winner_stats = strength2
        loser = pokemon1['name']
        loser_stats = strength1

    return {
        'winner': winner,
        'winner_stats': winner_stats,
        'loser': loser,
        'loser_stats': loser_stats
    }


def print_pokemon_data(pokemon):
    print(f"Name: {pokemon['name']}")
    stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon['stats']}
    for stat_name, value in stats.items():
        print(f"{stat_name.replace('-', ' ').capitalize()}: {value}")
    print()


async def main():
    pokemon_data = await fetch_all_pokemon_data()

    print("List of Pokemon and their data:\n")
    for pokemon in pokemon_data:
        print_pokemon_data(pokemon)

    battle_results = {name: 0 for name in POKEMON_NAMES}

    for _ in range(5):
        pokemon1, pokemon2 = random.sample(pokemon_data, 2)
        battle_result = simulate_battle(pokemon1, pokemon2)

        battle_results[battle_result['winner']] += 1

        print(f"The battle between {battle_result['winner']} and {battle_result['loser']}:")
        print(f"Winner: {battle_result['winner']} with power {battle_result['winner_stats']}")
        print(f"Loser: {battle_result['loser']} with power {battle_result['loser_stats']}\n")

    print("Final results of the battles:\n")
    for name, wins in battle_results.items():
        print(f"{name}: {wins} victories")


if __name__ == '__main__':
    asyncio.run(main())
