from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = "asdf;lkjasdf;lkjd"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    session['name'] = request.form['name']
    session['location'] = request.form['location']
    session['favorite_language'] = request.form['favorite_language']
    return redirect('/result')

@app.route('/result')
def result():
    # get information here, send to template
    return render_template(
        'result.html',
        # name=session['name'],
        # location=session['location'],
        # language=session['favorite_language']
    )

@app.route('/test')
def test():
    if "random_number" not in session:
        print("That doesn't exist!")
        session['random_number'] = 5
    else:
        print(session['random_number'])
    return render_template('test.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/test')

if __name__ == "__main__":
    app.run(debug=True)