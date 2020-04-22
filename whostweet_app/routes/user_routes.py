from flask import Blueprint, jsonify, request, render_template, redirect  # flash
from whostweet_app.services.twitter_service import api_client
from whostweet_app.models import User, Tweet, parse_records, db
from whostweet_app.services.basilica_service import connection as basilica_connection

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users.json")
def list_users():
    users = [
        {"id": 1, "user_handle": "name1"},
        {"id": 2, "user_handle": "name2"},
        {"id": 3, "user_handle": "name3"}
    ]
    user_records = User.query.all()
    print(user_records)
    users = parse_records(user_records)
    return jsonify(users)


@user_routes.route("/users/<screen_name>/fetch")
def fetch_user_data(screen_name=None):
    print(screen_name)
    # import api to query user and statuses by screen_name
    api = api_client()
    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(
        screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)

    # user_records = User.query.all()
    # return render_template("users.html", message="Here's some users", users=user_records)

    # create user in db
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

    # create statuses in db

    # get text from api
    all_texts = [status.full_text for status in statuses]
    # make text into vectors using basilica to save as embeddings
    embeddings = list(basilica_connection.embed_sentences(
        all_texts, model="twitter"))

    # save each status as tweet in db
    counter = 0
    for status in statuses:
        print("----------" * 8)
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter += 1
        db.session.commit()
    return "OK"


@user_routes.route("/users/new")
def new_user():
    return render_template("new_user.html")
