from .cart import Cart

# Create Context Processors so our cart can work on all pages

def cart(request):
    # Return default data from Cart
    return {'cart':Cart(request)}