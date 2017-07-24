from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Getting our list of MOST LOVED MELONS
MOST_LOVED_MELONS = {
    'cren': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimRegular/crenshaw.jpg',
        'name': 'Crenshaw',
        'num_loves': 584,
    },
    'jubi': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Jubilee-Watermelon-web.jpg',
        'name': 'Jubilee Watermelon',
        'num_loves': 601,
    },
    'sugb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Sugar-Baby-Watermelon-web.jpg',
        'name': 'Sugar Baby Watermelon',
        'num_loves': 587,
    },
    'texb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Texas-Golden-2-Watermelon-web.jpg',
        'name': 'Texas Golden Watermelon',
        'num_loves': 598,
    },
}

# YOUR ROUTES GO HERE
@app.route('/')
def home():
    """A route for the main homepage"""

    return render_template('homepage.html')


@app.route('/top-melons')
def top_melons():
    """A route to view the top rated melons"""

    # makes a default name of user
    make_name()

    # pass dict of melons to the top-melons page
    return render_template('top-melons.html', melons= MOST_LOVED_MELONS)


@app.route('/get-name')
def set_name():
    """Sets the user's name in session and redirects to top melons"""

    # pulls users name from form
    name = request.args.get('name')

    # adds it to session as 'name'
    session['name'] = name

    #send user back to top-melons
    return redirect('/top-melons')


@app.route('/love-melon', methods=["POST"])
def love_a_melon():
    """Increments up the num_loves of the users favorite melon"""

    # makes a default name of user
    make_name()

    # get the name of the melon from the form
    loved_melon = request.form.get('melon-to-love')

    # target the dict for that melon
    melon_info = MOST_LOVED_MELONS[loved_melon]

    # increment up the number of loves for the selected melon
    melon_info['num_loves'] = melon_info.get('num_loves', 0) + 1

    return render_template('/thank-you.html')


@app.route('/thank-you')
def thank_user():
    """Routes user to a thank you page"""

    # makes a default name of user
    make_name()

    return render_template("thank-you.html")


def make_name():
    """Creates a default name of User if a name isn't given"""

    # sets default name of 'User' if no name is found
    session['name'] = session.get('name', 'User')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
