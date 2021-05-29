from app import app
from flask import request, render_template


### ERRORS handler

@app.errorhandler(404)
def page_not_found(*args, **kvargs):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404