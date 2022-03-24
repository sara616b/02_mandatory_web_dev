from bottle import get, redirect, request, view

from g import *

@get("/tweets/new")
@get("/tweets/new/")
@view("new_tweet.html")
def _():
    try:
        if not check_if_logged_in():
            return redirect("/login")
        
        error = request.params.get("error")
        tweet_text = request.params.get("text") if request.params.get("text") else ""
        
        return dict(is_logged_in=check_if_logged_in(), error=error, tweet_text=tweet_text)
    
    except Exception as ex:
        print(ex)
        response.status = 500
        return redirect("/")
