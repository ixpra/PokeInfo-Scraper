import requests
from bs4 import BeautifulSoup

def get_pokemon_info(pokemon_name):
    base_url = 'https://bulbapedia.bulbagarden.net/wiki/'

    try:
        # Code to generate the Bulbapedia URL for the specific Pokemon's page
        pokemon_url = base_url + f'{pokemon_name}_(Pokémon)'

        # Send a GET request to the Bulbapedia page
        response = requests.get(pokemon_url)
        response.raise_for_status()  # Checks if the HTTP request was successful, if not responds with an error

        # Parse the HTML content from Bulbapedia with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract evolution information specifically
        evolution_info = extract_evolution_info(soup)

        # Extract base stats specifically
        stats_info = extract_base_stats(soup)

        # Extract weaknesses specifically
        weaknesses_info = extract_weaknesses(soup)


        # Print the parsed information
        print(f"Pokemon: {pokemon_name}")
        print(f"Evolution Information: {evolution_info}")
        print(f"Base Stats: {stats_info}")
        print(f"Weaknesses: {weaknesses_info}")


    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def extract_evolution_info(soup):
    # Find the <h3> tag containing the text 'Evolution'
    evolution_header = soup.find('span', {'id': 'Evolution'})

    if evolution_header:
        # If the <h3> is found, the code finds the first <p> tag after the <h3> tag
        evolution_paragraph = evolution_header.find_next('p')

        # This code extracts the text content of the <p> tag
        evolution_info = evolution_paragraph.text.strip() if evolution_paragraph else 'Not found'
        return evolution_info
    else:
        return 'Evolution Not found'

def extract_base_stats(soup):
    # Find the <th> tag containing the text 'Base stats'
    stats_header = soup.find('th', string='Base stats')

    if stats_header:
        # If the <th> is found, find the table containing base stats
        stats_table = stats_header.find_next('table')

        # Extract information from the table, assuming a specific structure
        if stats_table:
            # Extract base stats information
            stats_info = '\n'.join([row.text.strip() for row in stats_table.find_all('tr')[1:]])
            return stats_info

    return 'Base Stats not found'

def extract_weaknesses(soup):
    # Find the <th> tag containing the text 'Type effectiveness'
    weaknesses_header = soup.find('th', string='Type effectiveness')

    if weaknesses_header:
        # If the <th> is found, find the table containing weaknesses
        weaknesses_table = weaknesses_header.find_next('table')

        # Extract information from the table, assuming a specific structure
        if weaknesses_table:
            weaknesses_info = '\n'.join([row.text.strip() for row in weaknesses_table.find_all('tr')[1:]])
            return weaknesses_info

    return 'Weaknesses not found'


if __name__ == "__main__":
    # Get input from the user
    pokemon_name = input("Enter the Pokemon name: ")

    # Call the function with the user input
    get_pokemon_info(pokemon_name)
