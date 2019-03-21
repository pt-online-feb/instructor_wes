from config import app, db
from server.routes import dashboard, tweets, users

if __name__ == "__main__":
    app.run(debug=True)