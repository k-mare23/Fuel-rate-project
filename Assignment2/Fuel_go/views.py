from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user, logout_user
from .models import Profile, User, Quote
from .PricingModule import Price
from . import db

quote_info = []
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("views.homepage")
    #return redirect(url_for('views.fuel_quote_form'))


@views.route('/client_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        if len(full_name) < 1 or len(full_name) > 50:
            flash('Full name must be between 1 and 50 characters.', category='error')
        elif len(address1) < 1 or len(address1) > 100:
            flash('Address must be between 1 and 100 characters.', category='error')
        elif len(city) < 1 or len(city) > 100:
            flash('City must be between 1 and 100 characters.', category='error')
        elif len(state) != 2:
            flash('Reselect state.', category='error')
        elif len(zipcode) < 5 or len(zipcode) > 9:
            flash('Zipcode must be between 5 and 9 characters.', category='error')
        else:
            print("current_user id is :", current_user.id)
            new_user_profile = Profile(full_name= full_name, address1=address1, address2=address2, city=city,
                                      state=state, zipcode=zipcode, user_id=current_user.id)
            db.session.add(new_user_profile)
            db.session.commit()

            flash('Profile created!', category='success')
            return redirect(url_for('views.fuel_quote_form'))
        
    user = User.query.get(current_user.id)
    profile = user.user_profile
    if profile:
        if len(profile) > 1:
            del (profile[:-1])
        cur_profile_id = profile[0].id
        user_profile = Profile.query.get(cur_profile_id)
        user_address1 = user_profile.address1
        user_address2 = user_profile.address2
        user_city = user_profile.city
        user_state = user_profile.state
        user_zipcode = user_profile.zipcode
        user_fullname = user_profile.full_name

        return render_template('client_profile.html', user = current_user, full_name=user_fullname, address1=user_address1,
                            address2=user_address2, city=user_city, state=user_state, zipcode=user_zipcode)
    else:
        return render_template("client_profile.html", user=current_user)

@views.route('/fuel-quote', methods=['GET', 'POST'])
def fuel_quote_form():
    user = User.query.get(current_user.id)
    profile_list = user.user_profile
    if profile_list:
        if len(profile_list) > 1:
            del(profile_list[:-1])
        curr_user = Profile.query.get(profile_list[0].id) #get current profile's user id
        state = curr_user.state

        if request.method == 'POST':
            request_gallons = request.form.get('gallonsRequested')
            request_date = request.form.get('date')
            request_address = request.form.get('deliveryAddress')
            quote_history = Quote.query.filter_by(user_id=current_user.id).first()

            if request_gallons <= 0:
                flash("Gallons requested can not be 0 or under.", category = 'error')
            if len(request_address) < 1:
                flash('Enter a valid address.', category='error')
            else: 
                if quote_history:
                    history_flag = 1
                else:
                    history_flag = 0
                
                quote = Price(request_gallons, history_flag, state) 
                quote_result = quote.price_per_gallon()
                global quote_info
                quote_info = [request_gallons, request_address, request_date, quote_result[0], quote_result[1]]
            return redirect(url_for('views.fuel_quote_result'))

    return render_template("fuel_quote.html", user=current_user)


@views.route('/fuel-quote-result', methods=['GET', 'POST'])
def fuel_quote_result():
    global quote_info
    print('fuel_quote ', quote_info)
    if request.method == 'POST':
        
        new_quote_result = Quote(gallons_requested=quote_info[0],
                                 delivery_address=quote_info[1],
                                 date=quote_info[2],
                                 suggest_price=quote_info[3],
                                 total_price=quote_info[4], user_id=current_user.id
                                 )
        db.session.add(new_quote_result)
        db.session.commit()

        flash('Quote result added!', category='success')
        return redirect(url_for('views.fuel_quote_history'))

    return render_template("fuel_quote.html", user=current_user, gallons_requested=quote_info[0],
                           delivery_address=quote_info[1], delivery_date=quote_info[2], suggest_price=quote_info[3],
                           total_price=quote_info[4])


@views.route('/fuel-quote-history', methods=['GET', 'POST'])
def fuel_quote_history():
    user = User.query.get(current_user.id)
    history_list = user.user_quote
    return render_template("fuel_quote_hist.html", user=current_user, history_list=history_list)

@views.route('/viewprofile', methods=['GET', 'POST'])
def viewprofile():
    user = User.query.get(current_user.id)
    profile_list = user.user_profile
    if profile_list:
        if len(profile_list) > 1:
            del (profile_list[:-1])
        cur_profile_id = profile_list[0].id
        user_profile = Profile.query.get(cur_profile_id)
        if user_profile.address2 == '':
            user_address = user_profile.address1
        else:
            user_address = user_profile.address1 + ', ' + user_profile.address2

        user_city = user_profile.city
        user_state = user_profile.state
        user_zipcode = user_profile.zipcode
        user_fullname = user_profile.full_name
        user_idname = user.first_name

        return render_template("viewprofile.html", user=current_user, user_name=user_idname, full_name=user_fullname, address=user_address,
                           city=user_city, state=user_state, zipcode=user_zipcode)
    else:
        return render_template("viewprofile.html", user=current_user)

@views.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template("homepage.html", user=current_user)


@views.route('/home_login_page')
def home_login():
    logout_user()
    return redirect(url_for('auth.login'))


@views.route('/home_registration')
def home_registration():
    logout_user()
    return redirect(url_for('auth.sign_up'))