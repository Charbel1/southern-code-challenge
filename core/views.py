from datetime import datetime

from django.core import serializers
from django.db.models import Count
from django.db.models import F
from django.db.models import Max
from django.db.models import Q
from django.db.models import Subquery
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from core.models import PricingRule
from core.models import Property


class PropertyCreateView(APIView):

    def post(self, request, format=None):
        name = request.data["name"]
        price = request.data["base_price"]
        type = request.data["type"]
        property_obj = Property()
        property_obj.name = name
        property_obj.base_price = price
        property_obj.type = type
        property_obj.save()

        return HttpResponse(JsonResponse({"property_id":property_obj.id }),content_type="application/json", status=200)

class GetModifyDeleteOnePropertyDataView(APIView):
    def get(self, request,id,format=None):

        property_out = Property.objects.get(id = id).get_json_data()

        return HttpResponse(JsonResponse({"data_out":property_out}),content_type="application/json", status=200)

    def put(self, request,id,format=None):

        name = request.data["name"]
        price = request.data["base_price"]
        type = request.data["type"]
        property_obj = Property.objects.get(id = id)

        property_obj.name = name
        property_obj.base_price = price
        property_obj.type = type
        property_obj.save()

        return HttpResponse(JsonResponse({"property_id": property_obj.id}), content_type="application/json", status=200)


    def delete(self, request, id, format=None):

        property_out = Property.objects.get(id=id).delete()


        return HttpResponse(JsonResponse({"success": "property delete"}), content_type="application/json", status=200)

class GetAllPropertyDataView(APIView):
    def get(self, request,format=None):
        data_out = []
        type = request.GET.get('type', "")
        if type != "" :
            property_list = Property.objects.filter(Q(type=type))
        else:
            property_list = Property.objects.filter()

        for property in property_list:
            data_out.append(property.get_json_data())

        return HttpResponse(JsonResponse({"data":data_out}),content_type="application/json", status=200)



class GetSetPrincingRulePropertyView(APIView):
    def post(self, request,property_id, format=None):
        property = Property.objects.get(id=property_id)
        price_modifier = request.data["price_modifier"]
        min_stay_length = request.data["min_stay_length"]
        fixed_price= request.data["fixed_price"]
        specific_day = request.data["specific_day"]
        pricing_rule = PricingRule()
        pricing_rule.property_id = property.id
        pricing_rule.price_modifier = price_modifier
        pricing_rule.min_stay_length = min_stay_length
        pricing_rule.fixed_price = fixed_price
        pricing_rule.specific_day = specific_day

        pricing_rule.save()

        return HttpResponse(JsonResponse({"pricing_rule_id": pricing_rule.id}), content_type="application/json", status=200)

    def get(self, request, property_id, format=None):
        data_out = []
        list_princing_rule = PricingRule.objects.filter(property_id=property_id)
        for pricing_rule in list_princing_rule:
            data_out.append(pricing_rule.get_json_data())

        return HttpResponse(JsonResponse({"pricing_rule_list": data_out}), content_type="application/json",
                            status=200)

class GetOnePrincingRulePropertyView(APIView):
    def get(self, request, pricing_id, format=None):
        data_out = PricingRule.objects.get(id=pricing_id).get_json_data()

        return HttpResponse(JsonResponse({"pricing_rule": data_out}), content_type="application/json",
                            status=200)

class ModifyDeleteOnePricingRuleProperty(APIView):
    def put(self, request, pricing_id, format=None):
        pricing_rule = PricingRule.objects.get(id=pricing_id)
        price_modifier = request.data["price_modifier"]
        min_stay_length = request.data["min_stay_length"]
        fixed_price = request.data["fixed_price"]
        specific_day = request.data["specific_day"]

        pricing_rule.price_modifier = price_modifier
        pricing_rule.min_stay_length = min_stay_length
        pricing_rule.fixed_price = fixed_price
        pricing_rule.specific_day = specific_day

        pricing_rule.save()

        return HttpResponse(JsonResponse({"success": "changed fields"}), content_type="application/json",
                            status=200)

    def delete(self, request, pricing_id, format=None):
        PricingRule.objects.get(id=id).delete()

        return HttpResponse(JsonResponse({"success": "pricing rule delete"}), content_type="application/json", status=200)


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
