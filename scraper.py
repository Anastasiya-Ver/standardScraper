import requests
from bs4 import BeautifulSoup
import bs4
import time
from pymongo_get_database import get_database

# set up database
dbname = get_database()


# Will return the song URL of the first option (should generally be the right one)
def workURL(songInput):
	baseURL = "https://secondhandsongs.com/search/work?title=" + songInput
	response = requests.get(baseURL, params={"format": "json"})
	out = response.json()
	songURL = out['resultPage'][0]['uri']
	return songURL

# Will return the URL of every cover with a youtube link
def versionURL(workURL):
	allVersionsList = []
	versionListURL = workURL + "/versions"
	response = requests.get(versionListURL) 
	soup = BeautifulSoup(response.text, "html.parser")
	for i in soup.find_all("i", {"title":"listen on YouTube"}):
		relativeURL = i.find_parent().get('href')
		if "performance" in relativeURL:
			versionURL = "https://secondhandsongs.com" + relativeURL
			allVersionsList.append(versionURL)
	return allVersionsList





# Will return the link, album art, album title, and performer name of each cover
# API will NOT work because it doesn't give me the link and album art
def versionInfo(URL=""):
	response = requests.get(URL)
	soup = BeautifulSoup(response.text,"html.parser")

	dictPerformance = {}
	dictPerformance['URLSHS'] = URL
	# Link
	SHSURL = soup.find_all("a", {"title" : "Go to YouTube"})

	for URL in SHSURL:
		dictPerformance['URL'] = URL.get('href')

	# Album Name
	aTagAlbumName = soup.find_all("a", {"class": "link-release"})
	for name in aTagAlbumName:
		albumName = BeautifulSoup(name.text, "html.parser").text
		dictPerformance['albumName'] = albumName

	# Album Art
	for imgTag in soup.find_all('img', {'alt' : 'video'}):
		dictPerformance['albumArt'] = imgTag.get('src')	

	# Performer Name
	aTagArtist = soup.find_all("a", {"class": "link-proxies\\__cg__\\performer"})
	for tag in aTagArtist:
		artist = BeautifulSoup(tag.text, "html.parser").text
		dictPerformance['artist'] = artist

	# Release Date
	# This might break later (IT BROKE)
	# iDate = 0
	# ddTagDate = soup.find_all("dd")
	# for tag in ddTagDate:
	# 	if iDate == 2:
	# 		dictPerformance['date'] = BeautifulSoup(tag.text, "html.parser").text
	# 	iDate+=1

	# Return
	return dictPerformance

# Will go through every cover and return its information
def getEntries(songname, quantity=1):
	output = {}
	quantity = int(quantity)
	versionURLList = versionURL(workURL(songname))

	# prevent quantity from going out of bounds or too high
	if quantity > len(versionURLList):
		quantity = len(versionURLList)

	for URL in versionURLList[:quantity]:
		output[URL] = versionInfo(URL)
		print(URL)

	return output

def getEntriesChecks(songname, quantity, collectionName):
	output = {}
	quantity = int(quantity)
	versionURLList = versionURL(workURL(songname))
	# prevent quantity from going out of bounds or too high
	if quantity > len(versionURLList):
		quantity = len(versionURLList)
	# not found in collection
	if collectionName == "":
		for URL in versionURLList[:quantity]:
			output[URL] = versionInfo(URL)
			print(URL)
	# found in collection
	else:
		collection = dbname[collectionName]
		for URL in versionURLList[:quantity]:
			x = collection.find_one({"URLSHS":URL})
			if x is None :
				output[URL] = versionInfo(URL)

	return output