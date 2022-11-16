from datetime import datetime

from core.logic.booking_logic import BookingLogic
from core.logic.pricing_rule_logic import PricingRuleLogic
from core.utility.utility_code import ValidationDate


class UtilityCalculateBooking():

    def __init__(self):
        _pricing_rule_obj = None
        _booking = None
    def calcutate_final_price_booking(self,property_id : int, date_start_format : datetime, date_end_format:datetime):
        pricing_utility = PricingRuleLogic()
        booking_utility = BookingLogic()
        valid_utility = ValidationDate()

        date_start = valid_utility.parse_formate_date(date_start_format)
        date_end = valid_utility.parse_formate_date(date_end_format)
        stay_length = (date_end - date_start).days + 1
        max_stay_length = pricing_utility.get_max_stay_length_pricing_rule_property(property_id, stay_length)
        max_value2 = pricing_utility.get_max_value_pricing_rule_property(max_stay_length, property_id, stay_length)
        pricing_rule_obj = pricing_utility.filter_get_max_pricing_rule_obj(max_value2, property_id, stay_length)
        list_query = pricing_utility.get_specifict_days_with_max_fixed_price_rule(property_id, stay_length, date_start,
                                                                                  date_end)
        count_specific_day = len(list_query)
        total_specific_day = booking_utility.get_sum_specific_day(list_query)
        booking_utility.calculate_final_price(pricing_rule_obj.price_modifier, pricing_rule_obj.property.base_price,
                                              total_specific_day,
                                              stay_length, count_specific_day)

        self._pricing_rule_obj = pricing_rule_obj
        self._booking = booking_utility
        return booking_utility.get_final_price()

    def get_pricing_rule_obj_generate(self):
        return self._pricing_rule_obj

    def get_booking_utility(self):
        return  self._booking