from .models import Cart, CartItem
from productApp.models import Product
from django.shortcuts import get_object_or_404





def get_cart_items_from_db(request):
    
    db_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = []
    total = 0
    
    item_objects = db_cart.items.all()
           
    for item_obj in item_objects:
        subtotal = item_obj.quantity * item_obj.product.price
        item = {
            "product": item_obj.product,
            'quantity': item_obj.quantity,
            'subtotal': f"{subtotal:,}"
        }
        total += subtotal
        cart_items.append(item)
        
    return {
            "cart": cart_items,
            "total": f"{total:,}"
        }



def get_cart_items_from_session(request):
    cart_items = []
    total = 0
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
        
        total += subtotal
        cart_items.append(item)

    return {
            "cart": cart_items,
            "total": f"{total:,}"
        }

    
def add_item_to_cart(db_cart:Cart, product:Product, qty:int = 1):
    cart_item, created = CartItem.objects.get_or_create(
        cart = db_cart,
        product = product,
        defaults={
            "quantity": qty
        }
    )

    if not created:
        cart_item.quantity+=qty
        cart_item.save()