from bottle import get, redirect, request, view
import sqlite3
import jwt
import datetime
import json

from g import *

@get("/profile")
@get("/profile/")
@view("profile.html")
def _():
    db = None
    try:
        if not check_if_logged_in():
            return redirect("/login")

        user_id = jwt.decode(request.get_cookie("jwt", secret="secret"), JWT_KEY, algorithms=["HS256"])["user_id"]

        db = sqlite3.connect("database/database.sqlite")
        (user_first_name, user_last_name, user_username, user_email, user_created_at) = db.execute("""
            SELECT user_first_name, user_last_name, user_username, user_email, user_created_at
            FROM users
            WHERE user_id = :user_id
        """, (user_id,)).fetchone()

        user = {
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_username": user_username,
            "user_email": user_email,
            "user_created_at": datetime.datetime.fromtimestamp(int(user_created_at.split('.')[0])).strftime('%d/%m/%Y %H:%M'),
        }

        tweetsData = db.execute("""
            SELECT tweet_id, tweet_text, tweet_created_at, tweet_updated_at, tweet_image, tweet_user_id, user_first_name, user_last_name, user_username
            FROM tweets
            JOIN users
            WHERE tweets.tweet_user_id = users.user_id AND users.user_id = :user_id
            ORDER BY tweet_created_at DESC
            """, (user_id,)).fetchall()

        tweets = {}
        for tweet in tweetsData:
            tweets[tweet[0]] = {
                "tweet_text": tweet[1],
                "tweet_created_at": tweet[2],
                "tweet_created_at_datetime": date_text_from_epoch(tweet[2]),
                "tweet_updated_at": tweet[3],
                "tweet_updated_at_datetime": date_text_from_epoch(tweet[3]) if tweet[3] else None,
                "tweet_image": tweet[4],
                "tweet_user_id": tweet[5],
                "tweet_user_first_name": tweet[6],
                "tweet_user_last_name": tweet[7],
                "tweet_user_username": tweet[8],
            }
        return dict(is_logged_in=check_if_logged_in(), user=user, user_id=user_id, tweets=tweets)

    except Exception as ex:
        print(ex)
        response.status = 500
        return redirect("/")
    finally:
        if db != None:
            db.close()