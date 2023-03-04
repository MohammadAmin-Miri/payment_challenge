from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

regex_validator = RegexValidator(regex="^[+]?[0-9]{10,12}$", message="Please enter a valid phone number")


class CustomUser(AbstractUser):
    username = None
    phone = models.CharField(max_length=12, unique=True, validators=[regex_validator], null=True)
    email = models.EmailField(_('email address'), unique=True, null=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.email:
            return self.email
        elif self.phone:
            return self.phone
        else:
            return str(self.id)
        
        
class State(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name
    
    
class City(models.Model):
    name = models.CharField(max_length=120)
    state_id = models.ForeignKey(to=State, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
        
        
class Address(models.Model):
    user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    state_id = models.ForeignKey(to=State, on_delete=models.CASCADE)
    city_id = models.ForeignKey(to=City, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=12)
    description = models.TextField()
