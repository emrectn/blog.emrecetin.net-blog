


# Demo Blog.Emrecetin.net

I tried to create a blog site where I can write short articles basically on Python, Linux, C programming languages and Computer Engineering.


## API References

### User Create
```http
POST /api/user
HOST: domain.com
{
    "email": "EMAIL",
    "password": "PASSWORD",
    "fullname": "NAME SURNAME"
}
```

### User Delete
```http
DELETE /api/user
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

```

### User Change Password
```http
PUT /api/user
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    "new_password": "NEW_PASSWORD",
    "old_password": "OLD_PASSWORD"
}
```

### Auth
```http
POST /api/auth
HOST: domain.com

{
    "email": "EMAIL",
    "password": "PASSWORD"
}
```

### Post Get
```http
GET /api/post?post_id=POST_ID
HOST: domain.com
```
### Post Get All
```http
GET /api/posts
HOST: domain.com
```

### Post Create
```http
POST /api/post
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    "title": "ARTICLE TITLE",
    "text": "ARTICLE TEXT",
    "date": "2018-01-12 20:01:09.123132",
    "image": "IMAGE_PATH"  //Optional
}
```
### Post Delete
```http
DELETE /api/post?post_id=POST_ID
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw
```
### Label Create
```http
POST /api/label
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    "labels": "LABEL",
    "post_id": "POST_ID",
}
```
