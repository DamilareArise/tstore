from orderApp.models import Cart


def getCartCount(request):
    cart_count=0
    
    if request.user.is_authenticated:
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