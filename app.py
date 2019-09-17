import os

from flask import Flask, jsonify
from utils.database import db

from config import config
from flask_jsglue import JSGlue



def create_app(config_name=None):
    # create and configure the app
    app = Flask(__name__)
    jsglue = JSGlue(app)

    app.config.from_object(config.get(config_name or "default"))
    # setup_db
    # db.init_app(app)


    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code

    # import blueprints
    from home.views import home
    from users.views import user_app
    from blog.views import article

    # register blueprints
    app.register_blueprint(home)
    app.register_blueprint(user_app)
    app.register_blueprint(article)


    return app