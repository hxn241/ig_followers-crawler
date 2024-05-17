from instagrapi import Client
import time
import pandas as pd
import random
TARGET = 'pccomponentes'
ACCOUNT_USERNAME = ''
ACCOUNT_PASSWORD = ''
#ACCOUNT_USERNAME = ''
cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = cl.user_id_from_username(TARGET)
#followers = cl.user_followers_gql_chunk(user_id=user_id, max_amount=10)


def get_following(userid):
    following=cl.user_following(user_id=userid)
    return following


def get_followers(userid):
    count=0
    total_followers = []
    has_next = True
    cursor = None
    start_time = time.time()
    while has_next:
        try:
            followers = cl.user_followers_gql_chunk(user_id=user_id,max_amount=100,end_cursor=cursor)
            count += 1
            print(count)
            total_followers.extend(followers[0])
            cursor = followers[1]
            has_next = True if cursor is not None else False
            if not has_next and len(total_followers) < 2322:
                print("x")
            time.sleep(20)
        except Exception as e:
            print(f'exception: {e}')
            print(
                f"num requests: {count}\n"
                f"Total followers: {len(total_followers)}\n"
                f"Elapsed time: {(time.time()-start_time)/60:.2f}min"
            )
            time.sleep(3600)

    ids = [user.pk for user in total_followers]
    print(f'unique ids: {len(set(ids))}')
    end_time =  time.time()
    print(f'total execution time {(end_time-start_time)/60:.2f}min')


def sorteo_comentarios():
    my_file = open(r"G:\Mi unidad\pycharm-projects\ig_followers\data\hxn_followers.txt", "r")
    data = my_file.read()[:-1].split("\n")
    user_id = cl.user_id_from_username(TARGET)
    post_list = cl.user_medias(user_id, 10)
    post = post_list[2].id
    #followers = cl.user_followers(user_id)
    #followers = [v.username for k, v in followers.items()]
    ignore_list = ['anncaabaa', 'haff_rider', 'charliegarcia88']
    for username in data:
        if username in ignore_list:
            continue
        cl.media_comment(post, f'@{username}')
        time.sleep(random.randint(3,5))
    return print('Done!')

if __name__ == "__main__":
    # df = pd.read_excel(r"G:\Mi unidad\pycharm-projects\ig_followers\excel\creedfragrances_followers_20221026.xlsx")
    # usernames = list(set(df['username'].tolist()))
    # counter = 0
    #
    # user_followings = []
    # start_time = time.time()
    # for username in usernames:
    #     try:
    #         user_id = cl.user_id_from_username(username)
    #         following = get_following(user_id)
    #         user_followings.append({
    #             'user_id': user_id,
    #             'username': username,
    #             'followings': following
    #         })
    #         counter += len(following)
    #         if counter >= 10000:
    #             time.sleep(900-(time.time()-start_time))
    #     except Exception as e:
    #         print(e)
    #         print(f'username: {username}, counter: {counter}, elapsed time: {(time.time()-start_time)/60}min')
    # for user in user_followings:
    #     print(f'user{user.get("username")}, followings: {len(user.get("followings"))}')
    # print(user_followings)
    sorteo_comentarios()


# def sorteo_comentarios():
#     my_file = open(r"G:\Mi unidad\pycharm-projects\ig_followers\data\hxn_followers.txt", "r")
#     data = my_file.read()[:-1].split("\n")
#     user_id = cl.user_id_from_username(TARGET)
#     post_list = cl.user_medias(user_id, 10)
#     post = post_list[2].id
#     #followers = cl.user_followers(user_id)
#     #followers = [v.username for k, v in followers.items()]
#     for username in data:
#         cl.media_comment(post, f"@{username}")
#         time.sleep(random.randint(3,5))
#     return print('Done!')


# devuelve 10 ultimos posts con su id. post_list = cl.user_medias(user_id,10)
#post_list.id =  nos da el id para luego comentar
#cl.media_comment(post_id,"omg") # comentamos
#DA23VPz8G6HgbeT
# followers = cl.user_followers(user_id)
# followers = [v.username for k,v in followers.items()]
# iterar los followers y hacer los comentarios en el media
