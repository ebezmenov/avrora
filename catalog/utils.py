#! coding:-utf8-
from lxml import etree
from avrora.catalog.models import Category
from avrora.catalog.models import Product

def get_current_product_category(request, product):
    try:
        product_categories = product.get_categories()
        if len(product_categories) == 1:
            category = product_categories[0]
        else:
            last_category = request.session.get("last_category")

            if last_category is None:
                return product_categories[0]

            category = None
            if last_category in product_categories:
                category = last_category
            if category is None:
                category = product_categories[0]
    except IndexError:
        return None
    else:
#        request.session["last_category"] = category
        return category


def parse_item(offer):
    for item_offer in offer:
        if item_offer.tag == u'Артикул':
            print item_offer.tag, item_offer.text
            sku = item_offer.text
        elif item_offer.tag == u'Наименование':
            print item_offer.tag, item_offer.text
            name_full = item_offer.text
        elif item_offer.tag == u'Цены':
            pr = item_offer.xpath(u'./Цена/ЦенаЗаЕдиницу') # Справка по ХPAth Все элементы <Цена/ЦенаЗаЕдиницу> текущего контекста.
            print pr[0].tag, pr[0].text
            price = float(pr[0].text)
    from pytils.translit import slugify
    print 'Add new product: %s' % name_full 
    new_product = Product(name=name_full,sku=sku,price=price,slug=slugify(name_full))
    new_product.save()

def handle_cvs_import_product(f):
    """ Import product from csv file
    """
#    import csv
#    reader = csv.reader(f)
#    for row in reader:
#        print row
    xmldoc = etree.parse(f)
    offers = xmldoc.xpath(u'/КоммерческаяИнформация/ПакетПредложений/Предложения/Предложение')
    for offer in offers:
        parse_item(offer)


def list_nav_cat():
    list_nav = []
    root_cat = Category.objects.filter(level=0)
    for item in root_cat:
        list_nav.append(item)
        sub_category = Category.objects.filter(parent=item)
        if sub_category.count > 0:
            list_subitem = []
            for subitem in sub_category:
                list_subitem.append(subitem)
            list_nav.append(list_subitem)
    return list_nav

