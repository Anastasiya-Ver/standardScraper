from pymongo_get_database import get_database
from scraper import getEntriesChecks
import yt_dlp
import os

# Get user input and correct it
query = input("What song would you like to download? ").lower()
quantity = input("How many versions? ")
if quantity.isdigit() == False:
	quantity = 1
	print("not a digit")
quantity = int(quantity)
if quantity > 95:
	print ("Too high.  Quantity set to 95. ")
	quantity = 95
kebabQuery = query.replace(" ", "+")

# Set up database and collection
dbname = get_database()
collectionList = dbname.list_collection_names()


collection = dbname[query]

# Populate collection
numDownloaded = 0
entryDict = getEntriesChecks(kebabQuery, quantity, query)
for key,value in entryDict.items():
	collection.insert_one(value)
	print("success", key)
	numDownloaded+= 1
collectionSize = collection.count_documents({})

# Download sequence
wantToPrint = input(str(numDownloaded)+" songs added.  There are "+str(collectionSize) + " songs available to download.  Press 'y' if you would like to download all available covers of "+query+" . If you would like to download a range, type the starting index.")

if wantToPrint.lower() == "y" or wantToPrint.isdigit() == True:
	downloadPath = r'C:\\Users\\nata\\Music\\Jazz Standards\\'+query
	if not os.path.exists(downloadPath):
		os.makedirs(downloadPath)

	URLS = []
	collection = dbname[query]
	songCursor = collection.find()
	for entry in songCursor:
		URLS.append(entry['URL'])


# this assumes that the user is using a start at 1 counting system.
if wantToPrint.isdigit() == True:
	closingIndex = input("From "+ wantToPrint + " up to what index?")
	if int(closingIndex) > quantity:
		closingIndex = quantity
	URLS = URLS[int(wantToPrint)-1::int(closingIndex)-1]


ydl_opts = {
    'format': 'mp3/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'paths' : {'home' : downloadPath}
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)
