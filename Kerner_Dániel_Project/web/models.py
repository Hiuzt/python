from datetime import timezone
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser
from django.contrib.auth import authenticate

class CustomUserManager(UserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError("Nem adtál meg e-mail címet!")
        if not name:
            raise ValueError("Nem adtál meg nevet!")
        
        email = self.normalize_email(email)
        user = User.objects.model(
            email = email,
            name = name,
        )
        user.set_password(password)
        user.save(using=self.db)
        

        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    register_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self

    class Meta:
        db_table = "Users"
    
class Szamlak(models.Model):
    sorszam = models.CharField(max_length=255)
    megnevezes = models.CharField(max_length=255)
    kiegyenlitve = models.IntegerField(default=0)
    sztorno = models.IntegerField()
    datum_kiallitas = models.DateField()
    datum_teljesites = models.DateField()
    datum_fizetesihatarido = models.DateField()
    datum_kiegyenlites = models.DateTimeField()
    nettoarossz = models.DecimalField(max_digits=18, decimal_places=3)
    afaertekossz = models.DecimalField(max_digits=18, decimal_places=3)
    bruttoarossz =  models.DecimalField(max_digits=18, decimal_places=3)
    penznem = models.CharField(max_length=3)
    xmlvevo = models.CharField(max_length=255)
    eszamla = models.SmallIntegerField(default=1, max_length=1) #TinyINT nincs

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "szamlak"
