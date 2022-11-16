from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView

from core.logic.booking_logic import BookingLogic
from core.logic.pricing_rule_logic import PricingRuleLogic
from core.models import Booking
from core.utility.utility_code import ValidationDate


class SetBookingView(APIView):
    def post(self,request):
        pricing_utility = PricingRuleLogic()
        booking_utility = BookingLogic()
        valid_utility = ValidationDate()

        property_id = request.data["property_id"]
        date_start_format = request.data["date_start"]
        date_end_format = request.data["date_end"]

        date_start = valid_utility.parse_formate_date(date_start_format)

        date_end = valid_utility.parse_formate_date(date_end_format)

        if valid_utility.validate_change_greater(date_start,date_end):
            return HttpResponse(JsonResponse({"error": "order of dates is reversed"}), content_type="application/json",
                                status=200)

        # the number of days between the 2 dates is taken out
        stay_length = (date_end - date_start).days + 1


        max_stay_length = pricing_utility.get_max_stay_length_pricing_rule_property(property_id, stay_length)

        max_value2 = pricing_utility.get_max_value_pricing_rule_property(max_stay_length, property_id, stay_length)

        pricing_rule_obj = pricing_utility.get_max_pricing_rule_obj(max_value2, property_id, stay_length)

        list_query = pricing_utility.get_specifict_days_with_max_fixed_price_rule(property_id, stay_length, date_start,
                                                                                 date_end)
        count_specific_day = len(list_query)

        total_specific_day = booking_utility.get_sum_specific_day(list_query)
        booking_utility.calculate_final_price(pricing_rule_obj.price_modifier, pricing_rule_obj.property.base_price, total_specific_day,
                                              stay_length, count_specific_day)

        data_out = booking_utility.generate_data_out_json(pricing_rule_obj.property.base_price, date_start, date_end, pricing_rule_obj)

        booking = Booking()
        booking.property= pricing_rule_obj.property
        booking.date_end = date_end
        booking.date_start = date_start
        booking.final_price =booking_utility.get_final_price()
        booking.save()
        data_out["booking_id"] = booking.id

        return HttpResponse(JsonResponse({"data": data_out}), content_type="application/json",
                            status=200)

class GetBookingPropertyView(APIView):
    def get(self,request,property_id):
        data_out = []
        booking_list = Booking.objects.filter(property_id = property_id )
        for booking in booking_list:
            data_out.append(booking.get_json_data())

        return HttpResponse(JsonResponse({"data": data_out}), content_type="application/json",
                            status=200)

class GetAllBookingView(APIView):
    def get(self,request):
        data_out = []
        booking_list = Booking.objects.filter()
        for booking in booking_list:
            data_out.append(booking.get_json_data())

        return HttpResponse(JsonResponse({"data": data_out}), content_type="application/json",
                            status=200)


class GetBookingByIdView(APIView):
    def get(self,request,booking_id):
        data_out = []
        booking_list = Booking.objects.filter(id = booking_id)
        for booking in booking_list:
            data_out.append(booking.get_json_data())

        return HttpResponse(JsonResponse({"data": data_out}), content_type="application/json",
                            status=200)


