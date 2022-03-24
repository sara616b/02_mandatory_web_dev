from bottle import get, request, view, redirect

from g import *

@get("/signup")
@get("/signup/")
@view("signup.html")
def _():
    try:
        if check_if_logged_in():
            return redirect("/")

        # get errors to display in signup.html
        errors = {}
        for error in [
            "first-name-missing",
            "first-name-length",
            "last-name-missing",
            "email-missing",
            "email-invalid",
            "user-exists-email",
            "username-missing",
            "password-missing",
            "password-short",
            "user-exists-username"
            ]:
            errors[error.replace("-", "_")] = request.params.get(error) if request.params.get(error) else 'no-error'

        # get values in form from url so they're remembered after reload
        form_values = {}
        for input in ["first-name", "last-name", "email", "username"]:
            form_values[f"user_{input.replace('-', '_')}"] = request.params.get(input)

        return form_values | errors | dict(is_logged_in=check_if_logged_in())
    
    except Exception as ex:
        print(ex)
        response.status = 500
        return redirect("/")
