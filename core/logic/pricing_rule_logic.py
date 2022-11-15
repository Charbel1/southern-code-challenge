from datetime import datetime

from core.models import PricingRule
from core.models import Property
from core.utility.utility_code import ValidationDate


class PricingRuleLogic():

    def __init__(self):
        self._pricing_rule : PricingRule = None
        self._property : Property = None
        self._price_modifier : float = None
        self._min_stay_length : int = None
        self._fixed_price : float = None
        self._specific_day : datetime = None

    def validate_data(self,data:dict):

        utility_date = ValidationDate()

        if "property_id" in data:
            self._property = Property.objects.get(id = data["property_id"])

        if "price_modifier" in data:
            if data["price_modifier"] is not None:
                self._price_modifier = float(data["price_modifier"])

        if "min_stay_length" in data:
            if data["min_stay_length"] is not None:
                self._min_stay_length = int(data["min_stay_length"])

        if "fixed_price" in data:
            if data["fixed_price"] is not None:
                self._fixed_price = float(data["fixed_price"])

        if "specific_day" in data:
            if data["specific_day"] is not None:
                self._specific_day = utility_date.parse_formate_date(data["specific_day"])

    def create_pricing_rule(self):
        self._pricing_rule = PricingRule()
        self._pricing_rule.property_id = self._property.id
        self._pricing_rule.price_modifier = self._price_modifier
        self._pricing_rule.min_stay_length = self._min_stay_length
        self._pricing_rule.fixed_price = self._fixed_price
        self._pricing_rule.specific_day = self._specific_day
        self._pricing_rule.save()
        return self._pricing_rule