from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm

from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if query := request.GET.get('search'):
        products = (products.filter(name__contains=query) | 
                    products.filter(description__contains=query))
    additional_cards = 3 - products.count() % 3
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'additional_cards': additional_cards,
                   'query': query})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', 
                  {'product': product, 'cart_product_form': cart_product_form})
