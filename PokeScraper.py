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


        # Print the parsed information
        print(f"Pokemon: {pokemon_name}")
        print(f"Basic Pokemon Info: {basic_info}")
        print(f"Evolution Information: {evolution_info}")


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
    # Find the first <p> tag with class 'roundy'
    basic_info_paragraph = soup.find('p')

    if basic_info_paragraph:
        # Extract text content of the <p> tag
        basic_info = basic_info_paragraph.text.strip()
        return basic_info

    return 'Basic Pokemon Info Not Found'




if __name__ == "__main__":
    # Get input from the user
    pokemon_name = input("Enter the Pokemon name: ")

    # Call the function with the user input
    get_pokemon_info(pokemon_name)
