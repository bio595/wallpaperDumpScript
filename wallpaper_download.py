import httplib2, json, os
from threading import Thread


class WallpaperDownloader(object):

	def __init__(self):
		pass

	def get_downloaded_album(self):
		#Get the download album as a list of paths to files
		pass

	def download_album(self):
		Thread(target=self.__do_download).start()
		pass

	def __do_download(self):

		def sortByUpvotes(post_x, post_y):
			return post_y['data']['ups'] - post_x['data']['ups']

		#Find an album on /r/wallpaperdump and download it
		
		http = httplib2.Http()
		resp, content = http.request("http://www.reddit.com/r/wallpaperdump/new.json?limit=100", "GET")
		posts = json.loads(content)['data']['children']
		

		#Remove NSFW posts and posts that aren't imgur albums
		for post in posts:
			if post['data']['over_18'] or not post['data']['url'].startswith("http://imgur.com/a/"):
				posts.remove(post)


		#Could select the album by random
		#Sort by upvotes, get the highest rated post
		posts.sort(sortByUpvotes)
		album_id = posts[0]['data']['url'][len("http://imgur.com/a/"):]

		#Create a new connection object for talking to imgur api
		http = httplib2.Http()
		headers = {"Authorization" : "Client-ID 834426095b05c80"}
		url = "https://api.imgur.com/3/album/"+ album_id + "/images"
		resp, content = http.request(url, "GET", headers=headers)

		images = json.loads(content)['data']
		
		download_dir = os.path.expanduser("~/Desktop/wallpaperdump/")

		#make the wallpaperdump folder if doesnt already exist
		if not os.path.exists(download_dir):
			os.makedirs(download_dir)

		#Download each item
		for image in images:
			print "Downloading " + image['link']
			resp, content = http.request(image['link'], "GET")			
			with open(download_dir + image['link'][len("http://i.imgur.com/"):], 'w') as f:
				f.write(content)





