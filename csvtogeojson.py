import csv

# major hat tip to Chenyu for the logic of this Description
# source: https://chenyuzuoo.github.io/posts/56646/

filename = "data/test.csv"

csv_file = csv.reader(open(filename, 'r', encoding="utf8"), dialect='excel')


item_template = \
''' \
  {
    "type": "Feature",
    "geometry": {
       "type": "Point",
       "coordinates":  [ %s, %s]
    },
    "properties": {
    "Name": "%s",
    "Description":"%s",
    "Images":"%s"
    },
'''

geojson_start = \
   ''' \

{ "type" : "Feature Collection",
   "features" : [
   '''
#go through csv and get each piece of data
for row in csv_file:
    lat = row[1]
    long = row[2]
    name = row[0]
    descr = row[3]
    img_url = row[4]
    geojson_start += item_template % (lat, long, name, descr, img_url)

    geojson_start += \
    ''' \
    ]
    }
    '''

outFileHandle = open("data/filename.geojson", "w")
outFileHandle.write(geojson_start)
outFileHandle.close()
print("done")
