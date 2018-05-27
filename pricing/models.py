from datetime import date
from enum import Enum

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

import pdb

class Group(Enum):
    Mechanical = 0
    Electrical = 1

    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name

class Element(models.Model):
    name = models.CharField(max_length=30)
    group = models.IntegerField(choices=Group.choices(), default=Group.Electrical)
    is_component = models.BooleanField()

    def __init__(self, *args, **kwargs):
        super(Element, self).__init__(*args, **kwargs)
        if not self.pk and not self.is_component:
            self.is_component = self.IS_COMPONENT


class Product(Element):
    IS_COMPONENT = False
    element = models.OneToOneField(
        to=Element, 
        parent_link=True, 
        related_name='product',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        default=0,
        validators=[MinValueValidator(0)]
    ) 
    
    def get_all_products(self, amount):
        products = [{"amount": amount, "object": self}]
        return products


class Component(Element):
    IS_COMPONENT = True
    element = models.OneToOneField(
        to=Element, 
        parent_link=True, 
        related_name='component',
        on_delete=models.CASCADE
    )
    project_name = models.CharField(max_length=30, default="")

    def add_child(self, child, amount):
        self.relationship.create(
            child=child,
            amount=amount
        )

    def set_child(self, child, amount):
        relation = self.relationship.filter(child=child).first()
        relation.amount = amount
        relation.save()

    def delete_child(self, child):
        self.relationship.filter(child=child).delete()

    def update_child(self, child, amount):
        if self.relationship.filter(child=child).exists():
            self.set_child(child, amount)
        else:
            self.add_child(child, amount)

    def update_children(self, relationship_dict):
        old_children = dict()
        new_children = set()
        for relation in self.relationship.all():
            old_children.update({relation.child.pk: relation.amount})

        for child_id, amount in relationship_dict.items():
            new_children.update({child_id})
            child = Element.objects.get(pk=child_id)
            self.update_child(child, amount)

        for child_id in set(old_children.keys()).difference(new_children):
            self.delete_child(Element.objects.get(pk=child_id))

        if self.has_cycle(set()):
            self.update_children(old_children)
            return False
        
        return True

    def get_all_products(self, amount):
        products = []
        for relation in self.relationship.all():
            child = relation.child
            if child.is_component:
                products.extend(
                    child.component.get_all_products(
                        relation.amount * amount
                    )
                )
            else:
                products.extend(
                    child.product.get_all_products(
                        relation.amount * amount
                    )
                )
        return products

    def has_cycle(self, visited):
        #pdb.set_trace()
        for relation in self.relationship.all():
            if relation.pk in visited:
                return True
            visited.add(relation.pk)
            if relation.child.is_component:
                if relation.child.component.has_cycle(visited):
                    return True
        return False


class ElementRelationship(models.Model):
    parent = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name="relationship"
    )
    child = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()
    class Meta:
        unique_together = ('parent', 'child')
