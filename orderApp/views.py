from django.shortcuts import render, redirect, get_object_or_404
from productApp.models import Product
from django.contrib import messages
from orderApp.models import Cart, CartItem
from .cart_service import get_cart_items_from_db, get_cart_items_from_session,add_item_to_cart
# Create your views here.




def getCartView(request):    
    if request.user.is_authenticated:
        cart_in_session = request.session.get('cart', {})   
        if cart_in_session:
            db_cart, created = Cart.objects.get_or_create(
            user=request.user
            )
            
            # to get the product: check the session
            for product_id, qty in cart_in_session.items():
                product = get_object_or_404(Product, id=product_id)    
                add_item_to_cart(db_cart, product, qty) 
                           
            # return the cart
            cart_items = get_cart_items_from_db(request)
        
        else:
           cart_items = get_cart_items_from_db(request)
    else:
        cart_items = get_cart_items_from_session(request)
            
    return render(
        request,
        template_name="orderApp/cart.html",
        context={
            "cart": cart_items['cart'],
            "total": cart_items['total']
        }
    )



def addToCart(request, product_id):
    product_id = str(product_id)
    product = get_object_or_404(Product, id = product_id)
    
    if request.user.is_authenticated:
        db_cart, created = Cart.objects.get_or_create(
            user=request.user
        )
        add_item_to_cart(db_cart, product)
    
    else:
        cart_items = request.session.get('cart', {})
        
        if product_id in cart_items:
            cart_items[product_id] += 1
        else:
            cart_items[product_id] = 1 # {10: 1}
    
        # save cart to session
        request.session['cart'] = cart_items
        
    messages.success(request, f'{product.title} added to cart')
    
    return redirect('get-cart')

    
    # session = {
    #     "cart": {
    #         'product_id_1': 1,
    #         'product_id_2': 1,
    #         'product_id_3': 1,
    #     },
    #     "username": "Dami"
        
    # }

    
def removeItem(request, product_id):
    product_id = str(product_id)
    
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = cart.items.get(product_id=product_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    
    cart_items = request.session.get('cart', {})
    if product_id in cart_items:
        if cart_items[product_id] > 1:
            cart_items[product_id] -= 1 
            
        else:
            del cart_items[product_id]
            
        
        request.session['cart'] = cart_items    
        messages.success(request, 'Product removed from cart')
    else:
        messages.error(request, 'Product not found')
    
    return redirect('get-cart')