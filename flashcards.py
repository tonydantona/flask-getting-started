from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for)
from model import db, save_db

app = Flask(__name__)


@app.route('/')
def welcome():
    # in real world you probably pass a set of rows from the db, not the whole db
    return render_template('welcome.html', cards=db)


@app.route('/card/<int:index>')
def card_view(index):
    try:
        card = db[index]
        # so /card.html/index will render the following page
        # using the passed in args
        return render_template('card.html',
                               card=card,
                               index=index,
                               max_index=len(db) - 1)
    except IndexError:
        abort(404)


# by default, view functions just handle Get requests. we have to add others
@app.route('/add_card', methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        # form has been submitted, process the data
        card = {"question": request.form['question'],
                "answer": request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db) - 1))
    else:
        return render_template('add_card.html')


@app.route('/remove_card/<int:index>', methods=['GET', 'POST'])
def remove_card(index):
    try:
        if request.method == 'POST':
            # form submitted, delete the card
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            card = db[index]
            return render_template('remove_card.html', card=card)
    except:
        abort(404)


# REST api calls, i.e. use Flask to serve up json instead of html
@app.route('/api/card')
def api_card_list():
    # in real world you probably pass a set of rows from the db, not the whole db
    # the following line will not work. for security reasons you can't return a list into a json response in an api
    # return db
    # need to jsonify it
    return jsonify(db)


@app.route('/api/card/<int:index>')
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)
