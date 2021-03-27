import datetime

def get_author_fields(i=0):
    return {
        "username": f"Phil_Dunphy{i}",
        "displayName": f"Phil_Dunphy{i}",
        "host": f"http://somelink.xyz",
        "url": f"http://somelink.xyz/author/pdunph{i}",
        "github": f"http://github.com/phildunphy{i}",
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

def get_follow_fields():
    return {
        
    }

def get_comment_fields():
    return {
        "contentType": "text/plain",
        "comment": "hello I am comment"
    }

def get_like_fields():
    return {
        "object_id": "http://somelink.xyz"
    }
