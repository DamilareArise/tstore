from django.shortcuts import render, redirect, get_object_or_404
from productApp.models import Product

# Create your views here.



def getCartView(request):
    cart = request.session.get('cart', {})
    
    # {
    #     'product_id_1': 1,
    #     'product_id_2': 1,
    #     'product_id_3': 1,
    # }
    
    # [('product_id_1', 1), 'product_id_2': 1]
    
    cart_items = []  # [{"product": <product1>, 'qty': 2}, ]
    total= 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * qty
        item = {
            "product": product,
            'qty': qty,
            'subtotal': f"{subtotal:,}"
        }
        total += subtotal
        cart_items.append(item)
    
    return render(
        request,
        template_name="orderApp/cart.html",
        context={
            "cart": cart_items,
            "total": f"{total:,}"
        }
    )



def addToCart(request, product_id):
    product_id = str(product_id)
    cart_items = request.session.get('cart', {})
    if product_id in cart_items:
        cart_items[product_id] += 1

    else:
        cart_items[product_id] = 1 # {10: 1}
    
    # save cart to session
    request.session['cart'] = cart_items
    
    return redirect('get-cart')

    
    # session = {
    #     "cart": {
    #         'product_id_1': 1,
    #         'product_id_2': 1,
    #         'product_id_3': 1,
    #     },
    #     "username": "Dami"
        
    # }
    
