from flask import render_template, request, redirect, url_for, flash, Markup

from app import app


@app.route("/")
def index():
    return u"%s : %s" % (app.config['KAFKA_HOST'], app.config['binoas']['applications'],)


if __name__ == "__main__":
    app.run(threaded=True)
