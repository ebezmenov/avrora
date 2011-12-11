from django.db import models
from sorl.thumbnail import ImageField

# Create your models here.
class Category(models.Model):
    """A category is used to browse through the shop products. A category can
    have one parent category and several child categories.

    Parameters:

        - name:
            The name of the category.

        - slug
            Part of the URL

        - parent
            Parent of the category. This is used to create a category tree. If
            it's None the category is a top level category.

        - show_all_products
           If True the category displays it's direct products as well as products
           of it's sub categories. If False only direct products will be
           displayed.

         - products
            The assigned products of the category.

         - short_description
            A short description of the category. This is used in overviews.

         - description
            The description of the category. This can be used in details views
            of the category.

        - image
            The image of the category.

        - position
            The position of the category within the shop resp. the parent
            category.

        - static_block
            A assigned static block to the category.

        - active_formats
            If True product_rows, product_cols and category_cols are taken from
            the category otherwise from the parent.

        - product_rows, product_cols, category_cols
            Format information for the category views

        - meta_title
            Meta title of the category (HTML title)

        - meta_keywords
            Meta keywords of the category

        - meta_description
           Meta description of the category

        - uuid
           The unique id of the category

        - level
           The level of the category within the category hierachie, e.g. if it
           is a top level category the level is 1.

        - template
           Sets the template which renders the category view. If left to None, default template is used.

    """
    name = models.CharField(u"Name", max_length=50)
    slug = models.SlugField(u"Slug",unique=True)
    parent = models.ForeignKey("self", verbose_name=u"Parent", blank=True, null=True)

    # If selected it shows products of the sub categories within the product
    # view. If not it shows only direct products of the category.
    show_all_products = models.BooleanField(u"Show all products",default=True)

    products = models.ManyToManyField("Product", verbose_name=u"Products", blank=True, related_name="categories")
    short_description = models.TextField(u"Short description", blank=True)
    description = models.TextField(u"Description", blank=True)
    
    position = models.IntegerField(u"Position", default=1000)
    
    active_formats = models.BooleanField(u"Active formats", default=False)

    product_rows  = models.IntegerField(u"Product rows", default=3)
    product_cols  = models.IntegerField(u"Product cols", default=3)
    category_cols = models.IntegerField(u"Category cols", default=3)

    meta_title = models.CharField(u"Meta title", max_length=100, default="<name>")
    meta_keywords = models.TextField(u"Meta keywords", blank=True)
    meta_description = models.TextField(u"Meta description", blank=True)
    
    image = ImageField(upload_to = 'image/', blank=True)

    level = models.PositiveSmallIntegerField(default=1)
    class Meta:
        ordering = ("position", )
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug)
    
    def get_absolute_url(self):
        """Returns the absolute_url.
        """
        return ("avrora.catalog.views.category_view", (), {"slug" : self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_children(self):
        """Returns the first level child categories.
        """
        categories = Category.objects.filter(parent=self.id)
        return categories
    
    def get_root_parent(self):
        """ Returns root category
        """
        parent = self
        while parent.parent is not None:
            parent = parent.parent
        return parent
    
    def get_products(self):
        products = self.products.filter(active=True)
        return products


class Manufacturer(models.Model):
    """The manufacturer is the unique creator of a product.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class ProductManager(models.Manager):
    def active(self, **kwarqs):
        return self.filter(active=True, **kwarqs)

class Product(models.Model):
    """ A product is a sold in shop
    Parameters:
        - name
            the name of the product
        - slug
            the part of the URL 
        - sku
            The external unique id of the product

        - price
            The gross price of the product

        - effective_price:
            Only for internal usage (price filtering).

        - unit
            The unit of the product. This is displayed beside the quantity
            field.

        - price_unit
            The unit of the product's price. This is displayed beside the price

        - short_description
            The short description of the product. This is used within overviews.

        - description
            The description of the product. This is used within the detailed view
            of the product.

        - images
            The images of the product.

        - meta_title
            the meta title of the product (the title of the HTML page).

        - meta_keywords
            the meta keywords of the product.

        - meta_description
            the meta description of the product.

        - for_sale
            If True the product is for sale and the for sale price will be
            displayed.

        - active
            If False the product won't be displayed to shop users.

        - creation_date
            The creation date of the product

        - deliverable
            If True the product is deliverable. Otherwise not.

        - manual_delivery_time
            If True the delivery_time of the product is taken. Otherwise the
            delivery time will be calculate on global delivery times and
            selected shipping method.

        - delivery_time
            The delivery time of the product. This is only relevant if
            manual_delivery_time is set to true.

        - order_time
            Order time of the product when no product is within the stock. This
            is added to the product's delivery time.

        - ordered_at
            The date when the product has been ordered. To calculate the rest of
            the order time since the product has been ordered.

        - manage_stock_amount
            If true the stock amount of the product will be decreased when a
            product has been saled.

        - weight, height, length, width
            The dimensions of the product relevant for the the stock (IOW the
            dimension of the product's box not the product itself).

        - static_block
            A static block which has been assigned to the product.

        - sub_type
            Sub type of the product. At the moment that is standard, product with
            variants, variant.

        - default_variant
            The default variant of a product with variants. This will be
            displayed at first if the shop customer browses to a product with
            variant.

        - variants_display_type
            This decides howt the variants of a product with variants are
            displayed. This is select box of list.

        - parent
            The parent of a variant (only relevant for variants)

        - active_xxx
            If set to true the information will be taken from the variant.
            Otherwise from the parent product (only relevant for variants)

        - template
            Sets the template, which renders the product content. If left to None, default template is used.

        - active_price_calculation
            If True the price will be calculated by the field price_calculation

        - price_calculation
            Formula to calculate price of the product.

        - sku_manufacturer
            The product's article ID of the manufacturer (external article id)

        - manufacturer
            The manufacturer of the product.
    """
    name = models.CharField(u"Name", max_length=80, blank=True)
    slug = models.SlugField(u"Slug", unique=True, max_length=80)
    sku = models.CharField(u"SKU", unique=True, max_length=30)
    price = models.FloatField(u"Price", default=0.0)
    unit = models.CharField(blank=True, max_length=20)
    short_description = models.TextField(u"Short description", blank=True)
    description = models.TextField(u"Description", blank=True)
    active = models.BooleanField(u"Active", default=False)
    creation_date = models.DateTimeField(u"Creation date", auto_now_add=True)
    
    # Manufacturer
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, related_name="products")
    # Stocks
    manage_stock_amount = models.BooleanField(u"Manage stock amount", default=False)
    stock_amount = models.FloatField(u"Stock amount", default=0)
    class Meta:
        ordering = ("name", )
        
    admin_objects = models.Manager()
    objects = ProductManager()
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug) 
    
    @models.permalink
    def get_absolute_url(self):
        """Returns the absolute_url.
        """
        return ("avrora.catalog.views.product_detail", (), {"slug" : self.slug})
        
    def get_categories(self, with_parents=False):
        """Returns the categories of the product.
        """
        object = self
        if with_parents:
            categories = []
            for category in object.categories.all():
                while category:
                    categories.append(category)
                    category = category.parent
            categories = categories
        else:
            categories = object.categories.all()

        return categories

    def get_category(self):
        """Returns the first category of a product.
        """
        object = self
        try:
            return object.get_categories()[0]
        except IndexError:
            print 'Cat is NONe'
            return None
    
    def get_name(self):
        return self.name
    
    def get_image(self):
        image = None;
        cat = self.get_category()
        image = cat.image
        return image
    
    def get_description(self):
        if not self.description :
            self.description = self.get_category().description
        return self.description

