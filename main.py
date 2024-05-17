from scrap_only_followers import open_browser_session, login_instagram, go_to_user_profile, followers_to_xls, \
    scrap_followers
from scrap_followers_data import user_profile_test, scraping_target, followers_data_to_xls
import time
import pyautogui as pg
import pickle
import random

USERNAME =''
PASSWORD = ''
TARGET = 'lartissanparfamour'


def getting_followers():
    driver = open_browser_session(headless=True)
    login_instagram(driver, USERNAME, PASSWORD)
    count = go_to_user_profile(driver, TARGET)
    followers = scrap_followers(driver, count)
    followers_to_xls(followers, target=TARGET)


def retreive_followers_info():
    driver = open_browser_session(headless=True)
    login_instagram(driver, USERNAME, PASSWORD)
    count = user_profile_test(driver, TARGET)
    followers = scraping_target(driver, count)
    followers_data_to_xls(followers, target=TARGET)


def cookie_login(driver,url):
    try:
        cookies = pickle.load(open("data/cookies.pkl","rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(url)
    except Exception as e:
        print(e)

def generate_post():
    followers = user_list()
    from selenium.webdriver.common.keys import Keys
    driver = open_browser_session(headless=False)
    # login_instagram(driver, USERNAME, PASSWORD)
    cookie_login(driver,url='https://www.instagram.com/p/Cl3pe8YoJaK')
    #driver.get('https://www.instagram.com/p/Cl3pe8YoJaK')
    time.sleep(10)
    element = driver.find_element_by_xpath('//*[contains(@aria-label,"Añade un comentario")]')

    ignore_list = ['anncaabaa', 'haff_rider', 'charliegarcia88']
    for username in followers:
        if username in ignore_list:
            continue
        time.sleep(2)
        element.clear()
        element.click()
        time.sleep(1)
        pg.hotkey('altright','2')
        pg.write(username)
        pg.press('enter')
        time.sleep(random.randint(60,140))
        print(f'{username} mention done!')
    return print('mention done!')


def user_list():
    my_file = open(r"G:\Mi unidad\pycharm-projects\ig_followers\data\hxn_followers.txt", "r")
    data = my_file.read()[:-1].split("\n")
    return data
if __name__ == "__main__":
    generate_post()
    #getting_followers()
    # retreive_followers_info()