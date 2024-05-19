from django.db import models as django_models, models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class DashModel(django_models.Model):
    qtdeAlimentoPeixe = models.IntegerField(verbose_name='AlimentoPeixe')
    limpezaAgua = models.CharField(verbose_name="LimpezaAgua", max_length=40)
    peixeMorto = models.CharField(verbose_name="PeixeMorto", max_length=40)
    capacidadeTanque = models.FloatField(verbose_name="CapacidadeTanque")
    nomeCliente = models.CharField(verbose_name="Cliente", max_length=75)
    statusTanque = models.CharField(verbose_name="Status", max_length=75)
    valorAlface = models.FloatField(verbose_name="ValorAlface")
    valorPeixe = models.FloatField(verbose_name="ValorPeixe")
    qtdeVendaPeixe = models.IntegerField(verbose_name="VendaPeixe")
    qtdeVendaAlface = models.IntegerField(verbose_name="VendaAlface")
    dataInspecao = models.DateField(verbose_name="Data")
    idCliente = models.IntegerField(verbose_name="IdCliente")
    idTanque = models.IntegerField(verbose_name="IdTanque")
    qtdeAgua = models.FloatField(verbose_name="qtdeAgua")
    qtdeAlfaceColhida =  models.IntegerField(verbose_name="AlfaceColhido")
    qtdeAlfacePlantada = models.IntegerField(verbose_name="AlfacePlantado")
    qtdePeixesTanque = models.IntegerField(verbose_name="PeixesNoTanque")

    class Meta:
        db_table = 'AquaDash'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=254)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Additional fields can be added here
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_email(self):
        return self.email

    def get_id(self):
        return self.id
    
    def get_short_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_perms(self, perm_list, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_staff