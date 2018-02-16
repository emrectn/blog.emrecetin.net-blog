app = new Vue({
    'el': '#app',
    'data': {
        'posts': []
    },
    'created': function () {
        this.fetch_posts();
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
        }
    },
    'components': {
        'tag': {
            'template': '#tag',
            'props': ['tag_data'],
            'data': function () {
                return {'name': this.t};
            }
        },
        'post': {
            'template': '#post',
            'props': ['post_data']
        },
        'suggestion': {
            'template': '#suggestion',
        }
    }
})
