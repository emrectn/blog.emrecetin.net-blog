import requests
import random

BASE_URL = 'http://localhost:5000/api'

dict = {'EMAIL0': 'emre@cetin.com',
        'EMAIL1': 'asd@cetin.com',
        'EMAIL2': 'xxx@cetin.com'
        }

token = {'token0': '0',
         'token1': '1',
         'token2': '2'}

password = {'password0': '123456',
            'password1': '123456',
            'password2': '123456'}

TITLES = ("Yeni Dünya", "Eğitimde Yenilikler", "Bitcoin Düştü", "Hello World")
TEXT = "counterborder resolvable chiotilla ingatherer wheer avodire wantage pelf underzeal stasidion oligometochic trotyl antivice gametoid afterhend leatherback arapunga Cimicifuga repellence Inoperculata evaporation encounterer dramaturge Iberic"
DATE = "2018-01-12 20:01:09.123132"

OLD_PASSWORD = '123456'
NEW_PASSWORD = 'degisti'
FULLNAME = 'Emre Çetin'
LABEL_ID = 2
YORUM = 'HARİKA YAPMIŞŞSINIZ ELİNİZE SAĞLIK'

NUM = 10


def create_user(email):
    print("CREATE_USER")
    r = requests.post(
        BASE_URL + '/user',
        json={'email': email,
              'password': OLD_PASSWORD,
              'fullname': FULLNAME})

    return print("{} \n".format(r.json()))


def delete_user(token):
    print("DELETE_USER")
    r = requests.delete(
        BASE_URL + '/user',
        headers={'X-Token': token})

    return print("{} \n".format(r.json()))


def change_password(token):
    print("CHANGE_PASSWORD")
    r = requests.put(
        BASE_URL + '/user',
        headers={'X-Token': token},
        json={'new_password': NEW_PASSWORD,
              'old_password': OLD_PASSWORD})

    return print("{} \n".format(r.json()))


def do_admin(username, token):
    print("DO_ADMIN")
    r = requests.put(
        BASE_URL + '/doadmin',
        json={'username': username,
              'token': token})
    return print("{} \n".format(r.json()))


def login(email, password):
    print("LOGIN")
    r = requests.post(
        BASE_URL + '/auth',
        json={'email': email,
              'password': password})

    return print("{} \n".format(r.json()))


def post_get(post_id):
    print("FIRST 3 POST GET\n")
    r = requests.get(
        BASE_URL + '/post?id=' + str(post_id))

    return print("{} \n".format(r.json()))


def post_get_all():
    print("ALL THE POST GET")
    r = requests.get(
        BASE_URL + '/posts')

    return print("{} \n".format(r.json()))


def post_create(token):
    print("POST CREATE")
    r = requests.post(
        BASE_URL + '/post',
        headers={'X-Token': token},
        json={'title': random.choice(TITLES),
              'text': TEXT,
              'date': DATE})
    return print("{} \n".format(r.json()))


def post_delete(token, post_id):
    print("FIRST 3 POST DELETE \n")
    r = requests.delete(
        BASE_URL + '/post?id=' + str(post_id),
        headers={'X-Token': token})

    return print("{} \n".format(r.json()))


def label_create(token, article_num):
    print("LABEL CREATE")
    r = requests.post(
        BASE_URL + '/label',
        headers={'X-Token': token},
        json={'labels': random.choice(TITLES),
              'post_id': article_num})

    return print("{} \n".format(r.json()))


def label_delete(token, label_id):
    print("LABEL DELETE")
    r = requests.delete(
        BASE_URL + '/label?label_id=' + str(label_id),
        headers={'X-Token': token})

    return print("{} \n".format(r.json()))


def comment_get_to_article(post_id):
    print("COMMENT GET TO ARTİCLE")
    r = requests.get(
        BASE_URL + '/comment?post_id=' + str(post_id))

    return print("{} \n".format(r.json()))


def comment_get_to_user(user_id):
    print("COMMENT GET TO USER")
    r = requests.get(
        BASE_URL + '/comments?user_id=' + str(user_id))

    return print("{} \n".format(r.json()))


def comment_create(token, post_id):
    print("COMMENT CREATE")
    r = requests.post(
        BASE_URL + '/comment?post_id=' + str(post_id),
        headers={'X-Token': token},
        json={'text': YORUM,
              'date': DATE})

    return print("{} \n".format(r.json()))


def comment_delete(token, comment_id):
    print("COMMENT DELETE")
    r = requests.delete(
        BASE_URL + '/comment?comment_id=' + str(comment_id),
        headers={'X-Token': token})

    return print("{} \n".format(r.json()))


def comment_publish(token, comment_id):
    print("COMMENT PUBLİSH")
    r = requests.put(
        BASE_URL + '/comment?comment_id=' + str(comment_id),
        headers={'X-Token': token})

    return print("{} \n".format(r.json()))

if __name__ == '__main__':

    for i in range(0, 3):
        create_user(dict['EMAIL'+str(i)])
        # delete_user(TOKEN)
        do_admin(dict['EMAIL' + str(i)], token['token' + str(i)])
    # change_password(token['token2'])
    # login(dict['EMAIL2'], password['password2'])

    # POST CREATE
    for i in range(0, 10):
        num = random.randint(0, 2)
        post_create(token['token' + str(num)])

    # POST GET
    for i in range(0, 3):
        post_get(i+1)

    # POST DELETE
    # for i in range(0, 3):
    #     num = random.randint(0, 2)
    #     post_delete(token['token' + str(num)], i+1)

    # POST GET ALL
    post_get_all()

    # LABEL CREATE
    for i in range(0, 10):
        token_num = random.randint(0, 2)
        article_num = random.randint(1, 10)
        label_create(token['token' + str(token_num)], article_num)

    # LABEL DELETE
    token_num = random.randint(0, 2)
    label_delete(token['token' + str(token_num)], LABEL_ID)

    # COMMENT CREATE
    for i in range(0, 15):
        article_num = random.randint(1, 10)
        token_num = random.randint(0, 2)
        comment_create(token['token' + str(token_num)], article_num)

    # # COMMENT GET TO ARTİCLE
    POST_ID = 4
    comment_get_to_article(POST_ID)

    # COMMENT DELETE
    # COMMENT_ID = 4
    # comment_delete(token['token0'], COMMENT_ID)

    # COMMENT PUBLİSH
    COMMENT_ID = 4
    comment_publish(token['token0'], COMMENT_ID)

    # COMMENT GET TO USER
    USER_ID = 1
    comment_get_to_user(USER_ID)
