import re
import random
from dataclasses import dataclass, field
import time
import pandas as pd
import datetime as dt
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrap_only_followers import open_browser_session, login_instagram, go_to_user_profile

# USERNAME = ''
USERNAME = ''
# PASSWORD = ''
PASSWORD = ''
# TARGET = ''
TARGET = ''

TARGET_FOLLOWERS = 5000
INFLUENCER_MIN_FOLLOWERS = 5000


@dataclass
class User:
    username: str
    name: str
    is_private: bool
    followers: int
    following: int
    posts: int
    is_influencer: bool = field(init=False)

    def check_if_influencer(self):
        if self.followers > INFLUENCER_MIN_FOLLOWERS:
            return True
        return False

    def __post_init__(self):
        self.is_influencer: bool = self.check_if_influencer()


def extract_numeric_value(obj):
    try:
        return int(re.search("\\d+", obj).group(0))
    except:
        return 0


def check_is_private(driver):
    try:
        isprivate = driver.find_element(By.XPATH,'//*[contains(text(),"privada")]')
        return True
    except:
        return False


def user_profile_test(driver, target):
    driver.get(f"https://www.instagram.com/{target}")
    # time.sleep(random.randrange(5, 7))
    count = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f'//*[contains(@href,"/{target}/followers/")]/div/span'))).get_attribute('title')
    count = int("".join(count.split(",")))
    driver.find_element(By.XPATH, '//*[contains(text(),"seguidores")]').click()
    time.sleep(random.randrange(5, 7))
    return count


def extract_fields(driver, xpath):
    try:
        field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))).text
            # EC.visibility_of_element_located((By.XPATH, xpath))).text original
        return field
    except:
        return None


def get_user_data(user_elems, parsed_users):
    followers = []
    action = ActionChains(driver)
    for ig_user in user_elems:
        try:
            username = ig_user.text.split("\n")[0]
            if not any([True for user in parsed_users if user.username == username]):
                name = ig_user.text.split("\n")[1]
                pop_up = ig_user.find_element(By.XPATH, f"//*[contains(text(),'{username}')]")
                # action.move_to_element(
                #     ig_user.find_element(By.XPATH, "//*[@aria-labelledby]//div/a[contains(@role,'link')]")).perform()
                action.move_to_element(pop_up).perform()
                # time.sleep(random.randint(2, 3))

                seguidos = extract_fields(driver, xpath='//div[contains(@style,"390")]//*[contains(text(),"seguido") or contains(text(),"seguidos")]') #//*[contains(text(),"seguido") or contains(text(),"seguidos")]
                seguidores = extract_fields(driver, xpath='//div[contains(@style,"390")]//*[contains(text(),"seguidor") or contains(text(),"seguidores")]')#//*[contains(text(),"seguidor") or contains(text(),"seguidores")]
                publicaciones = extract_fields(driver, xpath='//div[contains(@style,"390")]//*[contains(text(),"publicaci")]')

                user_ig = User(
                    username=username,
                    name=name,
                    followers=extract_numeric_value(seguidores),
                    following=extract_numeric_value(seguidos),
                    posts=extract_numeric_value(publicaciones),
                    is_private=check_is_private(driver)
                )
                # action.move_by_offset(-600, 0).perform()
                action.move_to_element(driver.find_element(By.XPATH, '//*[contains(text(),"Seguidores")]')).perform()
                followers.append(user_ig)
        except Exception as e:
            print(e)
    return followers


def scraping_target(driver, count):
    # action = ActionChains(driver)
    followers = []
    try:
        fBody = driver.find_element_by_xpath("//div[@class='_aano']")
        scroll = 0
        run = True
        elems = []
        while run:
            last_iter_elems = len(elems) if scroll > 0 else 0
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + 5000;', fBody)
            elems = driver.find_elements_by_xpath("//*[@aria-labelledby]")
            num_elems = len(elems)
            new_followers = get_user_data(elems, followers)
            followers.extend(new_followers)
            # driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + 5000;', fBody)
            # time.sleep(random.randint(3, 6))
            print(f'iteration nº {scroll}')
            print(f'distinct followers: {len(followers)} from total: {count}')
            scroll += 1
            valid_followers = sum(
                [1 for user in followers if not user.is_private and user.followers < INFLUENCER_MIN_FOLLOWERS]
            )
            if num_elems == last_iter_elems or valid_followers >= TARGET_FOLLOWERS:
                run = False
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        return followers


def followers_data_to_xls(followers_list, target):
    followers_dict = [vars(x) for x in followers_list]
    pd.DataFrame(followers_dict).to_excel(f'data/{target}_followers_{dt.datetime.now():%Y%m%d}.xlsx', index=False)
    print('Followers file created')


if __name__ == "__main__":
    driver = open_browser_session(headless=True)
    login_instagram(driver, USERNAME, PASSWORD)
    count = user_profile_test(driver,TARGET)
    # count = go_to_user_profile(driver, TARGET)
    followers = scraping_target(driver, count)
    followers_data_to_xls(followers, target=TARGET)
