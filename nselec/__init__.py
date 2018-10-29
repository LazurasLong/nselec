import os
import importlib
import random

__version__ = "2.0.1"

from flask import Flask


def noconf_voters_example_data():
    # you should put a function called GET_VOTERS in the config file
    # this function is the backup
    return {"testlandia": "Testlandia"}


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "nselec.db"),
        GET_VOTERS=noconf_voters_example_data,
    )

    app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import cli

    cli.init_app(app)

    from . import election_list

    app.register_blueprint(election_list.bp)

    modules = ("vote", "results", "auth", "admin", "pages")
    for modname in modules:
        mod = importlib.import_module("nselec." + modname)
        bp = mod.bp
        app.register_blueprint(bp, url_prefix="/" + modname)

    app.add_url_rule("/", endpoint="index")

    @app.context_processor
    def version_context():
        return {"version": __version__}

    @app.template_filter("shuffle")
    def shuffle_filter(s):
        try:
            result = list(s)
            random.shuffle(result)
            return result
        except:
            return s

    return app
