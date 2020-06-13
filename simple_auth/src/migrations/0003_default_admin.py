from django.db import migrations
from django.contrib.auth.hashers import make_password

import sys
sys.path.append("./proto")
from proto.auth_pb2 import Admin


def add_default_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")

    user = User.objects.create(
        username="0@localhost.com",
        email="0@localhost.com",
        password=make_password("password"),
        is_active=True,
    )
    user.save()

    Profile = apps.get_model("src", "Profile")

    admin = Profile(
        user=user,
        role=Admin,
    )
    admin.save()

    return


class Migration(migrations.Migration):
    dependencies = [
        ('src', '0002_profile_role'),
    ]

    operations = [
        migrations.RunPython(add_default_admin),
    ]