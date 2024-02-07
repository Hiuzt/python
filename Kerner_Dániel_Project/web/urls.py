from django.urls import path
from . import views
from django.db import connection
from django.templatetags.static import static

from web.models import Szamlak

urlpatterns = [
    path("", views.homepage, name="index"),
    path("auth/register/", views.register_view, name="register"),
    path("auth/login/", views.login_view, name="login"),
    path("xmlinvoice/", views.xml_invoice, name="xmlinvoice"),
    path("signout/", views.signout, name="signout"),

]


def check_db_exists(): # Sql beszúrás ha nincs adat az adatbázisban
    invoice_data = list(Szamlak.objects.all())

    if (len(invoice_data) < 1):
        appname = __package__
        with open(appname + static("szamlak.sql"), 'r') as sql_file:
            sql_content = sql_file.read()
            
        with connection.cursor() as cursor:
            cursor.execute(sql_content)

        connection.commit()

check_db_exists()
