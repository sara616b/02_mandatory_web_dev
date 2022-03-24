from bottle import get, redirect, request, view
import sqlite3

from g import *

@get("/tweets/edit/<tweet_id>")
@get("/tweets/edit/<tweet_id>/")
@view("edit_tweet.html")
def _(tweet_id):
    db = None
    try:
        if not check_if_logged_in():
            return redirect("/login")
        
        tweet_to_edit = {}
        error = request.params.get("error")
        
        # connect to database
        db = sqlite3.connect("database/database.sqlite")

        # get tweet info from database
        tweet = db.execute("""
            SELECT tweet_text, tweet_image
            FROM tweets
            WHERE tweet_id = :tweet_id
        """,(tweet_id,)).fetchone()

        # if tweet is found, set info that's needed to display the editing inputs
        if tweet:
            tweet_to_edit = {
                "tweet_id": tweet_id,
                "tweet_text": tweet[0],
                "tweet_image": tweet[1]
            }
        
        # redirect if tweet doesn't exist
        if not tweet:
            return redirect("/")

        return dict(is_logged_in=check_if_logged_in(), tweet=tweet_to_edit, error=error)

    except Exception as ex:
        print(ex)
        response.status = 500
        return redirect("/")
    finally:
        if db != None:
            db.close()