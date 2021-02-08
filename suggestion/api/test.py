from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BarcodeTestCase(APITestCase):
    def test_upload(self):
        files = [("img", open("/home/gopi/Downloads/test.jpeg", "rb"))]
        url = reverse("barcode")
        with open("/home/gopi/Downloads/test.jpeg", "rb") as fp:
            data = {"img": fp}
            res = self.client.post(url, data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
