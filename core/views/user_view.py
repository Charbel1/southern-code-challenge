from rest_framework.authtoken.admin import User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from core.serializers.user_serializers import UserSerializer


class UserCrud(APIView):
    def post(self, request,format=None):
        serializer_class = UserSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user":user.username
                })

    def get(self, request, format=None):
        serializer_class = UserSerializer
        # serializer = serializer_class(data=request.data)
        users = User.objects.filter()
        data_out= []
        for user in users:
            data_out.append(
                    {
                            "id":user.id,
                            "username":user.username,
                            "email":user.email,
                            }
                    )
        return Response({"data_out": data_out}, status=HTTP_200_OK)

    def delete(self, request, format=None):
        users = User.objects.filter(username=request.data["username"])
        users.delete()

        return Response({"data_out": "ok"}, status=HTTP_200_OK)
