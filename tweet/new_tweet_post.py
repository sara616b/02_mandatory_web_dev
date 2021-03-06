from bottle import redirect, request, post
import uuid
import os
import jwt
import time
import sqlite3
import imghdr

from g import *

@post("/tweets/new")
def _():
    db = None
    redirectPath = "/"
    try:
        if not check_if_logged_in():
            redirectPath = "/login"
            return
        else:
            # decode jwt cookie to get user id for new tweet
            user_id = jwt.decode(request.get_cookie("jwt", secret="secret"), JWT_KEY, algorithms=["HS256"])["user_id"]
        
        # text
        new_tweet_text = request.forms.get("new_tweet_text")
        if not new_tweet_text:
            # cant post empty tweets
            redirectPath = "/tweets/new?error=empty"
            return
        if len(new_tweet_text) < 2:
            redirectPath = f"/tweets/new?error=short&text={new_tweet_text}"
            return
        if len(new_tweet_text) > 250:
            redirectPath = f"/tweets/new?error=long&text={new_tweet_text}"
            return
        
        # image 
        image = request.files.get("tweet_image")
        image_name = None
        if image:
            # get extention and validate
            file_name, file_extension = os.path.splitext(image.filename)
            if file_extension.lower() == ".jpg": file_extension = ".jpeg"
            if file_extension.lower() not in (".png", ".jpg", ".jpeg"):
                redirectPath = f"/tweets/new?error=image-not-allowed&text={new_tweet_text}"
                return

            # image name
            image_name = f"{str(uuid.uuid4())}{file_extension}"

            # save image
            image.save(f"assets/images/{image_name}")

            # is the image valid
            imghdr_extension = imghdr.what(f"assets/images/{image_name}")
            if file_extension != f".{imghdr_extension}":
                # delete the invalid image 
                os.remove(f"assets/images/{image_name}")
                redirectPath = f"/tweets/new?error=image-not-allowed&text={new_tweet_text}"
                return

        # connect to database
        db = sqlite3.connect("database/database.sqlite")
        
        # append new tweet with values
        new_tweet = {
            "tweet_id": str(uuid.uuid4()),
            "tweet_text": new_tweet_text,
            "tweet_created_at": str(time.time()),
            "tweet_updated_at": None,
            "tweet_image": image_name if image_name else None,
            "tweet_user_id": user_id,
        }

        # insert new tweet to database
        db.execute("""
            INSERT INTO tweets
            VALUES(
                :tweet_id,
                :tweet_text,
                :tweet_created_at,
                :tweet_updated_at,
                :tweet_image,
                :tweet_user_id)
            """, new_tweet)
        db.commit()

        redirectPath = "/"
        return

    except Exception as ex:
        print(ex)
        response.status = 500
        return redirect("/")

    finally:
        if db != None:
            db.close()
        return redirect(redirectPath)