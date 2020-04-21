from flask import Flask

from whostweet_app.models import db, migrate
from whostweet_app.routes.book_routes import book_routes
from whostweet_app.routes.home_routes import home_routes
from whostweet_app.routes.user_routes import user_routes


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/axel/Desktop/whos_tweet/whostweet.db"

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(user_routes)
    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
