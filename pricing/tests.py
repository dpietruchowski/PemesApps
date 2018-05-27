import pdb
from django.test import TestCase
from .models import Group, Element, Product, Component

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="P1")
        Product.objects.create(name="P2")
        Product.objects.create(name="P3")

    def test_is_component(self):
        p1 = Product.objects.get(name="P1")
        p2 = Product.objects.get(name="P2")
        p3 = Product.objects.get(name="P3")
        self.assertEqual(p1.is_component, False)
        self.assertEqual(p2.is_component, False)
        self.assertEqual(p3.is_component, False)

        
class ComponentTestCase(TestCase):
    def setUp(self):
        Component.objects.create(name="C1")
        Component.objects.create(name="C2")
        Component.objects.create(name="C3")

    def test_is_component(self):
        c1 = Component.objects.get(name="C1")
        c2 = Component.objects.get(name="C2")
        c3 = Component.objects.get(name="C3")
        self.assertEqual(c1.is_component, True)
        self.assertEqual(c2.is_component, True)
        self.assertEqual(c3.is_component, True)


class ComponentTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="P1")
        Product.objects.create(name="P2")
        Product.objects.create(name="P3")
        Component.objects.create(name="C1")
        Component.objects.create(name="C2")
        Component.objects.create(name="C3")

    def test_add_product(self):
        p1 = Product.objects.get(name="P1")
        p2 = Product.objects.get(name="P2")
        p3 = Product.objects.get(name="P3")
        c1 = Component.objects.get(name="C1")
        c1.add_child(p1, 10)
        c1.add_child(p2, 11)
        c1.add_child(p3, 12)
        self.assertEqual(c1.relationship.all().count(), 3)
        self.assertEqual(c1.has_cycle(set()), False)

    def test_add_component(self):
        c1 = Component.objects.get(name="C1")
        c2 = Component.objects.get(name="C2")
        c3 = Component.objects.get(name="C3")
        c1.add_child(c2, 10)
        c1.add_child(c3, 11)
        self.assertEqual(c1.relationship.all().count(), 2)
        self.assertEqual(c1.has_cycle(set()), False)

    def test_add_element(self):
        c1 = Component.objects.get(name="C1")
        c2 = Component.objects.get(name="C2")
        c3 = Component.objects.get(name="C3")
        p1 = Product.objects.get(name="P1")
        p2 = Product.objects.get(name="P2")
        p3 = Product.objects.get(name="P3")
        c1.add_child(c2, 10)
        c1.add_child(c3, 11)
        c1.add_child(p1, 12)
        c1.add_child(p2, 13)
        c1.add_child(p3, 14)
        self.assertEqual(c1.relationship.all().count(), 5)
        self.assertEqual(c1.has_cycle(set()), False)

    def test_self_cycle(self):
        c1 = Component.objects.get(name="C1")
        c1.add_child(c1, 10)
        self.assertEqual(c1.has_cycle(set()), True)

    def test_simple_cycle(self):
        c1 = Component.objects.get(name="C1")
        c2 = Component.objects.get(name="C2")
        c1.add_child(c2, 10)
        c2.add_child(c1, 11)
        self.assertEqual(c1.has_cycle(set()), True)
        self.assertEqual(c2.has_cycle(set()), True)

class UpdateChildrenTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="P1")
        Product.objects.create(name="P2")
        Product.objects.create(name="P3")
        Component.objects.create(name="C1")
        Component.objects.create(name="C2")
        Component.objects.create(name="C3")

    def first_update(self):
        p1 = Product.objects.get(name="P1")
        p2 = Product.objects.get(name="P2")
        p3 = Product.objects.get(name="P3")
        c1 = Component.objects.get(name="C1")
        c2 = Component.objects.get(name="C2")
        c3 = Component.objects.get(name="C3")
        relationship_dict = {
            p1.pk: 10,
            p2.pk: 11,
            p3.pk: 12,
            c2.pk: 14,
            c3.pk: 15,
        }
        c1.update_children(relationship_dict)

    def test_first_update(self):
        self.first_update()
        c1 = Component.objects.get(name="C1")
        self.assertEqual(c1.relationship.all().count(), 5)

    def test_new_empty_update(self):
        self.first_update()
        c1 = Component.objects.get(name="C1")
        c1.update_children({})
        self.assertEqual(c1.relationship.all().count(), 0)

    def test_more_new(self):
        pass

    def test_more_old(self):
        pass

    def test_equal_old_new(self):
        pass

    def test_separable_old_new(self):
        pass

    def test_simple_cycle(self):
        c1 = Component.objects.get(name="C1")
        c2 = Component.objects.get(name="C2")
        c1.add_child(c2, 10)
        relationship_dict = { c1.pk: 11 }
        c2.update_children(relationship_dict)
        self.assertEqual(c1.has_cycle(set()), False)
        self.assertEqual(c1.relationship.all().count(), 1)
        self.assertEqual(c2.relationship.all().count(), 0)


class GetAllProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="P1")
        Product.objects.create(name="P2")
        Product.objects.create(name="P3")
        Component.objects.create(name="C1")
        Component.objects.create(name="C2")
        Component.objects.create(name="C3")

    def test_1(self):
        p1 = Product.objects.get(name="P1")
        p2 = Product.objects.get(name="P2")
        p3 = Product.objects.get(name="P3")
        c1 = Component.objects.get(name="C1")
        c2 = Component.objects.get(name="C2")
        c3 = Component.objects.get(name="C3")
        relationship_dict1 = {
            c2.pk: 14,
            c3.pk: 15,
        }
        relationship_dict2 = {
            p1.pk: 10,
            p2.pk: 11,
        }
        relationship_dict3 = {
            p3.pk: 12,
        }
        c1.update_children(relationship_dict1)
        c2.update_children(relationship_dict2)
        c3.update_children(relationship_dict3)
        self.assertEqual(c1.relationship.all().count(), 2)
        self.assertEqual(c2.relationship.all().count(), 2)
        self.assertEqual(c3.relationship.all().count(), 1)
        products1 = c1.get_all_products(1)
        products2 = c2.get_all_products(1)
        products3 = c3.get_all_products(1)
        self.assertEqual(len(products3), 1)
        self.assertEqual(products3[0]['object'].name, "P3")
        self.assertEqual(products3[0]['amount'], 12)
        self.assertEqual(len(products2), 2)
        self.assertEqual(products2[0]['object'].name, "P1")
        self.assertEqual(products2[0]['amount'], 10)
        self.assertEqual(products2[1]['object'].name, "P2")
        self.assertEqual(products2[1]['amount'], 11)
        self.assertEqual(len(products1), 3)
        self.assertEqual(products1[0]['object'].name, "P1")
        self.assertEqual(products1[0]['amount'], 140)
        self.assertEqual(products1[1]['object'].name, "P2")
        self.assertEqual(products1[1]['amount'], 154)
        self.assertEqual(products1[2]['object'].name, "P3")
        self.assertEqual(products1[2]['amount'], 180)


    
