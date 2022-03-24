import secrets
from bottle import delete, get, post, response, request, redirect
from g import *
import sqlite3

@delete("/login")
def _():
    redirectPath = None
    try:
        # get cookie
        session_id = request.get_cookie("jwt", secret="secret")
        # remove cookie by making it expire 
        response.set_cookie("jwt", "", secret="secret", expires=0)

        # connect to database
        db = sqlite3.connect("database/database.sqlite")
        # delete session from database
        db.execute("DELETE FROM sessions WHERE session_id = :session_id", (str(session_id),))
        db.commit()

        redirectPath = "/"
    
    except Exception as ex:
        print(ex)
        response.status = 500
        redirectPath = "/"
    
    finally:
        if db != None:
            db.close()
        if redirectPath != None:
            return redirect(redirectPath)
