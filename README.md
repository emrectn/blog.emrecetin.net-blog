


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
### Tag Create
```http
POST /api/tag
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    "tags": "LABEL",
    "post_id": "POST_ID",
}

```
### Tag Delete
```http
DELETE /api/tag?tag_id=LABEL_ID
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    "tags": "LABEL",
    "post_id": "POST_ID",
}
```

### Comment Get (all comments a post)
```http
GET /api/comment?post_id=POST_ID
HOST: domain.com
```
### Comment Get (all comments a user)
```http
GET /api/comments?user_id=USER_ID
HOST: domain.com
```

### Comment Create
```http
POST /api/comment?post_id=POST_ID
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw

{
    "text": "TEXT",
    "date": "2018-01-12 20:01:09.123132",
}
```
### Comment Delete
```http
DELETE /api/comment?comment_id=COMMENT_ID
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw
```

### Comment Publish
```http
PUT /api/comment?comment_id=COMMENT_ID
HOST: domain.com
X-Token: as8as9-asdas65-zxx4c8-qweqw
```

### Test Script
```text
Python Script that test all api
```

![test_script](https://user-images.githubusercontent.com/29972884/35908498-f1af6552-0c01-11e8-8bd4-e41eb38081d0.gif)
