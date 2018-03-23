Vue.component('suggestion', {
    props: ['suggestion_data'],
    template : '<div class="panel panel-default clearfix shadow"> \
        <div class="view overlay"> \
            <img class="post-image" :src="suggestion_data.image"> \
            <div class="mask"> \
                <p v-if="suggestion_data.tags.length>0">{{suggestion_data.tags[0].toUpperCase()}}</p> \
            </div> \
        </div> \
        <div class="panel-footer header-color"> {{suggestion_data.title}}</div> \
    </div>',
});

Vue.component('post', {
    props: ['post_data'],
    template : '\
               <div class="panel panel-default clearfix polaroid">\
        <div class="crop">\
            <img class="post-image" :src="post_data.image">\
        </div>\
        <div class="panel-heading clearfix">\
            <span class="title col-md-6 col-xs-12" style="padding: 0px;">{{ post_data.title }}</span>\
            <span class="col-md-6 col-xs-12">\
                <div v-for="t in post_data.tags" >\
                <span class="semitransparent label label-warning tag">{{t}}</span>\
                </div>\
            </span>\
        </div>\
        <div class="panel-body">\
            {{ post_data.text }}\
            <hr>\
            <span class="col-md-3 col-sm-4 col-xs-5 semitransparent indicator">\
                <span class="glyphicon glyphicon-time"></span>\
                <span>&nbsp;{{ post_data.date.split(\' \')[0] }}</span>\
            </span>\
            <span class="col-md-3 col-sm-4 col-xs-4 semitransparent indicator">\
                <span class="glyphicon glyphicon-eye-open"></span>\
                <span>&nbsp;{{ post_data.seen }}</span>\
            </span>\
            <span class="col-md-3 col-sm-4 col-xs-3 semitransparent indicator">\
                <span class="glyphicon glyphicon-heart"></span>\
                <span>&nbsp;{{ post_data.likes }}</span>\
            </span>\
            <button type="button" class="btn btn-primary button col-md-3 col-xs-12 ">Devam</button>\
        </div>\
    </div>',
});

Vue.component('tag',{
    props: ['tag_data'],
    template: '<span class="semitransparent label label-warning tag">{{ tag_data }}</span>',
});


app = new Vue({
    'el': '#app',
    'data': {
        'selected': 'article',
        'posts': [],
        'suggestion_list': []
    },
    'created': function () {
        this.fetch_posts();
        this.fetch_popular();
    },
    'methods': {
        'fetch_posts': function() {
            let x = new XMLHttpRequest();
            application = this;
            x.open('GET', '/api/posts', true);
            x.onload = function(e) {
                if (x.readyState === 4) {
                    if (x.status === 200) {
                        application.posts = JSON.parse(x.responseText).data;
                    } else {
                        alert('HATA VAR');
                    }
                }
            }
            x.send(null);
        },
        'fetch_popular': function() {
            let x = new XMLHttpRequest();
            application = this;
            x.open('GET', '/api/posts?mode=popular', true);
            x.onload = function(e) {
                if (x.readyState === 4){
                    if (x.status === 200){
                        application.suggestion_list = JSON.parse(x.responseText).data;
                    } else {
                        alert('HATA VAR');
                    }
                }
            }
            x.send(null);
        },
     },
 });

app_menu = new Vue({
    'el': '#app-menu',
    'data': {
        'selected': ''
    },
    'methods': {
        'home_onclick': function() {
            app.selected = 'home';
            document.title = 'Anasayfa';
            document.getElementById('navbar').classList.remove('in')
            console.log(document.getElementById('navbar'))
        },
        'article_onclick': function() {

            app.selected = 'article';
            document.title = 'Article';
            document.getElementById('navbar').classList.remove('in')
        },
        'contact_onclick': function() {
            app.selected = 'contact';
            document.title = 'İletişim';
            document.getElementById('navbar').classList.remove('in')
        },
    }
});