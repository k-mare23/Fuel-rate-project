from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user
from .models import Profile, User

quote_info = []
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('views.fuel_quote_form'))

def get_price(state, request_frequent, request_gallons):
    # since we don't need to implement the price module for this assignment,
    # we can just assign 0s for suggested price and total amount due, and put those into 'results'  
    # Pricing module will be implemented later
    
    results = [0, 0]
    return results

@views.route('/', methods=['GET', 'POST'])
def client_profile():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        address = request.form.get('address')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip code')
        if len(full_name) < 1 or len(full_name) > 50:
            flash('Full name must have at least 1 character and at most 50 characters.', category='error')
        elif len(address) < 1 or len(address) > 100:
            flash('Address must have at least 1 character and at most 100 characters.', category='error')
        elif len(city) < 1 or len(city) > 100:
            flash('City must have at least 1 character and at most 100 characters.', category='error')
        elif len(state) != 2:
            flash('Please select a state.', category='error')
        elif len(zip_code) < 5 or len(zip_code) > 9:
            flash('Zipcode must have at least 5 characters at most 9 characters.', category='error')
        else:
            print("Current user is ", current_user.id)
            user_profile = Profile(full_name=full_name, address=address, address2=address2, city=city,
                                       state=state, zipcode=zip_code, user_id=current_user.id)
            flash('Created Profile Successfully', category = 'success')

    user = User.query.get(current_user.id)
    profile_list = user.user_profile

    if profile_list:
        if len(profile_list) > 1:
            del (profile_list[:-1])
        cur_profile_id = profile_list[0].id
        user_profile = Profile.query.get(cur_profile_id)
        user_address = user_profile.address
        user_address2 = user_profile.address2
        user_city = user_profile.city
        user_state = user_profile.state
        user_zipcode = user_profile.zip_code
        user_fullname = user_profile.full_name

        return render_template("client_profile.html", user=current_user, full_name=user_fullname, address=user_address,
                           address2=user_address2, city=user_city, state=user_state, zipcode=user_zipcode)

    else:
        return render_template("client_profile.html", user=current_user)