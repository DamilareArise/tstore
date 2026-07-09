from django.shortcuts import render, redirect, get_object_or_404
from productApp.models import Product
from django.contrib import messages
from orderApp.models import Cart, CartItem
# Create your views here.




def getCartView(request):
    
    cart_items = []  # [{"product": <product1>, 'qty': 2}, ]
    total= 0
    
    if request.user.is_authenticated:
        cart_in_session = request.session.get('cart', {})   
        if cart_in_session:
            pass
        else:
           cart, _ = Cart.objects.get_or_create(user=request.user)
           item_objects = cart.items.all()
           
           for item_obj in item_objects:
                subtotal = item_obj.quantity * item_obj.product.price
                item = {
                    "product": item_obj.product,
                    'quantity': item_obj.quantity,
                    'subtotal': f"{subtotal:,}"
                }
                total += subtotal
                cart_items.append(item)
    else:
        cart = request.session.get('cart', {})
        # {
        #     'product_id_1': 1,
        #     'product_id_2': 1,
        #     'product_id_3': 1,
        # }
        
        # [('product_id_1', 1), 'product_id_2': 1]
        
        
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, id=product_id)
            subtotal = product.price * qty
            item = {
                "product": product,
                'quantity': qty,
                'subtotal': f"{subtotal:,}"
            }
            
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
    product = get_object_or_404(Product, id = product_id)
    
    if request.user.is_authenticated:
        db_cart, created = Cart.objects.get_or_create(
            user=request.user
        )
        
        cart_item, created = CartItem.objects.get_or_create(
            cart = db_cart,
            product = product,
            defaults={
                "quantity": 1
            }
        )
        
        if not created:
            cart_item.quantity+=1
            cart_item.save()
    
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