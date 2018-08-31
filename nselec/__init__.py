import os
from flask import Flask

def noconf_voters_example_data():
    # you should put a function called GET_VOTERS in the config file
    # this function is the backup
    return {"testlandia":"Testlandia"}

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, 'nselec.db'),
        GET_VOTERS = noconf_voters_example_data,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import election_list
    app.register_blueprint(election_list.bp)

    from . import vote
    app.register_blueprint(vote.bp, url_prefix="/vote")

    return app
