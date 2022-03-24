from bottle import redirect, request, post
import re
import uuid
import time
import sqlite3

from g import *

@post("/signup")
def _():
    db = None
    redirectPath = "/"
    try:
        # get the info from the form and validate
        errors = []
        form_inputs = {}

        # first name
        new_user_first_name = request.forms.get("new_user_first_name")
        if not new_user_first_name:
            errors.append("first-name-missing")
        elif len(new_user_first_name) < 2 or len(new_user_first_name) > 50:
            errors.append("first-name-length")
        if new_user_first_name:
            form_inputs["first-name"] = new_user_first_name

        # last name
        new_user_last_name = request.forms.get("new_user_last_name")
        if not new_user_last_name:
            errors.append("last-name-missing")
        else:
            form_inputs["last-name"] = new_user_last_name

        # email
        new_user_email = request.forms.get("new_user_email")
        if not new_user_email:
            errors.append("email-missing")
        elif not re.match(REGEX_EMAIL, new_user_email):
            errors.append("email-invalid")
        if not new_user_email == '':
            form_inputs["email"] = new_user_email

        # username
        new_user_username = request.forms.get("new_user_username")
        if not new_user_username:
            errors.append("username-missing")
        else:
            form_inputs["username"] = new_user_username

        # password
        new_user_password = request.forms.get("new_user_password")
        if not new_user_password:
            errors.append("password-missing")
        elif len(new_user_password) < 3:
            errors.append("password-short")

        db = sqlite3.connect("database/database.sqlite")
        users_in_database = db.execute("""
            SELECT user_username, user_email
            FROM users
            WHERE user_username = :new_user_username OR user_email = :user_email
        """, (new_user_username, new_user_email)).fetchall()
        print(users_in_database)

        # check if username or email is already in use
        for user in users_in_database:
            if user[0] == new_user_username and new_user_username:
                errors.append("user-exists-username")
            if user[1] == new_user_email and new_user_email:
                errors.append("user-exists-email")

        # potential error messages
        if not errors == []:
            error_string = f'{"=error&".join(errors)}=error'
            form_input_string = ''
            for value in form_inputs:
                form_input_string += f"&{value}={form_inputs[value]}"
            redirectPath = f"/signup?{error_string}{form_input_string}"
            return

        # append user to USERS
        new_user = {
            "user_id": str(uuid.uuid4()),
            "user_first_name": new_user_first_name,
            "user_last_name": new_user_last_name,
            "user_username": new_user_username,
            "user_email": new_user_email,
            "user_password": new_user_password,
            "user_created_at": time.time(),
        }
        
        db.execute("INSERT INTO users VALUES(:user_id, :user_first_name, :user_last_name, :user_username, :user_email, :user_password, :user_created_at)", new_user)
        db.commit()
        redirectPath = "/login"
        return

    except Exception as ex:
        print(ex)
        response.status = 500
        redirectPath = "/"

    finally:
        if db != None:
            db.close()
        if redirectPath != None:
            return redirect(redirectPath)
