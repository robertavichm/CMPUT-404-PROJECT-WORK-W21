import datetime

def get_author_fields():
    return {
        "displayName": "Phil Dunphy",
        "host": "dummyHostUrl",
        "url": "dummyUrl",
        "github": "https://Github.com/phildunphy",
        "type": "Author",
    }

def get_post_fields():
    return {
        "title": "dummy title",
        "description": "hello dummy description",
        "source": "source from somewhere",
        "origin": "origial post location",
        "contentType": "text/plain",
        "content": "grrrr content content content lorem ipsum",
        "categories": ["test", "data"],
        "commentLink": "comment link",
        "commentCount": 50,
        "pageSize": 10,
        "visibility": "PUBLIC",
        "unlisted": False,
    }

def get_comment_fields():
    return {
        "contentType": "text/plain",
        "comment": "hello I am comment"
    }

def get_like_fields():
    return {
        "object_id": "link to post that was liked"
    }
