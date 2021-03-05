import datetime

def get_author_fields():
    return {
        "displayName": "dummyName",
        "host": "dummyUrl/dummyID",
        "url": "dummyUrl",
        "github": "dummyGitHubUrl",
        "type": "Author",
    }

def get_post_fields():
    return {
        "title": "dummy title",
        # "type": "post",
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
    