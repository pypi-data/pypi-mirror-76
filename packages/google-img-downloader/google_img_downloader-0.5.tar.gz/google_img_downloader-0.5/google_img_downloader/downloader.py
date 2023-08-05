# Built-in import
import os
import sys
import enum
import time
import base64

# Third-party import
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request, urllib.error, urllib.parse

from PIL import Image
from io import BytesIO


class ImageQuality(enum.Enum):
    default = ""
    large = "tbs=isz%3Al"
    medium = "tbs=isz%3Am"
    icon = "tbs=isz%3Ai"

class Downloader:
    def __init__(self,query):

        self.headers = {} # header needed on fetching images url request
        self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

        self.query = query # Query search
        self.quality = ""

        self.folder_path = "downloaded/%s/"%(self.query.replace(" ","_")) # Master saving folder
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        
        self.sleep_time = 0.25 # Sleeping time
        self.number_of_request = 5 # Default number of request after end scrolling reach
        self.number_of_scrolls = self.number_of_request / 250 + 1 # Total number of scrolling

        self.supported_extensions = ["jpg", "jpeg", "png", "gif"] # Supported format
        self.img_count = 0 # Total number of images found
        self.downloaded_img_count = 0 # Total number of images downloaded

    def set_query(self,query):
        self.query = query

    def set_folder_path(self,path):
        self.folder_path = path

    def set_quality(self,quality):
        self.quality = quality.value

    def set_sleep_time(self,time):
        self.sleep_time = time

    def get_url(self):
        return "https://www.google.co.in/search?q=%s&tbm=isch&%s"%(self.query,self.quality)

    def set_number_of_request(self,number):
        self.number_of_request = number
        self.number_of_scrolls = self.number_of_request / 200 + 1 # Default is 400

    def get_web_driver(self):
        driver = None
        browser = ["Chrome","Firefox","Safari"]
        for i in browser:
            try:
                if i == "Chrome": driver = webdriver.Chrome()
                if i == "Firefox": driver = webdriver.Firefox()
                if i == "Safari": driver = webdriver.Safari()
                break
            except expression as e:
                print("Webdriver failed to open")
        return driver

    def __prepare_driver(self):
        self.driver = self.get_web_driver()
        self.driver.get(self.get_url()) 
        print("Session ID : ", self.driver.session_id)

    def __prepare_page(self):
        for _ in range(int(self.number_of_scrolls)):
            for __ in range(10):
                # multiple scrolls needed to show all 400 images
                self.driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(self.sleep_time) # Sleep while loading images
            time.sleep(self.sleep_time*2) # Sleep while loading next page
            try:
                self.driver.find_element_by_xpath("//input[@value='Show more results']").click()
            except Exception as e:
                print("Less images found:", e)
                break

    def __fetch_images(self):
        self.img_count = 0
        self.downloaded_img_count = 0

        images = self.driver.find_elements_by_xpath('//img[contains(@class,"rg_i")]')
        print("Total images found:", len(images), "\n")

        for image in images:
            self.img_count += 1
            img_url = image.get_attribute('src')
            print("Downloading image ID : ", self.img_count)
            self.downloaded_img_count += 1
            try:
                if img_url[0:4] == "data":
                    format = img_url.split(",")[0]
                    format = format.split("/")[1]
                    format = format.split(";")[0]
                    imgdata = base64.decodebytes(bytes(img_url.split(",")[1],"utf-8"))
                    filename = self.folder_path+str(self.downloaded_img_count)+"."+format
                    with open(filename, 'wb') as f:
                        f.write(imgdata)
                else:
                    format = img_url.split(".")
                    format = format[len(format)-1]
                    if format not in self.supported_extensions:
                        format = "jpg"
                    req = urllib.request.Request(img_url, headers=self.headers)
                    raw_img = urllib.request.urlopen(req).read()
                    file_name = self.folder_path+self.query+"_"+str(self.img_count)+"."+str(format)
                    file_name = file_name.replace(" ","_")
                    with open(filename, 'wb') as f:
                        f.write(raw_img)
            except Exception as e:
                print("Downloading image ID : ", self.img_count, " Failed")
                print(e)
            if self.downloaded_img_count >= self.number_of_request:
                break
        print("Total downloaded: ", self.downloaded_img_count, "/", self.img_count)
        self.driver.quit()

    def start(self):
        try:
            self.__prepare_driver() # Prepare the driver and open the browser
            self.__prepare_page() # Load pages and scrool till the "number_of_scrools"
            self.__fetch_images() # Fetch and download the image(s) in specific format
        except Exception as e:
            print("Download failed because of ",e)