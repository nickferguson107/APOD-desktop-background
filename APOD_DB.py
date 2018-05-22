import urllib.request
import datetime
import time
import os
import ctypes
import sched
from bs4 import BeautifulSoup

class DesktopBackground:

    def get_image(self):  
        self.url = "http://apod.nasa.gov/"
        self.page = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.img = self.soup.find("img")
        self.apod_img_name = str(self.img['src'])
        self.apod_img_link = self.url + self.apod_img_name
        self.apod_img_title = str(self.soup.find('b'))
        self.today_name = self.apod_img_title[4:-5]
        if ":" in self.today_name:
            self.today_name = self.today_name.replace(":", " -", 1)
        self.image_to_save = urllib.request.urlopen(self.apod_img_link).read()
        return self.today_name, self.image_to_save

    def save_image(self, name, image):
        self.home_dir = os.path.expanduser('~')
        self.today_date = str(datetime.date.today())
        self.filename = self.today_date + " " + name + ".jpg"
        self.save_path = os.path.join(self.home_dir, "Pictures", "APOD Photos")
        self.save_path_with_img = os.path.join(self.save_path, self.filename)
        self.normed_path = os.path.normpath(self.save_path)
        self.normed_path_with_img = os.path.normpath(self.save_path_with_img)
        if not os.path.exists(self.normed_path):
            os.makedirs(self.normed_path)
        with open(self.normed_path_with_img, 'wb',) as f:
            f.write(image)
        f.close()
        return self.normed_path_with_img, self.today_date

    def job(self):
        self.save_name, self.image = self.get_image()
        image_path = self.save_image(save_name, image)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 0)
        return

set_background = DesktopBackground()

print("Updating...")
try:
    today_name, image = set_background.get_image()
    print("Today's image is of '{}'.".format(today_name))
    image_path, today_date = set_background.save_image(today_name, image)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 0)
    print("Image set as background.")
except TypeError:
    print("Update failed - APOD item is video. Waiting 1 hour to update.")
    time.sleep(3600)

while True:
    current_time = datetime.datetime.now()
    formatted_time = datetime.datetime.strftime(current_time, "%H:%M:%S")
    print("The current time is {}".format(str(formatted_time)))
    try:
        next_day_name, _ = set_background.get_image()
        if next_day_name == today_name:
            print("APOD image not changed from last check.")
            print("Waiting 10 minutes for next check.")
            time.sleep(600)
        else:
            print("Updating at {}".format(str(formatted_time)))
            set_background.job()
            time.sleep(43200)
            print("Waiting 12 hours before next check.")
    except TypeError:
        print("Update failed - APOD item is video. Waiting 1 hour to update.")
        time.sleep(3600)