from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model
    """


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
