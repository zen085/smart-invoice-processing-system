from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager
from core.models import  TimeStampModel
import uuid

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin,TimeStampModel):
    
    class Role(models.TextChoices):
        ADMIN = "admin","Admin"
        STAFF = "staff","Staff"
        CUSTOMER = "customer","Customer"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff =  models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # class Meta:
    #     db_table = "users"
    #     verbose_name = "User"
    #     verbose_name_plural = "Users"
    def __str__(self):
        return self.email
