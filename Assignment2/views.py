from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

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

