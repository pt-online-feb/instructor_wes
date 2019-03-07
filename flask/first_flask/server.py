from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', color="red")

@app.route('/colors/<pizza>')
def colors(pizza):
    return pizza

if __name__ == "__main__":
    app.run(debug=True)