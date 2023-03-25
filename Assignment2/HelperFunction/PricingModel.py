class PricingModel:
    def __init__(self, gallons_requested, rate_history):
        self.gallons_requested = gallons_requested
        self.rate_history = rate_history
    
    #TODO Calculate Price using constant variables such as Location Factor, Company Profit Factor