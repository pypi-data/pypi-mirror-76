'''
Imports Used in Package
'''
import requests
from bs4 import BeautifulSoup
import random
import csv
import json
import urllib.request
from fake_useragent import UserAgent
import time


# Main Class Starts Here


"""
User Agents
"""
try:
    ua = UserAgent()
except:
    time.sleep(1)
    ua = UserAgent()



class Imager:
    """
    Imager Class: The  Main Class
    :Fucntions:
            DogPile,Ecosia,Unsplash,Getty,Shutterstock
    """

    def DogPile(query, page, ft=None):
        """DogPile Search Images from Dogpile Search Engine.
        :param page:
            Set numbers of pages you want to Search.
        :param ft:
            set Ouput Type (Json,CSV,txt) ..... (json,csv,txt)
        :return:
            Depending on your ft value your ouput is generated.If you not enter Any ft Param then Function returns list.
        """
        links_imgs = []
        der_links = []
        for i in range(1, page):
            try:
                headers = {"User-Agent": '{}'.format(ua.random)}
                html = requests.get(f"https://www.dogpile.com/serp?q={query}&page={i}&sc=mvdP7cm6rBRP20",
                                    headers=headers).content
                soup = BeautifulSoup(html, "html.parser")
                links_imgs = [i.get("href") for i in soup.find_all("a", {"class": "link"})]
            except Exception as e:
                continue
            der_links.append(links_imgs)
        imgs_dogpile = [j for i in der_links for j in i]
        print("Pictures Derived : ", len(imgs_dogpile))
        if ft == "csv":
            links_imgs = [["Link", "Query"]]
            for i in range(len(imgs_dogpile)):
                links_imgs.append(["{}".format(imgs_dogpile[i]), "{}".format(query)])
            with open(f'imager.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(links_imgs)
            print("CSV Created")
        elif ft == "txt":
            with open("imager.txt", "w") as file:
                for i in imgs_dogpile:
                    file.write("{}\n".format(i))
                file.close()
            print("Txt File Created")
        elif ft == "json":
            data_json = []
            for i in range(len(imgs_dogpile)):
                data = {
                    "ID": i,
                    "Link": imgs_dogpile[i],
                    "Query": query
                }
                data_json.append(data)
            with open('imager.json', 'w', encoding='utf-8') as file:
                json.dump(data_json, file, ensure_ascii=False, indent=4)
            print("Json is Created")
        else:
            return imgs_dogpile

    def Ecosia(query, page, ft=None):
        """Ecosia Search Images from Ecosia Search Engine.
        :param page:
            Set numbers of pages you want to Search.
        :param ft:
            set Ouput Type (Json,CSV,txt) ..... (json,csv,txt)
        :return:
            Depending on your ft value your ouput is generated.If you not enter Any ft Param then Function returns list.
        """
        ancors = []
        for i in range(1, page):
            try:
                headers = {"User-Agent": '{}'.format(ua.random)}
                soup = BeautifulSoup(
                    requests.get(f"https://www.ecosia.org/images?q={query}&p={i}", headers=headers).content,
                    "html.parser")
                anchors = soup.find_all("a", class_="image-result")
                ancors.append(anchors)
            except:
                continue
        imgs = [j.attrs.get('href') for i in ancors for j in i]
        print("Pictures Derived : ", len(imgs))
        if ft == "csv":
            links_imgs = [["Link", "Query"]]
            for i in range(len(imgs)):
                links_imgs.append(["{}".format(imgs[i]), "{}".format(query)])
            with open(f'imager.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(links_imgs)
            print("CSV Created")
        elif ft == "txt":
            with open("imager.txt", "w") as file:
                for i in imgs:
                    file.write("{}\n".format(i))
                file.close()
            print("Txt File Created")
        elif ft == "json":
            data_json = []
            for i in range(len(imgs)):
                data = {
                    "ID": i,
                    "Link": imgs[i],
                    "Query": query
                }
                data_json.append(data)
            with open('imager.json', 'w', encoding='utf-8') as file:
                json.dump(data_json, file, ensure_ascii=False, indent=4)
            print("Json is Created")
        else:
            return imgs

    def Unsplash(query, page, ft=None):
        """Unsplash Search Images from Unsplash Search Engine.
                :param page:
                    Set numbers of pages you want to Search.
                :param ft:
                    set Ouput Type (Json,CSV,txt) ..... (json,csv,txt)
                :return:
                    Depending on your ft value your ouput is generated.If you not enter Any ft Param then Function returns list.
        """
        images = []
        for i in range(1, page):
            html = requests.get(f"https://unsplash.com/napi/search/photos?query={query}&xp=&per_page=20&page={i + 1}")
            data = json.loads(html.content)
            values = []
            for i in range(len(data['results'])):
                value = data['results'][i]
                values.append(value)
            for i in range(len(values)):
                value = values[i]['urls']['full']
                images.append(value)
        print("Pictures Derived : ", len(images))
        if ft == "csv":
            links_imgs = [["Link", "Query"]]
            for i in range(len(images)):
                links_imgs.append(["{}".format(images[i]), "{}".format(query)])
            with open(f'imager.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(links_imgs)
            print("CSV Created")
        elif ft == "txt":
            with open("imager.txt", "w") as file:
                for i in images:
                    file.write("{}\n".format(i))
                file.close()
            print("Txt File Created")
        elif ft == "json":
            data_json = []
            for i in range(len(images)):
                data = {
                    "ID": i,
                    "Link": images[i],
                    "Query": query
                }
                data_json.append(data)
            with open('imager.json', 'w', encoding='utf-8') as file:
                json.dump(data_json, file, ensure_ascii=False, indent=4)
            print("Json is Created")
        else:
            return images

    def Getty(query, ft=None):
        """Getty Search Images from Getty Search Engine.
            :param ft:
                    set Ouput Type (Json,CSV,txt) ..... (json,csv,txt)
            :return:
                    Depending on your ft value your ouput is generated.If you not enter Any ft Param then Function returns list.
        """
        list_agents = line
        headers = {"User-Agent": '{}'.format(random.choice(list_agents))}
        soup = BeautifulSoup(requests.get(f"https://www.gettyimages.com/photos/{query}", headers=headers).content, "html.parser")
        images = soup.findAll('img', class_="gallery-asset__thumb")
        links = []
        for i in images:
            links.append(i.attrs.get("src"))
        print("Pictures Derived : ", len(links))
        if ft == "csv":
            links_imgs = [["Link", "Query"]]
            for i in range(len(links)):
                links_imgs.append(["{}".format(links[i]), "{}".format(query)])
            with open(f'imager.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(links_imgs)
            print("CSV Created")
        elif ft == "txt":
            with open("imager.txt", "w") as file:
                for i in links:
                    file.write("{}\n".format(i))
                file.close()
            print("Txt File Created")
        elif ft == "json":
            data_json = []
            for i in range(len(links)):
                data = {
                    "ID": i,
                    "Link": links[i],
                    "Query": query
                }
                data_json.append(data)
            with open('imager.json', 'w', encoding='utf-8') as file:
                json.dump(data_json, file, ensure_ascii=False, indent=4)
            print("Json is Created")
        else:
            return links

    def Shutterstock(query, page, ft=None):
        """Shutterstock Search Images from Shutterstock Search Engine.
                :param page:
                    Set numbers of pages you want to Search.
                :param ft:
                    set Ouput Type (Json,CSV,txt) ..... (json,csv,txt)
                :return:
                    Depending on your ft value your ouput is generated.If you not enter Any ft Param then Function returns list.
                """
        list_agents = line
        headers = {"User-Agent": '{}'.format(random.choice(list_agents))}
        links = []
        for i in range(1, page):
            soup = BeautifulSoup(requests.get(f"https://www.shutterstock.com/search/{query}?page={i}", headers=headers).content,
                        "html.parser")
            imgs_links = soup.find_all('img')
            for i in imgs_links:
                if i.get('src') == None:
                    pass
                else:
                    links.append(i.get('src'))
        print("Pictures Derived : ", len(links))
        if ft == "csv":
            links_imgs = [["Link", "Query"]]
            for i in range(len(links)):
                links_imgs.append(["{}".format(links[i]), "{}".format(query)])
            with open(f'imager.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(links_imgs)
            print("CSV Created")
        elif ft == "txt":
            with open("imager.txt", "w") as file:
                for i in links:
                    file.write("{}\n".format(i))
                file.close()
            print("Txt File Created")
        elif ft == "json":
            data_json = []
            for i in range(len(links)):
                data = {
                    "ID": i,
                    "Link": links[i],
                    "Query": query
                }
                data_json.append(data)
            with open('imager.json', 'w', encoding='utf-8') as file:
                json.dump(data_json, file, ensure_ascii=False, indent=4)
            print("Json is Created")
        else:
            return links
