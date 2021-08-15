from django.shortcuts import render
from products.models import Products
from django.views.generic.list import ListView
# Create your views here.
def Home(request):
    # sql_query = "select * from products"
    products_object = Products.objects.all()
    print("products_object",products_object)
    context = {"name":"Abhishek" , "name_list":['t','r','e','n','d','i','n','g', 'U'],"products":products_object}
    return render(request,"dashboard/home.html",context)


class HomePageCBV(ListView):
    model = Products
    template_name = 'dashboard/home.html'
    context_object_name = 'products'