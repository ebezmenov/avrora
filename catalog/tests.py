#-*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from avrora.catalog.models import Product


class SimpleTest(TestCase):
    def setUp(self):
        self.p1 = Product.objects.create(name=u'Шланг Transair 32 мм', slug='transair', price=5, active=True)
        
    def test_get_name(self):
        self.assertEqual(self.p1.name,u'Шланг Transair 32 мм')
         
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
