from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView

from core.logic.booking_logic import BookingLogic
from core.logic.pricing_rule_logic import PricingRuleLogic


class SetBookingView(APIView):
    def post(self,request):
        pricing_utility = PricingRuleLogic()
        booking_utility = BookingLogic()
        property_id = request.data["property_id"]
        date_start_format = request.data["date_start"]
        date_end_format = request.data["date_end"]


        date_start = datetime.strptime(date_start_format, '%m-%d-%Y')
        date_end = datetime.strptime(date_end_format, '%m-%d-%Y')
        stay_length = (date_end - date_start).days + 1
        # aqui
        max_stay_length = pricing_utility.get_max_stay_length_pricing_rule_property(property_id, stay_length)
        # cambiar nombre
        max_value2 = pricing_utility.get_max_value_pricing_rule_property(max_stay_length, property_id, stay_length)

        pricing_rule_obj = pricing_utility.get_max_pricing_rule_obj(max_value2, property_id, stay_length)

        list_query = pricing_utility.get_specifict_days_with_max_fixed_price_rule(property_id, stay_length, date_start,
                                                                                 date_end)
        count_specific_day = len(list_query)
        total_specific_day = booking_utility.get_sum_specific_day(list_query)
        final_price = booking_utility.get_final_price(pricing_rule_obj.price_modifier,pricing_rule_obj.property.base_price,total_specific_day,
                                                      stay_length,count_specific_day)

        data_out = booking_utility.get_data_out_json(pricing_rule_obj.property.base_price,date_start,date_end,pricing_rule_obj)



        return HttpResponse(JsonResponse({"data": data_out}), content_type="application/json",
                            status=200)
