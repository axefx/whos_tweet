from flask import Blueprint, render_template, request
from sklearn.linear_model import LogisticRegression

from whostweet_app.models import User
from whostweet_app.services.basilica_service import connection as basilica_connection

stats_routes = Blueprint("stats_routes", __name__)


@stats_routes.route("/")
def wt_prediction_form():
    user_records = User.query.all()
    user_names = [user.screen_name for user in user_records]
    return render_template("prediction_form.html", user_names=user_names)


@stats_routes.route("/stats/predict", methods=["POST"])
def whostweet_prediction():
    print("FORM DATA", dict(request.form))
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]
    # train model
    model = LogisticRegression(random_state=24, max_iter=2000)

    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()

    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets

    embeddings = []
    labels = []
    all_tweets = user_a_tweets + user_b_tweets
    for tweet in all_tweets:
        embeddings.append(tweet.embedding)
        labels.append(tweet.user.screen_name)

    model.fit(embeddings, labels)
    # make prediction
    example_embedding = basilica_connection.embed_sentence(
        tweet_text, model="twitter")
    result = model.predict([example_embedding])
    screen_name_most_likely = result[0]

    return render_template("prediction_results.html",
                           screen_name_a=screen_name_a,
                           screen_name_b=screen_name_b,
                           tweet_text=tweet_text,
                           screen_name_most_likely=screen_name_most_likely
                           )
