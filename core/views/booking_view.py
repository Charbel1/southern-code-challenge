from datetime import datetime

from django.db.models import Max
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView

from core.models import PricingRule


class SetBookingView(APIView):
    def post(self, request, format=None):

        property_id = request.data["property_id"]
        date_start_format = request.data["date_start"]
        date_end_format = request.data["date_end"]

        date_start = datetime.strptime(date_start_format, '%m/%d/%Y')
        date_end = datetime.strptime(date_end_format, '%m/%d/%Y')


        # date_end = datetime.strptime(date_end, '%m/%d/%Y')
        stay_length = (date_end-date_start).days +1
        print(stay_length)
        query = Q()
        query_date = Q()
        query &= Q(property_id=property_id,min_stay_length__lte=stay_length)
        base_query= Q()
        base_query &=Q(property_id=property_id, min_stay_length__lte=stay_length)
        max_value_day = PricingRule.objects.filter(base_query).aggregate(
                Max('min_stay_length'))
        max_value =PricingRule.objects.filter(Q(min_stay_length=max_value_day["min_stay_length__max"]) & base_query
                                              ).aggregate(Max('price_modifier'))
        max_pricing_rule= PricingRule.objects.filter(Q(price_modifier = max_value["price_modifier__max"]) & base_query)\
            .order_by("id").first()

        base_query &= Q(property_id=property_id, min_stay_length__lte=stay_length)
        base_query_filter =PricingRule.objects.filter(base_query)
        max_value_day_2 = base_query_filter.aggregate(Max('min_stay_length'))
        max_value_2 = base_query_filter.filter(min_stay_length=max_value_day_2["min_stay_length__max"]).aggregate(Max('price_modifier'))
        max_pricing_rule_2 = base_query_filter.filter(price_modifier = max_value_2["price_modifier__max"]).order_by("id")


        pricing_rules = PricingRule.objects.filter(Q(property_id=property_id,min_stay_length__lte=stay_length))
        query_date &= Q(specific_day__range=(date_start,date_end))

        pricing_rules_spe_day = pricing_rules.filter(Q(specific_day__isnull=False)&query_date)
        z=pricing_rules_spe_day.values('specific_day').annotate(max_id=Max('fixed_price'))

        pricing_rules_spe_day_2 = pricing_rules.filter(Q(specific_day__isnull=False) & query_date)
        suma = 0
        for a in z:
            suma += a["max_id"]
            print(a["specific_day"],a["max_id"])

        valor_with_desc =( (max_pricing_rule.price_modifier *  max_pricing_rule.property.base_price) / 100 ) + max_pricing_rule.property.base_price
        total_base = ((stay_length - z.count()) * valor_with_desc)
        # desc = (max_pricing_rule.price_modifier *  total_base) / 100
        total_all= total_base + suma
        print(total_all)
        # print(pricing_rules.price_modifier)
        # for a in pricing_rules:
        #     print (a.specific_day)
        #     total = (a.property.base_price  * stay_length)
        #     total_por =(a.price_modifier * total)/100
        #     print(total+total_por)
        return HttpResponse(JsonResponse({"success": "pricing rule delete"}), content_type="application/json",
                            status=200)
