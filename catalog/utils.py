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
    
def handle_cvs_import_product(f):
    """ Import product from csv file
    """
    import csv
    reader = csv.reader(f)
    for row in reader:
        print row
    