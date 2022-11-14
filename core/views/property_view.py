from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView

from core.models import Property
from core.serializers.property_serializers import PropertySerializer


class PropertyCreateView(APIView):

    def post(self, request, format=None):
        # name = request.data["name"]
        # price = request.data["base_price"]
        # type = request.data["type"]
        property_seri = PropertySerializer(data=request.data)
        if property_seri.is_valid():
            property_obj= property_seri.save()
            return HttpResponse(JsonResponse({"property_id": property_obj.id}), content_type="application/json",
                                status=200)


        return HttpResponse(JsonResponse({"Error": property_seri.errors}), content_type="application/json", status=400)

        # property_obj = Property()
        # property_obj.name = name
        # property_obj.base_price = price
        # property_obj.type = type
        # property_obj.save()



class GetModifyDeleteOnePropertyDataView(APIView):
    def get(self, request,id,format=None):

        property_out = Property.objects.get(id = id).get_json_data()

        return HttpResponse(JsonResponse({"data_out":property_out}),content_type="application/json", status=200)

    def put(self, request,id,format=None):



        property_seri = PropertySerializer(data=request.data)
        if property_seri.is_valid():
            try:
                property_obj = Property.objects.get(id=id)
            except Property.DoesNotExist:
                return HttpResponse(JsonResponse({"error":"Property id Error"}), content_type="application/json",
                                    status=400)

            property_obj.name = request.data["name"]
            property_obj.base_price=request.data["base_price"]
            property_obj.type = request.data["type"]

            return HttpResponse(JsonResponse({"success": "data updated"}), content_type="application/json",
                                status=200)

        return HttpResponse(JsonResponse({"Error": property_seri.errors}), content_type="application/json", status=400)


    def delete(self, request, id, format=None):
        try:
            property_out = Property.objects.get(id=id).delete()
        except Property.DoesNotExist:
            return HttpResponse(JsonResponse({"error": "property does not exist"}), content_type="application/json",
                                status=400)

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
