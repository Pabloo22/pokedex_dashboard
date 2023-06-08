import requests
import os

# Create a directory to store the images
os.makedirs('../images/', exist_ok=True)

# Change the working directory to the images directory
os.chdir('../images/')

# Download the images
for i in range(1, 802):
    url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/' + str(i).zfill(3) + '.png'
    r = requests.get(url)
    with open(str(i).zfill(3) + '.png', 'wb') as f:
        f.write(r.content)
    print('Downloaded ' + str(i).zfill(3) + '.png')
