import wikipedia
import wikipediaapi
import csv
import requests
import json
import geojson
wiki_wiki = wikipediaapi.Wikipedia('en')


# using wikipediaapi

def print_categorymembers(categorymembers, level=0, max_level=1):
        for c in categorymembers.values():
            # print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            print("%s" % (c.title))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)

# get category members
cat = wiki_wiki.page("Category:Beaux-Arts_architecture_in_New_York_City")


beaux_buildings = cat.categorymembers
titles_array = []

def summaries(buildings):
    i = 0
    for item in buildings:
        if i < 2:
            page = wiki_wiki.page(item)
            print("Page - Title: %s" % page.title)
            print("Page - Summary: %s" % page.summary[0:-1])
            i +=1

def makearray(buildings):
    for item in buildings:
        page = wiki_wiki.page(item)
        titles_array.append(page.title)


# array of all titles
makearray(beaux_buildings)

# empty array to fill with name, coords, description, images

all_info = []

#make function to get correct Images
def thumbnail_getter(page_name):
    this_id = wikipedia.page(page_name).pageid
    sid = str(this_id)
    print(this_id)
    wiki_dump = requests.get("http://en.wikipedia.org/w/api.php?action=query&titles={}&prop=pageimages&format=json&pithumbsize=300".format(page_name))
    wiki_json = wiki_dump.json()
    url = wiki_json['query']['pages'][sid]['thumbnail']['source']
    return(url)


#using wikipedia (this is confusing)

def getInfo(array):
    for article in array:
        print(article)
        try:
            coords = wikipedia.page(article).coordinates
            array_coords = [coords[0], coords[1]]
            latitude = coords[0]
            longitude = coords[1]
        except:
            coords = None
        try:
            description = wikipedia.page(article).summary
        except:
            description = None
        # for the image, we need to figure out how to get the main image each time
        # https://stackoverflow.com/questions/8363531/accessing-main-picture-of-wikipedia-page-by-api

        try:
            image = thumbnail_getter(article)
        except:
            image = None
        temp = [article, latitude, longitude, description, image]
        all_info.append(temp)

getInfo(titles_array)

#write to csv

filename = "data/test.csv"

fields = ['Name', 'Latitude', 'Longitude', 'Description', 'Images']

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(fields)
    csvwriter.writerows(all_info)

# next do the geojson convert: https://stackoverflow.com/questions/48586647/python-script-to-convert-csv-to-geojson

csvfile.close()
