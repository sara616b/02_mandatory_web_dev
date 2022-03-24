from bottle import get, request, view, redirect

from g import *

@get("/login")
@get("/login/")
@view("login.html")
def _():
    try:
        if check_if_logged_in():
            return redirect("/")

        error = request.params.get("error")

        # get email from params to set as value in input 
        user_email = request.params.get("user_email")

        return dict(error=error, user_email=user_email, is_logged_in=check_if_logged_in())
        
    except Exception as ex:
        print(ex)
        response.status = 500
        return redirect("/")