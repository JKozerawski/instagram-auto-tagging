import os
import urllib
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from glob import glob
import filecmp
import pickle
import random
from pyvirtualdisplay import Display



class ImageDownloader():
	def __init__(self, savePath):
		self.savePath = savePath
		self.justMostRecent = False

	def set_tag(self, tag):
		self.tag = tag

	def check_if_file_exists(self):
		for txtFile in self.txtFiles:
			if ( filecmp.cmp('./temp.txt', txtFile) ): return False
		return True
	
	def download_images(self, tag=None):

		# set tag:
		if(tag!=None): self.set_tag(tag)

		# create folder if one does not exist:
		if(not os.path.isdir(self.savePath+self.tag+"/")):
			os.mkdir(self.savePath+self.tag+"/")

		#url to go to:
		page_url = "https://www.instagram.com/explore/tags/"+self.tag+"/"
		display = Display(visible=0, size=(800, 600))
		display.start()
		#Chrome stuff:
		driver = webdriver.Chrome()
		driver.get(page_url)
		soup = BeautifulSoup(driver.page_source,"lxml")

		# check how many images are in the folder already:
		count = len(glob(self.savePath+self.tag+"/"+"*jpg"))
		self.txtFiles = glob(self.savePath+self.tag+"/"+"*txt")	
		assert count == len(self.txtFiles)


		#iterate over the pictures
		for index, pictureParent in enumerate(soup.find_all('div', attrs={'class': '_4rbun'})) :
			# omit the top posts
			if(index >= 9) :

				# get the description:
				try:
					caption = pictureParent.contents[0] ['alt']
					captionText = caption.encode('UTF-8').lower()	# lowercase the description

					f= open("./temp.txt","w+") #the + lets it create the file
					f.write(captionText)
					f.close()
					# proceed only if actual hashtag is in the description and if file has already been downloaded:
					if("#"+self.tag in captionText and self.check_if_file_exists()):
						count+=1
						#download the image:
						url = pictureParent.contents[0] ['src']

						# name the image file:
						imageFilename = self.savePath+self.tag+"/" + str(count-1) + ".jpg"
						urllib.urlretrieve(url, imageFilename)

						#save the caption in a text file:
						# name the description file:
						textFilename = self.savePath+self.tag+"/" + str(count-1) + ".txt"
						f= open(textFilename,"w+") #the + lets it create the file
						f.write(captionText)
						f.close()
				except:
					print "Some error"

				
		driver.quit()
		display.stop()

	def get_x_tags(self, tag, noOfTagsToDownload):
		self.set_tag(tag)
		if( len(glob(self.savePath+self.tag+"/"+"*jpg")) <=noOfTagsToDownload):
			prev_n = len(glob(self.savePath+self.tag+"/"+"*jpg"))
			self.download_images()
			print "Scraping:",self.tag, "Scraped:",len(glob(self.savePath+self.tag+"/"+"*jpg")) - prev_n, "new images.","Left:", len(self.listOfTags), "categories"
		else: self.listOfTags.remove(self.tag)

	def go_through_list_of_tags(self, listOfTags, noOfTagsToDownload):
		random.shuffle(listOfTags)
		listOfTags = [x.lower() for x in listOfTags]
		self.listOfTags = listOfTags
		print self.listOfTags
		while(len(self.listOfTags)>0 ):
			for tag in self.listOfTags:
				self.get_x_tags(tag, noOfTagsToDownload)
				


#------------------------------------------------------------------
def main():

	

	nouns = "/media/jedrzej/Seagate/Python/instagram-auto-hashtag/words/most_common_nouns.p"
	#nouns2 = "/media/jedrzej/Seagate/Python/instagram-auto-hashtag/words/nouns.p"
	adjectives = "/media/jedrzej/Seagate/Python/instagram-auto-hashtag/words/adjectives.p"

	verbs = "/media/jedrzej/Seagate/Python/instagram-auto-hashtag/words/verbs.p"
	prepositions = "/media/jedrzej/Seagate/Python/instagram-auto-hashtag/words/prepositions.p"
	adverbs = "/media/jedrzej/Seagate/Python/instagram-auto-hashtag/words/adverbs.p"

	l = pickle.load( open(verbs, "rb" ) )
	downloader = ImageDownloader("/media/jedrzej/Seagate/DATA/instagram_images/verbs/")
	downloader.go_through_list_of_tags(l, 50)
	'''
	l = pickle.load( open( adjectives, "rb" ) )
	print l
	random.shuffle(l)
	downloader = ImageDownloader("/media/jedrzej/Seagate/DATA/instagram_images/adjectives/")
	downloader.go_through_list_of_tags(l, 50)
	'''

	

	

if __name__ == "__main__":
    main()












