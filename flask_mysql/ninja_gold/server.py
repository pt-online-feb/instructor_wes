from flask import Flask, render_template, redirect, session, request
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def index():
    query_string = "SELECT * FROM locations;"
    db = connectToMySQL("feb_ninja_gold_demo")
    location_list = db.query_db(query_string)
    return render_template('index.html', locations=location_list)

@app.route('/locations/new')
def new_location():
    return render_template('new_location.html')

@app.route('/locations/create', methods=["POST"])
def create_location():
    query_string = 'INSERT INTO locations (name, min_gold, max_gold) VALUES(%(name_from_form)s, %(min_from_form)s, %(max_from_form)s);'
    form_data = {
        "name_from_form": request.form['name'],
        "min_from_form": request.form['min_gold'],
        "max_from_form": request.form['max_gold']
    }
    db = connectToMySQL("feb_ninja_gold_demo")
    db.query_db(query_string, form_data)
    return redirect('/locations/new')

if __name__ == "__main__":
    app.run(debug=True)
