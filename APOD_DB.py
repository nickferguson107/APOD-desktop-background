import urllib.request
import datetime
import time
import os
import ctypes
import sched
from bs4 import BeautifulSoup

def get_image(url):  

    url = "http://apod.nasa.gov/"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    img = soup.find("img")
    apod_img_name = str(img['src'])
    apod_img_link = url + apod_img_name
    apod_img_title = str(soup.find('b'))
    today_name = apod_img_title[4:-5]

    if ":" in today_name:
        today_name = today_name.replace(":", " -", 1)

    image_to_save = urllib.request.urlopen(apod_img_link).read()

    return today_name, image_to_save

def save_image(name, image):

    home_dir = os.path.expanduser('~')
    today_date = str(datetime.date.today())
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

    return normed_path_with_img, today_date

def main(url):

    try:
        today_name, image = get_image(url)
        print("Today's image is of '{}'.".format(today_name))
        image_path, _ = save_image(today_name, image)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 0)
        print("Image set as background.")
    except TypeError:
        print("Update failed - APOD item is video. Waiting 1 hour to update.")
        time.sleep(3600)

    return today_name

if __name__ == '__main__':

    url = "http://apod.nasa.gov/"
    today_name = main(url)

    while 1:
        current_time = datetime.datetime.now()
        formatted_time = datetime.datetime.strftime(current_time, "%H:%M:%S")
        print("The current time is {}".format(str(formatted_time)))
        next_name, _ = get_image(url)
        if next_name == today_name:
            print("APOD image not changed from last check.")
            print("Waiting 10 minutes for next check.")
            time.sleep(600)
        else:
            print("Updating at {}".format(str(formatted_time)))
            main(url)
            time.sleep(43200)
            print("Waiting 12 hours before next check.")
