from datetime import date

from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=15
    )

    def add_child(self, child, amount):
        self.children.create(
            child=child,
            amount=amount
        )

    def set_child(self, child, amount):
        child_dependency = self.children.filter(child=child).first()
        child_dependency.amount = amount
        child_dependency.save()

    def delete_child(self, child):
        self.children.filter(child=child).delete()

    def update_child(self, child, amount):
        if self.children.filter(child=child).exists():
            self.set_child(child, amount)
        else:
            self.add_child(child, amount)

    def update_children(self, children_dict):
        old_children = set()
        new_children = set()
        for child in self.children.all():
            old_children.update({child.child.pk})

        for id, amount in children_dict.items():
            new_children.update({id})
            self.update_child(Product.objects.get(pk=id), amount)

        for child_id in old_children.difference(new_children):
            self.delete_child(Product.objects.get(pk=child_id))

    def get_full_dependency(self, amount):
        full_dependency = [{"amount": amount, "object": self}]
        for child in self.children.all():
            full_dependency.extend(child.child.get_full_dependency(child.amount * amount))
        return full_dependency

class ProductDependency(models.Model):
    parent = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="children"
    )
    child = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="parents"
    )
    amount = models.IntegerField()

class Order(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField(default=date.today)
    datetime = models.DateTimeField(default=timezone.now)

    def add_product(self, product):
        pass

class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    amount = models.IntegerField()