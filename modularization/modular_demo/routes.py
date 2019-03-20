from config import app
import users_controllers

app.add_url_rule("/", view_func=users_controllers.index)
app.add_url_rule("/users/create", view_func=users_controllers.users_create, methods=['POST'])
app.add_url_rule('/success', view_func=users_controllers.success)