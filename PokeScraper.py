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
        
        # Extract basic pokemon information specifically
        basic_info = extract_basic_info(soup)

        # Extract basic pokemon information specifically
        stats_info = extract_base_stats_info(soup)

        # Print the parsed information
        print(f"Pokemon: {pokemon_name}")
        print(f"Basic Pokemon Info: {basic_info}")
        print(f"Pokemon Evolution Information: {evolution_info}")
        print(f"{pokemon_name}'s Base Stats: {stats_info}")


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

def extract_basic_info(soup):
    # Find the first <p> tag 
    basic_info_paragraph = soup.find('p')

    if basic_info_paragraph:
        # Extract text content of the <p> tag
        basic_info = basic_info_paragraph.text.strip()
        return basic_info

    return 'Basic Pokemon Info Not Found'

def extract_base_stats_info(soup):
    # Find the header row that contains 'HP', 'Attack', 'Defense', etc.
    header_row = soup.find('tr', style='background: #FF5959; text-align:center')

    if header_row:
        # Extract the names of the stats
        stat_names = [th.text.strip() for th in header_row.find_all('th')]

        # Find the row containing the base stats values
        base_stats_row = soup.find('tr', style='background: #FF5959; text-align:center').find_next('tr')

        # Extract the base stats values
        base_stats_values = [td.text.strip() for td in base_stats_row.find_all(['th', 'td'])]

        # Combine the stat names and values into a formatted string
        stats_info_list = [f"{stat_names[i]}: {base_stats_values[i]}" for i in range(len(stat_names))]
        stats_info = '\n'.join(stats_info_list)

        return stats_info

    return 'Base Stats Information Not Found'


if __name__ == "__main__":
    # Get input from the user
    pokemon_name = input("Enter the Pokemon name: ")

    # Call the function with the user input
    get_pokemon_info(pokemon_name)
