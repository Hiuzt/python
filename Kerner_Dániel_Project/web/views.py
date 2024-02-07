from django.conf import settings
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from web.models import Szamlak, CustomUserManager, User
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import xml.etree.ElementTree as ET

from .forms import LoginForm, RegisterForm


@login_required(login_url="/auth/login")
def homepage(request):
   
    invoice_data = list(Szamlak.objects.all())
    invoice_list = Paginator(invoice_data, 10) 

    page_number = request.GET.get("page")
    page_object = invoice_list.get_page(page_number)
    if not page_number:
        page_number = 1
     
    context = {"invoices": invoice_list.page(page_number), "page_object": page_object}
    return render(request, "invoices.html", context)

def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit = False)
                
            user_source = CustomUserManager()
            print(form.cleaned_data["password"])
            user = user_source.create_user(form.cleaned_data["email"], form.cleaned_data["name"], form.cleaned_data["password"])
            
            messages.success(request, "Sikeresen regisztráltál egy felhasználót!")
            return redirect("login")
        else:
            messages.error(request, form.errors)

    context = {"form": form}
    return render(request, "auth/register.html", context)

def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user_source = authenticate(request, username=form.cleaned_data["email"], password = form.cleaned_data["password"])
            if user_source is not None:
                login(request, user_source)
                messages.success(request, "Sikeresen bejelentkezés!")
                return redirect("index")
            else:
                messages.error(request, "Rossz adatokat adtál meg!")
        
    context = {"form": form}
    return render(request, "auth/login.html", context)
    
@login_required(login_url="/auth/login")
def signout(request):
    logout(request)
    return redirect("login")

@login_required(login_url="/auth/login")
def xml_invoice(request):
    app_name = __package__
    tree = ET.parse(app_name + static("xml/szamla.xml"))
    root = tree.getroot()

    data = {}

    def get_items(xml_element, append):
        temp_table = []
        for item in root.findall(xml_element):
            temp_dict = {}
            for child in item: 
                if child.tag == "cim":
                    temp_dict[child.tag] = {}
                    for address in child:
                        temp_dict[child.tag][address.tag] = address.text   
                elif xml_element == "./osszesites":
                    temp_dict[child.tag] = {}
                    for schild in child:
                        temp_dict[child.tag][schild.tag] = schild.text 
                else:
                    temp_dict[child.tag] = child.text   
            if append:                          
                temp_table.append(temp_dict)
            else:
                temp_table = temp_dict
        return temp_table

    
    data["elado"] = get_items("./fejlec/elado", False)
    data["vevo"] = get_items("./fejlec/vevo", False)
    data["szamla"] = get_items("./fejlec/szamlainfo", False)
    data["tetelek"] = get_items("./tetelek/tetel", True)
    data["osszesites"] = get_items("./osszesites", False)
    data["controller"] = get_items("./controller", False)

    context = {"data": data}
    return render(request, "invoice-xml.html", context)