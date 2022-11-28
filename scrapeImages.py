import os
import requests
from bs4 import BeautifulSoup

os.makedirs("images", exist_ok=True)

# Download the page
res = requests.get("https://www.ea.com/en-au/games/apex-legends/about/characters")
res.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(res.text, "html.parser")

# Get the media URL in each tile element
image_urls = []
for el in soup.select("ea-tile"):
    image_urls.append(el["media"])

# Verify the URLs work
for url in image_urls:
    res = requests.get(url)
    res.raise_for_status()
    if res.status_code == requests.codes.ok:
        # Download the images
        print('Downloading image %s...' % url)
        with open(os.path.join("images", os.path.basename(url)), "wb") as image:
            for chunk in res.iter_content(100000):
                image.write(chunk)
    else:
        print(f"Could not download {url}")

print("Done")
