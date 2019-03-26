from config import app
from server.controllers import resume_items

app.add_url_rule('/resume_items/create', view_func=resume_items.create, endpoint="resume_items:create", methods=['POST'])
app.add_url_rule('/resume_items/<user_id>', view_func=resume_items.current_user, endpoint="resume_items:current_user")