from config import app
from server.controllers import users

app.add_url_rule('/users/new', view_func=users.users_new, endpoint="users:new")
app.add_url_rule('/users/create', view_func=users.users_create, endpoint="users:create", methods=['POST'])
app.add_url_rule('/users/login', view_func=users.users_login, endpoint="users:login", methods=['POST'])
app.add_url_rule('/users/logout', view_func=users.users_logout, endpoint="users:logout")