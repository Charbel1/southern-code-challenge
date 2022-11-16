from datetime import datetime

from core.models import PricingRule


class BookingLogic():
    specific_day =[]
    def get_final_price(self):
        return self.total_all
    def get_sum_specific_day(self, list_specific_day: list):
        suma = 0
        for value in list_specific_day:
            aux =f"specific_day {value['specific_day']}, fixed_price: {value['max_id']}"
            self.specific_day.append(aux)
            suma += value["max_id"]

        return suma


    def calculate_final_price(self, price_modifier, property_base_price, total_specific_day, stay_length, count_specific_day):
        valor_with_desc = ((price_modifier * property_base_price) / 100) + \
                          property_base_price

        total_base = ((stay_length - count_specific_day) * valor_with_desc)
        # desc = (max_pricing_rule.price_modifier *  total_base) / 100
        self.total_all = total_base + total_specific_day



        return self.total_all


    def get_data_out_json(self,base_price :int ,date_start : datetime, date_end :datetime, pricing_rule : PricingRule):
        data_out = {
                    "Property base_price " : base_price,
                    "Booking":{
                            "date_start": date_start,
                            "date_end":date_end,
                            "stay length" : (date_start-date_end).days + 1
                            },
                    "Pricing Rules":{
                            "Pricing Rules":f"min_stay_length:{pricing_rule.min_stay_length} price_modifier {pricing_rule.price_modifier}",
                            "specific_day":self.specific_day
                            },
                    "Final Price": self.total_all
                    }
        return data_out


