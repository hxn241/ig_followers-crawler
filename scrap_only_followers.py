import os
import pickle
import random
import datetime as dt
import math
import time

import pandas as pd
from fake_useragent import UserAgent
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as ChromeDriverManager


def scrap_followers(driver, count):
    followers = []
    try:
        fBody = driver.find_element_by_xpath("//div[@class='_aano']")
        scroll = 0
        run = True
        while run == True:
            last_iter_elems = len(elems) if scroll > 0 else 0
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + 5000;', fBody)
            # time.sleep(random.randint(3, 6))
            print(f'iteration nº {scroll}')
            elems = list(set(driver.find_elements_by_xpath("//*[@aria-labelledby]")))
            num_elems = len(elems)
            followers.extend([(",".join(elem.text.split('\n'))) for elem in elems])
            print(f'distinct followers: {len(set(followers))} from total: {count}')
            scroll += 1
            if num_elems == last_iter_elems:
                run = False
    except Exception as e:
        print(e)
    finally:
        followers = list(set(followers))
        driver.quit()
        return followers


def followers_to_xls(followers_list, target):
    followers_list = [follower.split(",")[:2] for follower in followers_list]
    df = pd.DataFrame(followers_list, columns = ['id', 'name'])
    df.to_excel(f'data/{target}_followers_{dt.datetime.now():%Y%m%d}.xlsx', index=False)
    print('Followers file created')


def open_browser_session(headless, url='https://www.instagram.com'):
    chrome_options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    # chrome_options.add_argument(f'user-agent={userAgent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--log-level=3")
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(),
        options=chrome_options
    )
    driver.maximize_window()
    driver.get(url)
    # time.sleep(random.randrange(10, 12))
    return driver


def accept_notifications(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//div//*[contains(text(),"Ahora no")]'))
        ).click()
    except:
        pass


def login_instagram(driver, username, password):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//div//*[contains(text(),"solo cookies necesarias")]'))
        ).click()
        #driver.find_element(By.XPATH, '//div//*[contains(text(),"solo cookies necesarias")]').click()
        username_input = driver.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)
        # time.sleep(random.randrange(5, 8))
        pss_input = driver.find_element_by_name('password')
        pss_input.clear()
        pss_input.send_keys(password)
        time.sleep(random.randrange(1, 2))
        pss_input.send_keys(Keys.RETURN)
        time.sleep(random.randrange(8, 10))
        pickle.dump(driver.get_cookies(),open("data/cookies.pkl","wb"))
        print(f'[{username}] Successfully logged on!')
    except Exception as e:
        print(f'[{username}] Authorization fail \n error:{e}')
    accept_notifications(driver)
    accept_notifications(driver)


def go_to_user_profile(driver, target):
    driver.get(f"https://www.instagram.com/{target}")
    # time.sleep(random.randrange(5, 7))
    count = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f'//*[contains(@href,"/{target}/followers/")]/div/span'))).get_attribute('title')
    count = int("".join(count.split(",")))
    driver.find_element(By.XPATH, '//*[contains(text(),"seguidores")]').click()
    # time.sleep(random.randrange(5, 7))
    return count