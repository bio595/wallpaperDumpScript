import httplib2, json, os, random, time, sys
from threading import Thread


class WallpaperDownloader(object):

	def __init__(self, subreddit="wallpaperdump", download_dir="~/Desktop/wallpaperdump/"):
		if download_dir[-1] != "/":
			download_dir += "/"
		self.download_dir = os.path.expanduser(download_dir)
		self.finished_downloading = False
		self.download_progress = "0%"
		self.subreddit = subreddit

	def get_downloaded_album(self):
		downloads = os.listdir(self.download_dir)
		downloads = [self.download_dir + path for path in downloads]
		random.shuffle(downloads)
		return downloads

	def download_album(self):
		self.finished_downloading = False
		self.download_progress = "0%"
		Thread(target=self.__do_download).start()

	def __check_subreddit_exists(self):
		http = httplib2.Http()
		r, c = http.request("http://www.reddit.com/subreddits/search.json?q={0}&limit=1".format(self.subreddit), "GET")
		j = json.loads(c)
		return len(j['data']['children']) == 1

	def get_download_progress(self):
		return self.download_progress

	def has_finished_downloading(self):
		return self.finished_downloading


	def __get_posts_from_subreddit(self):
		http = httplib2.Http()
		resp, content = http.request("http://www.reddit.com/r/{0}/new.json?limit=100".format(self.subreddit), "GET")
		posts = json.loads(content)['data']['children']
		
		#Remove NSFW posts and posts that aren't imgur albums
		return [post for post in posts if not post['data']['over_18'] and post['data']['url'].startswith("http://imgur.com/a/") ]

	def __get_image_list_from_imgur(self, album_id):
		print "Quering imgur"
		#Create a new connection object for talking to imgur api
		http = httplib2.Http(disable_ssl_certificate_validation=True)
		headers = {"Authorization" : "Client-ID 834426095b05c80"}
		url = "https://api.imgur.com/3/album/"+ album_id + "/images"
		resp, content = http.request(url, "GET", headers=headers)

		return json.loads(content)['data']

	def __download_image(self, image):
		#check if we've already downloaded this image before
		downloads = os.listdir(self.download_dir)

		filename = image['link'][len("http://i.imgur.com/"):]
		if not filename in downloads:
			http = httplib2.Http()
			resp, content = http.request(image['link'], "GET")			
			with open(self.download_dir + filename, 'wb') as f:
				f.write(content)
		else:
			print "Duplicate image: {0}".format(filename)

	def __do_download(self):

		#Find an album on /r/wallpaperdump and download it
		print "Querying reddit"
		
		if not self.__check_subreddit_exists():
			print "subreddit does not exist, sorry"
			return

		posts = self.__get_posts_from_subreddit()

		#Select the album randomly
		post_index = 0 #int(random.random() * len(posts) - 1)

		#Find the album ID
		album_id = posts[post_index]['data']['url'][len("http://imgur.com/a/"):]
		print posts[post_index]['data']['title']
		
		#remove anchor to a specific image if it exists
		if '#' in album_id:
			album_id = album_id[:album_id.index('#')]

		print "Album ID: " + album_id

		images = self.__get_image_list_from_imgur(album_id)
		print "Number of images in album: " + str(len(images))
		
		#make the wallpaperdump folder if doesnt already exist
		if not os.path.exists(self.download_dir):
			os.makedirs(self.download_dir)

		#Download each item
		for i, image in enumerate(images):
			self.__download_image(image)
			self.download_progress = str(float(i + 1) / len(images) * 100) + "%"
			sys.stdout.write( "Downloading " + image['link'] + "\t" + self.download_progress + "\r")
			sys.stdout.flush()
		
		print "\n"
		self.finished_downloading = True
		print "Finished downloading"


def main():
	wd = WallpaperDownloader("pics", "~/Desktop/test")
	wd.download_album()

if __name__ == '__main__':
	main()