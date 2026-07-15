from orderApp.models import Cart
from .cart_service import transfer_to_db


def getCartCount(request):
    cart_count=0
    
    if request.user.is_authenticated:
        cart_in_session = request.session.get('cart', {})   
        if cart_in_session:
            transfer_to_db(request, cart_in_session)
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item_objects = cart.items.all()
        for item in item_objects:
           cart_count += item.quantity 
           
    else:
        cart = request.session.get('cart', {})
        
        for qty in cart.values():
            cart_count += qty
        
    return {
        'cart_count': cart_count
    }