from rest_framework import views
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from suggestion.utils import get_barcode


class BarcodeApiView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        img = request.data.get("img", None)
        if img:
            barcode = get_barcode(img)
            if barcode:
                data = {"status": "succes", "data": barcode}
                return Response(data=data, status=status.HTTP_200_OK)
            data = {"status": "failure", "data": "check the image"}
            return Response(data=data, status=status.HTTP_200_OK)
        data = {"status": "failure", "data": "bad request"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
