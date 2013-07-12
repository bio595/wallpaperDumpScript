import httplib2, json, os, random
from threading import Thread


class WallpaperDownloader(object):

	def __init__(self):
		self.download_dir = os.path.expanduser("~/Desktop/wallpaperdump/")
		self.finished_downloading = False

	def get_downloaded_album(self):
		downloads = os.listdir(self.download_dir)
		downloads = [self.download_dir + path for path in downloads]
		print downloads
		random.shuffle(downloads)
		return downloads

	def download_album(self):
		self.finished_downloading = False
		Thread(target=self.__do_download).start()

	def has_finished_downloading(self):
		print self.finished_downloading
		return self.finished_downloading

	def __do_download(self):

		def sortByUpvotes(post_x, post_y):
			return post_y['data']['ups'] - post_x['data']['ups']



		#Find an album on /r/wallpaperdump and download it
		print "Querying reddit"
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

		print "Quering imgur"
		#Create a new connection object for talking to imgur api
		http = httplib2.Http()
		headers = {"Authorization" : "Client-ID 834426095b05c80"}
		url = "https://api.imgur.com/3/album/"+ album_id + "/images"
		resp, content = http.request(url, "GET", headers=headers)

		images = json.loads(content)['data']

		#make the wallpaperdump folder if doesnt already exist
		if not os.path.exists(self.download_dir):
			os.makedirs(self.download_dir)

		print "Number of images in album: " + str(len(images))
		#Download each item
		for i, image in enumerate(images):
			resp, content = http.request(image['link'], "GET")			
			with open(self.download_dir + image['link'][len("http://i.imgur.com/"):], 'w') as f:
				f.write(content)
			print "Downloading " + image['link'] + "\t" + str(float(i + 1) / len(images) * 100) + "%"
			
		self.finished_downloading = True
		print "Finished"





