from django.template import RequestContext
from avrora.catalog.models import Category
from avrora.catalog.models import Product
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def get_category_nodes(request):
    """Returns the category tree as JSON for extJS.
    """
    categories = Category.objects.filter(parent = None)
        
    return render_to_response('main_view.html',{ 'cat': categories})

#TODO: Add context -processors
@login_required
def category_view(request, slug):
    active_cat = Category.objects.get(slug = slug)
    root_categories = Category.objects.filter(parent = None)
    return render_to_response('catalog_view.html',{ 'root_cat': root_categories, 'active':active_cat})

@login_required
def product_detail(request, slug):
    product = Product.objects.get(slug = slug)
    product.get_description()
    image = product.get_image()
    root_categories = Category.objects.filter(parent = None)
    active_cat = product.get_category()
    user_profile = request.user.get_profile()
    discount = user_profile.discount 
    act_price = product.price * (100 - discount) / 100
    return render_to_response('product_detail.html', {'root_cat': root_categories, 
                                                      'product':product,
                                                      'active':active_cat,
                                                      'act_price':act_price,
                                                      'discount':discount,
                                                      'image':image}
                              , context_instance=RequestContext(request))

    