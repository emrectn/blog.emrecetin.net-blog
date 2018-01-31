

# Demo Blog.Emrecetin.net

I tried to create a blog site where I can write short articles basically on Python, Linux, C programming languages and Computer Engineering.


## API References

**User Create**
```http
POST /api/user
HOST: domain.com
{
    'email': 'emre@emrecetin.net',
    'password': 'emre123',
    'fullname': 'Emre Cetin'
}
```

**User Delete**
```http
DELETE /api/user
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

// If you want delete user, you have to be admin or the user
```

**User Change Password**
```http
PUT /api/user
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    'new_password': 'emre123',
    'old_password': 'emre12345'
}
```

**Auth**
```http
POST /api/auth
HOST: domain.com

{
    'email': 'emre@emrecetin.net',
    'password': 'emre123'
}
```

**Post Get**
```http
GET /api/post?post_id={post id}
HOST: domain.com
```
**Post Get All**
```http
GET /api/posts
HOST: domain.com
```

**Post Create**
```http
POST /api/post
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    'title': 'Hello World!',
    'text': 'Technology develop like a raw every year...',
    'date': '2018-01-12 20:01:09.123132',
    'image': '/static/name.png'  //Optional
}
```
**Post Delete**
```http
DELETE /api/post?post_id{post id}
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw
```
**Label Create**
```http
POST /api/label
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
	'labels': 'Education',
	'post_id': '1',
}
```
