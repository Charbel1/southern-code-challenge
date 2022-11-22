from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from core.logic.pricing_rule_logic import PricingRuleLogic
from core.models import Booking
from core.models import Property
from core.utility.utility_code import ValidationDate
from core.views.calculate_booking import UtilityCalculateBooking


class SetBookingView(APIView):
    def post(self,request):
        pricing_utility = PricingRuleLogic()
        valid_utility = ValidationDate()
        utility = UtilityCalculateBooking()

        property_id = request.data["property_id"]
        date_start_format = request.data["date_start"]
        date_end_format = request.data["date_end"]

        date_start = valid_utility.parse_formate_date(date_start_format)

        date_end = valid_utility.parse_formate_date(date_end_format)

        if valid_utility.validate_change_greater(date_start,date_end):
            return Response({"Error": "order of dates is reversed"}, status=HTTP_400_BAD_REQUEST)

        try:
            final_price =utility.calcutate_final_price_booking(property_id, date_start_format, date_end_format)
        except Property.DoesNotExist:
            return Response({"Error": "property does not exist"}, status=HTTP_400_BAD_REQUEST)

        pricing_rule_obj = utility.get_pricing_rule_obj_generate()
        booking_utility = utility.get_booking_utility()
        property =utility.get_property()

        data_out = booking_utility.generate_data_out_json(final_price,property.base_price,
                                                          date_start, date_end, pricing_rule_obj)

        booking = Booking()
        booking.property= property
        booking.date_end = date_end
        booking.date_start = date_start
        booking.final_price =booking_utility.get_final_price()
        booking.save()
        data_out["booking_id"] = booking.id

        return Response({"data": data_out}, status=HTTP_200_OK)

class GetBookingPropertyView(APIView):
    def get(self,request,property_id):
        data_out = []
        booking_list = Booking.objects.filter(property_id = property_id )
        for booking in booking_list:
            data_out.append(booking.get_json_data())

        return Response({"data": data_out}, status=HTTP_200_OK)

class GetAllBookingView(APIView):
    def get(self,request):
        data_out = []
        booking_list = Booking.objects.filter()
        for booking in booking_list:
            data_out.append(booking.get_json_data())

        return Response({"data": data_out}, status=HTTP_200_OK)


class GetBookingByIdView(APIView):
    def get(self,request,booking_id):
        data_out = []
        booking_list = Booking.objects.filter(id = booking_id)
        for booking in booking_list:
            data_out.append(booking.get_json_data())

        return Response({"data": data_out}, status=HTTP_200_OK)


