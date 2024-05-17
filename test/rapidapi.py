import time
import json
import requests
import pandas as pd

API_KEYS = [""]
url = "https://instagram-bulk-profile-scrapper.p.rapidapi.com/clients/api/ig/followers"


def get_api_key(key_dict):
    max_value = max(list(key_dict.values()))
    api_key = list(key_dict.keys())[list(key_dict.values()).index(max_value)]
    return api_key


def load_requests():
    with open('../remainin_requests.txt', 'r') as f:
        data = f.read()
    aux_dict = json.loads(data)
    return aux_dict

aux_dict = load_requests()
api_key = get_api_key(aux_dict)
# api_key = '3cda8e7f53msh10f9c9ed2579306p156521jsn3adb6c67c83b'
has_next = True
total_followers = []
next_cursor = None
count = 0
retry = False
followers = []
target_account = 'aurianenatura'
while has_next:
    try:
        # api_key = get_api_key(aux_dict)
        count += 1
        #querystring = {"username":"mario_carrillo12","corsEnabled":"false",'nextMaxId':next_cursor}
        querystring = {"ig":target_account,'nextMaxId':next_cursor}
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "instagram-bulk-profile-scrapper.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.ok:
            result = response.json()
            if result.get("cursor") != "":  ####
                total_followers.extend(result.get("data"))
                cursor = result.get("cursor", {})
                if cursor.get("moreAvailable", False):
                    if retry == True:
                        next_cursor = old_cursor
                        has_next = True
                    else:
                        next_cursor = cursor.get("nextMaxId")
                        has_next = True
                else:
                    has_next = False
                retry=False
            else:
                retry=True
                old_cursor = next_cursor
        remaining_requests = response.headers.get("X-RateLimit-Request-Remaining")
        if remaining_requests == '0':
            aux_dict[api_key] = 0
            api_key = get_api_key(aux_dict)
        else:
            aux_dict[api_key] = int(remaining_requests)
        print(f'Remaining requests: {remaining_requests}, api_key :{api_key}')
        time.sleep(10)
    except Exception as e:
        print(e)
with open('../remainin_requests.txt', 'w') as f:
    f.writelines(json.dumps(aux_dict))

followers.extend([item.get("username") for item in total_followers])
followers = set(followers)
with open("G:/Mi unidad/pycharm-projects/ig_followers/data/" + target_account + ".txt", 'w') as follow:
    follow.write("\n".join(map(lambda x: str(x), followers)))
ig_data = pd.DataFrame().from_records([item for item in total_followers])
ig_data.drop_duplicates(subset=['pk'],inplace=True)
ig_data.to_excel(f"data/{target_account}.xlsx",index=False)
# file = open("G:/Mi unidad/pycharm-projects/ig_followers/data/" + target_account + ".txt", 'w')
# file.write("\n".join(map(lambda x: str(x), followers)))
# file.close()


