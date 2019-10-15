from PIL import Image

import dialogs
import io
import photos
import requests

ALBUM_NAME = "iOS Logos"

ITUNES_API_URL = "https://itunes.apple.com/search"


def get_album():
	albums = photos.get_albums()
	albums = [a for a in albums if a.title == ALBUM_NAME]
	if not albums:
		return photos.create_album(ALBUM_NAME)
	else:
		return albums[0]

def search_itunes_api(app_name):
	params = {'term': term, 'entity': 'iPadSoftware'}
	return requests.get(ITUNES_API_URL, params=params).json()['results']

def retrieve_image(url):
	imageBytes = requests.get(url).content
	return Image.open(io.BytesIO(imageBytes))

def save_image_to_album(img):
	img.save(".tmp.png", "PNG")
	album = get_album()
	asset = photos.create_image_asset(".tmp.png")
	album.add_assets([asset])	
	
# Prompt for the app to search for
term = dialogs.input_alert("App Name", "Enter app to search for",
																											"Spark Readdle")
																											
# Search for the app on iTunes																										
results = search_itunes_api(term)

# Sometimes we get multiple hits from the search, so prompt
# the user to select the app they want
if not results:
	dialogs.alert("No App Found")
elif len(results) == 1:
	result = results[0]
else:
	trackNames = [r['trackName'] for r in results]
	selectedTrack = dialogs.list_dialog("Select App", trackNames)
	result = [r for r in results if r['trackName'] == selectedTrack][0]

# retrieve and save the image
img = retrieve_image(result['artworkUrl512'])
save_image_to_album(img)
