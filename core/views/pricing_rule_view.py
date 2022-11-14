from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView

from core.models import PricingRule
from core.models import Property


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
