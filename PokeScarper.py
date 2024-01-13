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

        # Extract generation information specifically
        generation_info = extract_generation_info(soup)

        # Extract type effectiveness information specifically
        #type_effectiveness_info = extract_type_effectiveness_info(soup)

        # Print the collected information
        print(f"Pokemon: {pokemon_name}")
        print(f"Evolution Information:\n{evolution_info}")
        print(f"Generation Information:\n{generation_info}")
        #print(f"Type Effectiveness Information:\n{type_effectiveness_info}")

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
        return 'Not found'

def extract_generation_info(soup):
    # Find the section containing generation information
    generation_section = soup.find('a', {'title': 'Generation'})

    if generation_section:
        # Find the sibling <td> element
        generation_td = generation_section.find_next('td')

        # Check if the <td> element exists and has text
        generation_info = generation_td.text.strip() if generation_td else 'Not found'
        return generation_info
    else:
        return 'Not found'

#def extract_type_effectiveness_info(soup):
    # Find the section containing type effectiveness information
    type_effectiveness_section = soup.find('span', {'id': 'Type_effectiveness'})

    if type_effectiveness_section:
        # Find the sibling <table> element
        type_effectiveness_table = type_effectiveness_section.find_next('table')

        if type_effectiveness_table:
            # Extract information from <td> elements
            type_effectiveness_info = ''
            for row in type_effectiveness_table.find_all('tr')[1:]:
                cells = row.find_all('td')

                # Check if the row has enough cells
                if len(cells) >= 2:
                    type_name = cells[0].text.strip()
                    effectiveness = cells[1].text.strip()
                    type_effectiveness_info += f"{type_name}: {effectiveness}\n"
                else:
                    type_effectiveness_info += 'Not found\n'

            return type_effectiveness_info

    return 'Not found'

if __name__ == "__main__":
    # Get input from the user
    pokemon_name = input("Enter the Pokemon name: ")

    # Call the function with the user input
    get_pokemon_info(pokemon_name)
