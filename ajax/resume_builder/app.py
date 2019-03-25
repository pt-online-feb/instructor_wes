from config import app, db
from server.routes import users, resume_items, dashboard

if __name__ == "__main__":
    app.run(debug=True)