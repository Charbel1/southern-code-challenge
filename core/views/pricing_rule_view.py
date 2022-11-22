from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
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
        return Response({"pricing_rule_list": data_out}, status=HTTP_200_OK)

class CreatePrincingRulePropertyView(APIView):
    def post(self, request):
        pricing_logic = PricingRuleLogic()
        try:
            pricing_logic.validate_data(request.data)
            pricing_rule_obj = pricing_logic.create_pricing_rule()
        except Property.DoesNotExist:
            return Response({"Error": "property does not exist"}, status=HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"Error": "Error format data"}, status=HTTP_400_BAD_REQUEST)

        return Response({"pricing_rule_id": pricing_rule_obj.id}, status=HTTP_200_OK)
class GetOnePrincingRulePropertyView(APIView):
    def get(self, request, pricing_id):
        data_out = PricingRule.objects.get(id=pricing_id).get_json_data()

        return Response({"pricing_rule": data_out}, status=HTTP_200_OK)

class DeleteOnePricingRuleProperty(APIView):

    def delete(self, request, pricing_id):
        PricingRule.objects.get(id=pricing_id).delete()
        return Response({"success": "pricing rule delete"}, status=HTTP_200_OK)

class UpdateOnePricingRuleProperty(APIView):
    def put(self, request):
        pricing_logic = PricingRuleLogic()
        try:
            pricing_logic.validate_data(request.data)
            pricing_logic.update_pricing_rule()
        except PricingRule.DoesNotExist:
            return Response({"Error": "pricing_rule does not exist"}, status=HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"Error": "Error format data"}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": "update pricing rule"}, status=HTTP_200_OK)