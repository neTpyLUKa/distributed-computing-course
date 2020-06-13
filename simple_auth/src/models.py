from django.contrib.auth.models import User
from django.db import models

from proto.auth_pb2 import (
    User as GRPCUser,
    Admin as GRPCAdmin,
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(
        choices=(
            (GRPCUser, "User"),
            (GRPCAdmin, "Admin"),
        ),
        default=GRPCUser,
    )

    @staticmethod
    def exists(email):
        return Profile.objects.filter(user__email=email).exists()

    @staticmethod
    def add(email, password, role=GRPCUser, is_active=False):
        user = User.objects.create_user(username=email, email=email, password=password, is_active=is_active)
        user.save()

        profile = Profile(user=user, role=role)
        profile.save()
        return user

    @staticmethod
    def confirm_email(id):
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()


    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username
