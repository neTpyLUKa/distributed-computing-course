from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError
from django_grpc_framework.services import Service
from src.models import Profile


from src.serializers import ProfileProtoSerializer


class Auth(Service):
    """
    gRPC version of auth service for verifying tokens.
    """

    def Verify(self, request, context):
        print("Verifying...")
        try:
            token = UntypedToken(request.token)
            profile = Profile.objects.get(user_id=token["user_id"])
            profile.has_valid_token = True
        except TokenError as e:
            print(e)
            profile = Profile(user=User())

        profile_serializer = ProfileProtoSerializer(profile)

        return profile_serializer.message
