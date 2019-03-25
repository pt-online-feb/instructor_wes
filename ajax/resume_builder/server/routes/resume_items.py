from config import app
from server.controllers import resume_items

app.add_url_rule('/resume_items/create', view_func=resume_items.create, endpoint="resume_items:create", methods=['POST'])