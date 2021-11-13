from bs4 import BeautifulSoup as bs
from tqdm import tqdm

import requests
import os

OU_PATH = "./output/"

OU_PATH_BACK = OU_PATH + "back/"
OU_PATH_FRONT = OU_PATH + "front/"
OU_PATH_BACK_SHINY = OU_PATH + "back_shiny/"
OU_PATH_FRONT_SHINY = OU_PATH + "front_shiny/"

NUMBER_OF_POKEMONS = 151 #First gen pokemons

#URLs
URL_FRONT_SHINY_SPRITES = "https://archives.bulbagarden.net/wiki/Category:Black_and_White_Shiny_sprites"
URL_FRONT_SPRITES = "https://archives.bulbagarden.net/wiki/Category:Black_and_White_sprites"
URL_BACK_SHINY_SPRITES = "https://archives.bulbagarden.net/wiki/Category:Black_and_White_Shiny_back_sprites"
URL_BACK_SPRITES = "https://archives.bulbagarden.net/wiki/Category:Black_and_White_back_sprites"

def main():
    get_front_sprites()
    get_front_shiny_sprites()
    get_back_sprites()
    get_back_shiny_sprites()

def get_front_sprites():
    urls = get_images(URL_FRONT_SPRITES)
    download(OU_PATH_FRONT, urls)

def get_back_sprites():
    urls = get_images(URL_BACK_SPRITES)
    download(OU_PATH_BACK, urls)

def get_front_shiny_sprites():
    urls = get_images(URL_FRONT_SHINY_SPRITES)
    download(OU_PATH_FRONT_SHINY, urls)

def get_back_shiny_sprites():
    urls = get_images(URL_BACK_SHINY_SPRITES)
    download(OU_PATH_BACK_SHINY, urls)

def get_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    
    urls = {}
    
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        
        img_name = str(img.attrs.get("alt")).lower().replace(" ", "_")
        img_url = img.attrs.get("src")
        
        if not img_url or not img_name or img_name[0:3] != "spr":
            # if img does not contain src attribute, just skip
            continue
        
        urls[img_name] = img_url
    
    print(url)

    return urls

def download(path, urls):

    if not os.path.isdir(path):
        os.makedirs(path)
    
    for url in urls:
        file_name = url
        file_download_path = urls[url]

        print(file_name)
        print(file_download_path)
        
        if not os.path.exists(path + file_name):
            response = requests.get(file_download_path, stream=True)
            file_size = int(response.headers.get("Content-Length", 0))
            progress = tqdm(response.iter_content(1024), f"Downloading {file_name}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

            with open(path + file_name, "wb") as f:
                for data in progress.iterable:
                    # write data read to the file
                    f.write(data)
                    # update the progress bar manually
                    progress.update(len(data))

if __name__ == "__main__":
    main()