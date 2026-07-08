


def getCartCount(request):
    cart = request.session.get('cart', {})
    cart_count=0
    for qty in cart.values():
        cart_count += qty
    
    return {
        'cart_count': cart_count
    }