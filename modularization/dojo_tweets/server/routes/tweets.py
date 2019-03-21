from config import app
from server.controllers import tweets

app.add_url_rule('/tweets/create', view_func=tweets.create, endpoint="tweets:create", methods=['POST'])