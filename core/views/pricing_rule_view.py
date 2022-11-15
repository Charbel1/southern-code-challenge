from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView

from core.logic.pricing_rule_logic import PricingRuleLogic
from core.models import PricingRule
from core.models import Property


class GetPrincingRulePropertyView(APIView):

    def get(self, request, property_id):
        data_out = []
        list_princing_rule = PricingRule.objects.filter(property_id=property_id)
        for pricing_rule in list_princing_rule:
            data_out.append(pricing_rule.get_json_data())

        return HttpResponse(JsonResponse({"pricing_rule_list": data_out}), content_type="application/json",
                            status=200)

class CreatePrincingRulePropertyView(APIView):
    def post(self, request):
        pricing_logic = PricingRuleLogic()
        try:
            pricing_logic.validate_data(request.data)
            pricing_rule_obj = pricing_logic.create_pricing_rule()
        except Property.DoesNotExist:
           return HttpResponse(JsonResponse({"error": "property does not exist" }), content_type="application/json",
                               status=400)
        except Exception:
            return HttpResponse(JsonResponse({"error": "Error format data"}), content_type="application/json",
                                status=400)


        return HttpResponse(JsonResponse({"pricing_rule_id": pricing_rule_obj.id}), content_type="application/json", status=200)


class GetOnePrincingRulePropertyView(APIView):
    def get(self, request, pricing_id):
        data_out = PricingRule.objects.get(id=pricing_id).get_json_data()

        return HttpResponse(JsonResponse({"pricing_rule": data_out}), content_type="application/json",
                            status=200)


class DeleteOnePricingRuleProperty(APIView):

    def delete(self, request, pricing_id):
        PricingRule.objects.get(id=pricing_id).delete()

        return HttpResponse(JsonResponse({"success": "pricing rule delete"}), content_type="application/json", status=200)

class UpdateOnePricingRuleProperty(APIView):
    def put(self, request):
        pricing_logic = PricingRuleLogic()
        try:
            pricing_logic.validate_data(request.data)
            pricing_logic.update_pricing_rule()
        except PricingRule.DoesNotExist:
            return HttpResponse(JsonResponse({"error": "pricing_rule does not exist"}), content_type="application/json",
                                status=400)
        except Exception:
            return HttpResponse(JsonResponse({"error": "Error format data"}), content_type="application/json",
                                status=400)

        return HttpResponse(JsonResponse({"success": "update pricing rule"}), content_type="application/json",
                            status=200)
