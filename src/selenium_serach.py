from pprint import pprint
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import re

options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument('--disable-gpu')

#Get watch party movie name
def get_name(url,id,password):
    login_url = "https://tinyurl.com/y7rhjdzm"
    driver = webdriver.Chrome(options=options)
    driver.get(login_url)

    driver.find_element(By.ID, "ap_email").send_keys(id)
    driver.find_element(By.ID, "continue-announce").submit()

    sleep(3)

    driver.find_element(By.ID, "ap_password").send_keys(password)
    driver.find_element(By.ID, "signInSubmit").submit()

    driver.get(url)
    driver.get(url)
    sleep(3)

    origin_text = driver.find_element(By.CLASS_NAME, "_36RzrH").text
    origin_movie_name = origin_text.splitlines()

    driver.quit()

    return delete_symbol(origin_movie_name[1])

#Pull filmarks's data
def search_title(url,driver,title):

    #Search titles
    driver.get(url)
    pprint(title)
    titles = driver.find_elements(By.CLASS_NAME, "p-content-cassette__title")

    for index in range(len(titles)):
        pprint(titles[index].text)
        if titles[index].text in title:
            sleep(2)

            #Go movie page
            titles[index].click()
            sleep(2)

            #No Synopsis
            try: 
                if driver.find_element(By.CLASS_NAME, "p-content-detail__synopsis-desc").text:
                    print("ok")
            except:
                return [driver.current_url]

            #OK Synopsis
            return [driver.current_url, driver.find_element(By.CLASS_NAME, "p-content-detail__synopsis-desc").text]
            
    return

#Go filmarks links
def get_info(title):
    driver = webdriver.Chrome(options=options)
    genre_list = ["movies","dramas","animes"]

    for genre in genre_list:
        result = search_title("https://filmarks.com/search/" + genre + "?q=" + title,driver,title)
        if None != result:
            result.insert(0, genre)
            result.insert(0, title)
            return result

    driver.quit()

#delete symbol
def delete_symbol(name):
    if "(字幕版)" in name:
        new_name = re.sub(r"[(字幕版)]", "", name)
        return new_name
    elif "(吹替版)" in name:
        new_name = re.sub(r"[(吹替版)]", "", name)
        return new_name
    else:
        return name