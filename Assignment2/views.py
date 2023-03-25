from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user, logout_user
from .models import Profile, User, Quote
from . import db

quote_info = []
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('views.fuel_quote_form'))

@views.route('/client_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        if len(full_name) < 2 or len(full_name) > 50:
            flash('Full name must be greater than 2 and less than 50 characters.', category='error')
        elif len(address1) < 2 or len(address1) > 100:
            flash('Address must be greater than 2 and less than 100 characters.', category='error')
        elif len(city) < 2 or len(city) > 100:
            flash('City must be greater than 2 and less than 100 characters.', category='error')
        elif len(state) != 2:
            flash('Reselect state.', category='error')
        elif len(zipcode) < 5 or len(zipcode) > 9:
            flash('Zipcode must be greater than 5 and no more than 9 characters.', category='error')
        else:
            print("current_user id is :", current_user.id)
            new_user_profile = Profile(full_name=full_name, address1=address1, address2=address2, city=city,
                                       state=state, zipcode=zipcode, user_id=current_user.id)
            db.session.add(new_user_profile)
            db.session.commit()

            flash('Profile created!', category='success')
            return redirect(url_for('views.fuel_quote_form'))

    return render_template("client_profile.html", user=current_user)

# Fuel Quote Form backend to obtain data from frontend form.
@views.route('/fuel_quote', methods=['GET', 'POST'])
@login_required
def fuel_quote_form():
    if request.method == 'POST':
        # get user input for fuel quote
        request_gallons = request.form.get('gallons_requested')
        request_delivery_date = request.form.get('delivery_date')
        gallons_requested =""

        # calculate suggested price and total amount due
        state = current_user.profile.state
        suggested_price = 0 # pricing module will be implemented later
        total_amount_due = float(request_gallons) * suggested_price

        # save fuel quote later
        gallons_requested=request_gallons
        delivery_address=current_user.profile.address
        delivery_date=request_delivery_date
        suggested_price=suggested_price
        total_amount_due=total_amount_due
        user_id=current_user.id

        return redirect(url_for('views.fuel_quote_history'))

    return render_template('fuel_quote.html', user=current_user)

@views.route('/fuel_quote_history')
@login_required
def fuel_quote_history():
    # query database for user's fuel quote history
    # quotes = FuelQuote.query.filter_by(user_id=current_user.id).all()
    if request.method == 'GET':
        start = request.args.get('start', default=0, type=int)
        limit_url = request.args.get('limit', default=20, type=int)
        questions = mongo.db.questions.find().limit(limit_url).skip(start);
        data = [doc for doc in questions]
        return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= data), 200
    return render_template('fuel_quote_hist.html', user=current_user) #, quotes=quotes)