from flask import Flask, render_template
from app.api.auth import bp as auth_bp
from app.api.post import bp as post_bp
from app.api.user import bp as user_bp
from app.api.label import bp as label_bp
from app.api.comment import bp as comment_bp


app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)
app.register_blueprint(label_bp)
app.register_blueprint(comment_bp)


# Session secret key
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

POSTS = [
    {'title': 'Unbestarred Bandstand',
     'summary': 'Pariatur dolor deserunt veniam esse veniam consectetur sit est pariatur sed eu ullamco labore eu est est veniam cillum commodo magna sint minim do elit minim non proident dolore anim laboris pariatur ut ea. Hildegarde Besen',
     'author': 'Hermelinda Clarson',
     'date': '15/06/16',
     'tags': ['provisionless', 'acutifoliate'],
     'image': '0.jpg',
     'count': 1433},
    {'title': 'Grammaticize Foreigner',
     'summary': 'Pariatur do ut exercitation officia exercitation nostrud aliqua sed labore voluptate veniam sunt occaecat culpa officia velit sint excepteur deserunt ad sed veniam officia. Vena Petronzio',
     'author': 'Joie Decroo',
     'date': '11/04/11',
     'tags': ['onychomancy', 'quadded', 'Helicidae'],
     'image': '1.jpg',
     'count': 1340},
    {'title': 'Sizz Desight',
     'summary': 'Lorem ipsum sit deserunt dolor ad eiusmod cupidatat commodo magna do enim aliqua id deserunt nulla sed laborum dolor et in esse labore nostrud do velit occaecat consectetur dolore. Miss Kearsey',
     'author': 'Ona Baghdasarian',
     'date': '20/09/17',
     'tags': ['undercour', 'sphygmosc', 'amblypod'],
     'image': '2.jpg',
     'count': 972},
    {'title': 'Morphinist Deflectionization',
     'summary': 'Tempor quis ut minim eu officia aute dolore aute tempor dolore proident voluptate sed pariatur incididunt in ullamco dolore cillum. Phil Takacs',
     'author': 'Merlyn Nik',
     'date': '10/11/18',
     'tags': ['interfibrillar', 'foyer'],
     'image': '3.jpg',
     'count': 626},
    {'title': 'Periodontology Turner',
     'summary': 'Et anim id ea aliquip et id ullamco elit et sint adipisicing in labore culpa consequat sint laborum consectetur minim nisi deserunt in ut quis deserunt sint et ut in quis nulla magna. Chrissy Hipol',
     'author': 'Vi Nwachukwu',
     'date': '26/05/18',
     'tags': ['mongreliza', 'psoriasic', 'liturgiology'],
     'image': '4.jpg',
     'count': 936},
    {'title': 'Gamophyllous Glutoid',
     'summary': 'Lorem ipsum aliquip et adipisicing labore laboris cupidatat nulla ut enim sed fugiat culpa proident et non dolore dolor quis excepteur tempor in labore sit esse adipisicing veniam voluptate adipisicing aliquip aliqua voluptate in qui commodo tempor. Naida Viafara',
     'author': 'Linh Gianola',
     'date': '20/05/11',
     'tags': ['outlimb', 'ticul', 'plumber'],
     'image': '5.jpg',
     'count': 1923},
]

SUBJECTS = {
    'header': 'Yeni Eklenenler',
    'tags': ['Moldova', 'Qatar', 'Dominican Republic', 'Philippines', 'Benin', 'Slovenia']}

SUGGESTION_LIST = [
    {'image': '/static/11.jpg',
     'summary': 'Et anim id ea aliquip et',
     'tag': 'CSS'},
    {'image':  '/static/12.jpg',
     'summary': 'Lorem ipsum aliquip et ad',
     'tag': 'PYTHON'},
    {'image':  '/static/11.jpg',
     'summary': 'Et anim id ea aliquip et',
     'tag': 'JAVA'},
    {'image':  '/static/12.jpg',
     'summary': 'Lorem ipsum aliquip et ad',
     'tag': 'C++'},
    {'image':  '/static/11.jpg',
     'summary': 'Et anim id ea aliquip et',
     'tag': 'HTML'},
]


@app.route('/')
def index():
    return render_template(
        'index.html', posts=POSTS, subjects=SUBJECTS,
        sugestion_list=SUGGESTION_LIST)


@app.route('/login')
def login():
    return render_template('login.html')


# Decorator
@app.route('/singup')
def singup():
    return render_template('singup.html')
