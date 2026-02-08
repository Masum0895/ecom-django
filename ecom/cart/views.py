from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    total = cart.cart_total()
    return render(request,'cart_summary.html',{'cart_products':cart_products, 'quantities':quantities,'total': total})



def cart_add(request):
    # Get the cart
    cart=Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        # Save to session
        cart.add(product = product, quantity = product_qty)

        # Get cart quantity
        cart_quantity = cart.__len__()

        #Return Response
        # response = JsonResponse({'Product Name':product.name})
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request,("Product added to Cart"))
        return response
    

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        # Call Delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request,("Item Deleted from Shopping Cart successfully!"))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request,("Your Cart has benn Updated!"))
        return response
        #return redirect('cart_summary')
    