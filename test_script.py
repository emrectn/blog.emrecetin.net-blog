import requests
import random
from faker import Faker
from itertools import cycle
BASE_URL = 'http://localhost:5000/api'

f = Faker()


IMAGES = cycle([
    '/static/0.jpg',
    '/static/1.jpg',
    '/static/2.jpg',
    '/static/3.jpg',
    '/static/4.jpg',
    '/static/5.jpg',
    '/static/11.jpg',
    '/static/12.jpg',
])

USER_COUNT = 4
POST_COUNT = 11
COMMENT_COUNT = 20


def generate_user():
    return {'fullname': f.name(),
            'email': f.safe_email(),
            'password': f.password(),
            'token': f.password(32)}


def generate_post():
    title = f.text(16).split(".")[0]
    title[0].upper()
    title[-1].upper()
    return {'title': title,
            'text': '\n'.join(f.paragraphs(3)),
            'image': next(IMAGES),
            'date': f.date_time().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'seen': f.random_int(0, 999),
            'likes': f.random_int(0, 999)}


def generate_tag(post_id):
    text = f.text(7).split(".")[0]
    text.upper()
    return {'tags': text,
            'post_id': post_id}


def generate_comment():
    return {'text': f.text(50),
            'date': f.date_time().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'post_id': f.random_int(0, POST_COUNT-1)}


def create_user(user):
    r = requests.post(
        BASE_URL + '/user',
        json={'email': user['email'],
              'password': user['password'],
              'fullname': user['fullname']})

    print("{} \n".format(r.json()))
    return


def delete_user(token):
    print("DELETE_USER")
    r = requests.delete(
        BASE_URL + '/user',
        headers={'X-Token': token})

    print("{} \n".format(r.json()))
    return


def change_password(token, user):
    print("CHANGE_PASSWORD")
    r = requests.put(
        BASE_URL + '/user',
        headers={'X-Token': token},
        json={'new_password': f.password(),
              'old_password': user['password']})

    print("{} \n".format(r.json()))
    return


def make_admin(username, token):
    print("MAKE_ADMIN")
    r = requests.put(
        BASE_URL + '/makeadmin',
        json={'username': username,
              'token': token})

    print("{} \n".format(r.json()))
    return


def login(email, password):
    r = requests.post(
        BASE_URL + '/auth',
        json={'email': email,
              'password': password})

    return r.json().get('data')


def post_get(post_id):
    r = requests.get(
        BASE_URL + '/post?id=' + str(post_id))

    print("{} \n".format(r.json()))
    return


def post_get_all():
    print("ALL THE POST GET")
    r = requests.get(
        BASE_URL + '/posts')

    print("{} \n".format(r.json()))
    return


def post_create(token, post):
    print("POST CREATE")
    print(post['title'])
    r = requests.post(
        BASE_URL + '/post',
        headers={'X-Token': token},
        json={'title': post['title'],
              'text': post['text'],
              'date': post['date'],
              'image': post['image'],
              'seen': post['seen'],
              'likes': post['likes']})

    print("{} \n".format(r.json()))
    return


def post_delete(token, post_id):
    print("FIRST 3 POST DELETE \n")
    r = requests.delete(
        BASE_URL + '/post?id=' + str(post_id),
        headers={'X-Token': token})

    print("{} \n".format(r.json()))
    return


def tag_create(token, tag):
    print("TAG CREATE")
    r = requests.post(
        BASE_URL + '/tag',
        headers={'X-Token': token},
        json={'tags': tag['tags'],
              'post_id': tag['post_id']})

    print("{} \n".format(r.json()))
    return


def tag_delete(token, tag_id):
    print("TAG DELETE")
    r = requests.delete(
        BASE_URL + '/tag?tag_id=' + str(tag_id),
        headers={'X-Token': token})

    print("{} \n".format(r.json()))
    return


def comment_get_to_article(post_id):
    print("COMMENT GET TO ARTİCLE")
    r = requests.get(
        BASE_URL + '/comment?post_id=' + str(post_id))

    print("{} \n".format(r.json()))
    return


def comment_get_to_user(user_id):
    print("COMMENT GET TO USER")
    r = requests.get(
        BASE_URL + '/comments?user_id=' + str(user_id))

    print("{} \n".format(r.json()))
    return


def comment_create(token, comment):
    print("COMMENT CREATE")
    r = requests.post(
        BASE_URL + '/comment?post_id=' + str(comment['post_id']),
        headers={'X-Token': token},
        json={'text': comment['text'],
              'date': comment['date']})

    print("{} \n".format(r.json()))
    return


def comment_delete(token, comment_id):
    print("COMMENT DELETE")
    r = requests.delete(
        BASE_URL + '/comment?comment_id=' + str(comment_id),
        headers={'X-Token': token})

    print("{} \n".format(r.json()))
    return


def comment_publish(token, comment_id):
    print("COMMENT PUBLİSH")
    r = requests.put(
        BASE_URL + '/comment?comment_id=' + str(comment_id),
        headers={'X-Token': token})

    print("{} \n".format(r.json()))
    return

if __name__ == '__main__':
    # CREATE USER
    users = [generate_user() for _ in range(USER_COUNT)]
    for u in users:
        print('USER CREATE : {}'.format(u['fullname']))
        create_user(u)

    # MAKE ADMIN
    for u in users:
        make_admin(u['email'], u['token'])

    # LOG IN
    for u in users:
        login_result = login(u['email'], u['password'])
        if login_result:
            print('USER LOGIN : {}\n'.format(u['email']))
            u['token'] = login_result
        else:
            print('USER NOT LOGIN : {}'.format(u['email']))

    # CHANGE PASSWORD
    for u in users:
        change_password(u['token'], u)

    # DELETE USER
    # u = users[-1]
    # print(u)
    # delete_user(u['token'])

    # POST CREATE
    posts = [generate_post() for _ in range(POST_COUNT)]
    for p in posts:
        post_create(random.choice(users)['token'], p)

    # POST GET
    for i in range(3):
        post_get(i+1)

    # POST GET ALL
    post_get_all()

    # POST DELETE
    # post_delete(random.choice(users)['token'], POST_COUNT)
    # os.system("rm storage.db")

    # TAG CREATE
    POST_NUMBER = len(posts)
    tags = [generate_tag(i+1) for i in range(POST_NUMBER-1)]
    for tag in tags:
        tag_create(random.choice(users)['token'], tag)

    tags = [generate_tag(i+1) for i in range(POST_NUMBER-1)]
    for tag in tags:
        tag_create(random.choice(users)['token'], tag)

    # TAG DELETE
    # tag_delete(random.choice(users)['token'], len(tags))

    # COMMENT CREATE
    comments = [generate_comment() for _ in range(COMMENT_COUNT)]
    for comment in comments:
        comment_create(random.choice(users)['token'], comment)

    # COMMENT GET TO ARTICLE
    comment_get_to_article(posts.index(random.choice(posts)) + 1)

    # COMMENT GET TO USER
    comment_get_to_user(users.index(random.choice(users)) + 1)

    # COMMENT DELETE
    # comment_delete(random.choice(users)['token'], comments.index(random.choice(comments)) + 1)

    # COMMENT PUBLISH
    for i in range(5):
        try:
            index = comments.index(random.choice(comments)) + 1
            comment_publish(random.choice(users)['token'], index)
        except None-Type:
            print("Böyle bir post bulunamadi : {}".format(index))
            pass

