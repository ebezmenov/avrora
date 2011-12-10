#! coding:-utf8-
from django import template
from django.core.exceptions import ObjectDoesNotExist
from avrora.catalog.models import Category
from avrora.catalog.models import Product
from avrora.catalog.utils import get_current_product_category

register = template.Library()

@register.inclusion_tag('catalog/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, obj):
    """
    """
    if isinstance(obj, Category):
        objects = []
        while obj is not None:
            objects.insert(0, {
                "name" : obj.name,
                "url"  : obj.get_absolute_url(),
            })
            obj = obj.parent

        result = {
            "objects" : objects,
            "MEDIA_URL" : context.get("MEDIA_URL"),
        }
    elif isinstance(obj, Product):
        try:
            parent_product = obj
        except ObjectDoesNotExist:
            return []
        else:
            request = context.get("request")
            category = get_current_product_category(request, obj)
            if category is None:
                return []
            else:
                objects = [{
                    "name" : obj.get_name(),
                    "url"  : obj.get_absolute_url(),
                }]
                while category is not None:
                    objects.insert(0, {
                        "name" : category.name,
                        "url" : category.get_absolute_url(),
                    })
                    category = category.parent

        result = {
            "objects" : objects,
            "MEDIA_URL" : context.get("MEDIA_URL"),
        }

    else:
        return []

    return result

@register.inclusion_tag("inclusion/nav_list.html", takes_context=True)
def nav_lists(context):
# Создаем список для меню
    menu_nav = []
    root_cat = Category.objects.filter(level=0)
    for item in root_cat:
        list_nav=[]
        list_nav.append(item)
        sub_category = Category.objects.filter(parent=item)
        if sub_category.count() > 0:
            list_subitem = []
            for subitem in sub_category:
                list_subitem.append({'name':subitem.name, 'url':subitem.get_absolute_url(),})
            if list_subitem.count > 0 : list_nav.append(list_subitem)
        menu_nav.append(list_nav)
    result = {"lists": menu_nav,}
    return result
