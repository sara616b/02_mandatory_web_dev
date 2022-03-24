from bottle import get, run, static_file, default_app

# STYLESHEET #########################
@get("/assets/app.css")
def style():
    return static_file("/assets/app.css", root=".")
    
# SCRIPT #############################
@get("/assets/script.js")
def script():
    return static_file("/assets/script.js", root=".")

# IMAGES #############################
@get("/assets/images/<image_filename>")
def get_images(image_filename):
    return static_file(f"/assets/images/{image_filename}", root=".")

# FAVICON #############################
@get("/favicon.svg")
def get_favicon():
    return static_file(f"/assets/favicon.svg", root=".")

# IMPORTING MODULES ##################
from feed import get_feed
from tweet import new_tweet_get, new_tweet_post, edit_tweet_get, edit_tweet_put, delete_tweet_delete
from signup import get_signup, post_signup
from login import get_login, post_login, delete_login
from user import profile_get

# PRODUCTION or DEVELOPMENT ##########
try:
    import production
    application = default_app()
except:
    run(host="127.0.0.1", port=4444, reloader=True, debug=True, server="paste")
