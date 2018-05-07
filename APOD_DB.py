import urllib.request
import datetime
import time
import os
import ctypes
import sched
from bs4 import BeautifulSoup

def get_image():  
    url = "http://apod.nasa.gov/"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    img = soup.find("img")
    apod_img_name = str(img['src'])
    apod_img_link = url + apod_img_name
    apod_img_title = str(soup.find('b'))
    today_name = apod_img_title[4:-5]
    image_to_save = urllib.request.urlopen(apod_img_link).read()
    return today_name, image_to_save

def save_image(name, image):
    home_dir = os.path.expanduser('~')
    filename = today_date + " " + name + ".jpg"
    save_path = os.path.join(home_dir, "Pictures", "APOD Photos")
    save_path_with_img = os.path.join(save_path, filename)
    normed_path = os.path.normpath(save_path)
    normed_path_with_img = os.path.normpath(save_path_with_img)
    if not os.path.exists(normed_path):
        os.makedirs(normed_path)
    with open(normed_path_with_img, 'wb',) as f:
        f.write(image)
    f.close()
    return normed_path_with_img

def job(today_date, save_name, image, image_path):
    today_date = str(datetime.date.today())
    save_name, image = get_image()
    image_path = save_image(save_name, image)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 0)

time_now = datetime.datetime.now()
time_until_6am = ((30-time_now.hour-1)*3600)+((60-time_now.minute-1)*60)+(60-time_now.second)
s = sched.scheduler(time_now, time.sleep(time_until_6am))

today_date = str(datetime.date.today())
save_name, image = get_image()
image_path = save_image(save_name, image)
ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 0)

s.enter(time_until_6am, 1, job, argument=(today_date, save_name, image, image_path))

while True:
    run_forever = sched.scheduler(time.time, time.sleep(3600))