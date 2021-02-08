import logging
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .google_keyword_idea_service import SearchVolumePuller
from .serializers import (
    UserSigninSerializer,
    UserSerializer,
    PositionSerializer,
    MapPositionSerializer,
)
from .authentication import token_expire_handler, expires_in
from ..models import Position, MapPosition


logger = logging.getLogger(__name__)


class GoogleKeywordIdea(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        query = request.data.get("query")
        msg = f"Query: {query}"
        logger.debug(msg)
        logger.debug("Hey there it works!!")
        data = SearchVolumePuller.get_google_service(query)
        return Response({"data": data})


@api_view(["POST"])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def signin(request):
    signin_serializer = UserSigninSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=signin_serializer.data["username"], password=signin_serializer.data["password"]
    )
    if not user:
        return Response(
            {"detail": "Invalid Credentials or activate account"}, status=HTTP_404_NOT_FOUND
        )

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user)

    # token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)  # The implementation will be described further
    user_serialized = UserSerializer(user)

    return Response(
        {"user": user_serialized.data, "expires_in": expires_in(token), "token": token.key},
        status=HTTP_200_OK,
    )


@api_view(["GET"])
def user_info(request):
    return Response(
        {"user": request.user.username, "expires_in": expires_in(request.auth)}, status=HTTP_200_OK
    )


class PositionListApiView(ListAPIView):
    # queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated,)
    # user = authenticate(
        # username=serializer_class.data["username"], password=serializer_class.data["password"]
    # )
    # if not user:
    #     return Response(
    #         {"detail": "Invalid Credentials or activate account"}, status=HTTP_404_NOT_FOUND
    #     )
    # token, _ = Token.objects.get_or_create(user=user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PositionSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Position.objects.all()
        url = self.request.query_params.get("url", None)
        date = self.request.query_params.get("date", None)
        if url is not None:
            queryset = queryset.filter(url=url)
        if date is not None:
            d = datetime.strptime(date, "%Y-%m-%d")
            queryset = queryset.filter(date__month=d.month)
        return queryset.filter(verified=True)


class MapPositionListApiView(ListAPIView):
    queryset = MapPosition.objects.all()
    serializer_class = MapPositionSerializer
    permission_classes = (IsAuthenticated,)
    # token, _ = Token.objects.get_or_create(user=user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MapPositionSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = MapPosition.objects.all()
        name = self.request.query_params.get("name", None)
        date = self.request.query_params.get("date", None)
        if name is not None:
            queryset = queryset.filter(name=name)
        if date is not None:
            d = datetime.strptime(date, "%Y-%m-%d")
            queryset = queryset.filter(date__month=d.month)
        return queryset.filter(verified=True)

