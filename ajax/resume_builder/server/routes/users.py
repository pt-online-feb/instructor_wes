from config import app
from server.controllers import users

app.add_url_rule('/users/new', view_func=users.new, endpoint="users:new")
app.add_url_rule('/users/create', view_func=users.create, endpoint="users:create", methods=['POST'])
app.add_url_rule('/users/login', view_func=users.login, endpoint="users:login", methods=['POST'])
app.add_url_rule('/users/logout', view_func=users.logout, endpoint="users:logout")
app.add_url_rule('/users/first_name', view_func=users.first_name, endpoint="users:first_name")