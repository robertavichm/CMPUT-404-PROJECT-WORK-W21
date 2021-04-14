import datetime

def get_test_credentials(i=0):
    return {
        "username": f"user{i}",
        "password": "123",
    }

def get_author_fields(i=0):
    return {
        "displayName": f"Phil_Dunphy{i}",
        "host": f"http://somelink.xyz",
        "url": f"http://somelink.xyz/author/pdunph{i}",
        "github": f"http://github.com/phildunphy{i}",
        "type": "Author",
    }

def get_post_fields(i=0, visibility="PUBLIC", unlisted=False):
    return {
        "title": f"dummy title {i}",
        "description": "hello dummy description",
        "source": f"source from somewhere {i}",
        "origin": f"origial post location {i}",
        "contentType": "text/plain",
        "content": "grrrr content content content lorem ipsum",
        "categories": ["test", "data"],
        "commentLink": f"comment link {i}",
        "commentCount": 50,
        "pageSize": 10,
        "visibility": visibility,
        "unlisted": unlisted,
    }

def get_follow_fields():
    return {
        
    }

def get_comment_fields():
    return {
        "contentType": "text/plain",
        "comment": "hello I am comment"
    }

def post_comment_fields(id=0):
    return {
        "type": "comment",
        "author": f"{id}",
        "contentType": "text/plain",
        "comment": "hello I am comment"
    }


def get_like_fields(id=0):
    return {
        "object_id": f"{id}"
    }
