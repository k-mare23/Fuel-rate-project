class Price:
    def __init__(self, gallons_requested, rate_history, state):
        self.gallons_requested = gallons_requested
        self.rate_history = rate_history
        self.state = state

    def price_per_gallon(self):
        curr_price = 1.50
        company_profit_factor = .10

        if self.state == "TX":
            loc_factor = 0.02
        else:
            loc_factor = 0.04

        if self.rate_history >= 1:
            history_factor = 0.01
        else:
            history_factor = 0.00
        
        if self.gallons_requested > 1000:
            gallon_factor = 0.02
        else:
            gallon_factor = 0.03

        
        margin = curr_price * (loc_factor - history_factor + gallon_factor + company_profit_factor)
        suggested_price = curr_price + margin
        total_amount_due = self.gallons_requested * suggested_price

        prices = [suggested_price, total_amount_due]

        return prices


