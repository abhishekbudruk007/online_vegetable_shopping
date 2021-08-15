from django.shortcuts import render
from django.shortcuts import redirect , get_object_or_404
from .models import Products , OrderItem , CheckoutAddress
from .models import Wishlist , Order
from .forms import CheckoutForm
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic.detail import DetailView , View
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone

def DetailViewFBV(request,pk):
    # sql_query = "select * from product where id=pk"
    products_object = Products.objects.filter(id=pk)[0]
    print("products_object",products_object)
    context = {"product":products_object}
    return render(request,'products/products_detail_view.html',context)



class ProductDetailCBV(DetailView):
    model = Products
    template_name = 'products/products_detail_view.html'



def AddToWishlistFBV(request,pk):
    product_object = Products.objects.filter(id=pk)[0]
    wishlist_object , created = Wishlist.objects.get_or_create(
        wishlist_user = request.user,
        wishlist_product = product_object
    )

    return redirect('dashboard:home')



class WishlistCBV(ListView):
    # Wishlist.objects.all()
    model = Wishlist
    template_name = "products/products_wishlist_view.html"
    context_object_name = "products"

    def get_queryset(self):
        query_set = Wishlist.objects.filter(wishlist_user=self.request.user)
        print("query_set",query_set)
        return query_set


class DeleteWishlistCBV(DeleteView):
    model = Wishlist
    success_url = reverse_lazy('products:wishlist')
    template_name = 'products/wishlist_confirm_delete.html'


def add_to_cart(request, pk):
   product = get_object_or_404(Products, pk=pk)
   order_product, created = OrderItem.objects.get_or_create(
       orderitem_product=product,
       orderitem_user=request.user,
       orderitem_ordered=False
   )
   order_qs = Order.objects.filter(user=request.user, ordered=False)

   if order_qs.exists():
       order = order_qs[0]

       if order.products.filter(orderitem_product__pk=product.pk).exists():
           order_product.orderitem_quantity += 1
           order_product.save()
           # messages.info(request, "Added quantity Item")
           return redirect("products:order_summary")
       else:
           order.products.add(order_product)
           # messages.info(request, "Item added to your cart")
           return redirect("products:order_summary")
   else:
       ordered_date = timezone.now()
       order = Order.objects.create(user=request.user, ordered_date=ordered_date)
       order.products.add(order_product)
       # messages.info(request, "Item added to your cart")
       return redirect("products:order_summary")



def remove_from_cart(request, pk):
   product = get_object_or_404(Products, pk=pk)
   order_qs = Order.objects.filter(
       user=request.user,
       ordered=False
   )
   if order_qs.exists():
       order = order_qs[0]
       if order.products.filter(orderitem_product__pk=product.pk).exists():
           order_item = OrderItem.objects.filter(
               orderitem_product=product,
               orderitem_user=request.user,
               orderitem_ordered=False
           )[0]
           order_item.delete()
           messages.info(request, "Item \""+order_item.orderitem_product.product_name+"\" remove from your cart")
           return redirect("dashboard:home")
       else:
           messages.info(request, "This Item not in your cart")
           return redirect("products:product_detail_view", pk=pk)
   else:
       messages.info(request, "You do not have an Order")
       return redirect("products:product_detail_view", pk=pk)


from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect , get_object_or_404, render

class OrderSummaryView(View):
   def get(self, *args, **kwargs):
       try:
           order = Order.objects.get(user=self.request.user, ordered=False)
           context = {
               'object': order
           }
           return render(self.request, 'products/order_summary.html', context)
       except ObjectDoesNotExist:
           messages.error(self.request, "You do not have an order")
           return redirect("dashboard:home")


def reduce_quantity_item(request, pk):
   product = get_object_or_404(Products, pk=pk )
   order_qs = Order.objects.filter(
       user = request.user,
       ordered = False
   )
   if order_qs.exists():
       order = order_qs[0]
       if order.products.filter(orderitem_product__pk=product.pk).exists() :
           order_item = OrderItem.objects.filter(
               orderitem_product=product,
               orderitem_user=request.user,
               orderitem_ordered=False
           )[0]
           if order_item.orderitem_quantity > 1:
               order_item.orderitem_quantity -= 1
               order_item.save()
           else:
               order_item.delete()
           messages.info(request, "Item quantity was updated")
           return redirect("products:order_summary")
       else:
           messages.info(request, "This Item not in your cart")
           return redirect("products:order_summary")
   else:
       #add message doesnt have order
       messages.info(request, "You do not have an Order")
       return redirect("products:order_summary")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'products/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')

                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
                if payment_option == 'C':
                    order.payment = payment_option
                    order.ordered = True
                    order.save()
                    messages.add_message(self.request, messages.SUCCESS, "Ordered Successfully")
                    return redirect('dashboard:home')
                elif payment_option == 'S':
                    return redirect('products:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('products:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid Payment option")
                    return redirect('products:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("products:order_summary")
