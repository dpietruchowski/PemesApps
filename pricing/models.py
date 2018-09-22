from datetime import date
from enum import Enum

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

import pdb

class Relationship:
    def add_child(self, child, amount):
        self.relationship_model.create(
            child=child,
            amount=amount
        )

    def set_child(self, child, amount):
        relation = self.relationship_model.filter(child=child).first()
        relation.amount = amount
        relation.save()

    def delete_child(self, child):
        self.relationship_model.filter(child=child).delete()

    def update_child(self, child, amount):
        if self.relationship_model.filter(child=child).exists():
            self.set_child(child, amount)
        else:
            self.add_child(child, amount)

    def update_children(self, relationship_dict):
        old_children = dict()
        new_children = set()
        for relation in self.relationship_model.all():
            old_children.update({relation.child.pk: relation.amount})

        for child_id, amount in relationship_dict.items():
            new_children.update({child_id})
            print(relationship_dict)
            child = self.child_model.objects.get(pk=child_id)
            self.update_child(child, amount)

        for child_id in set(old_children.keys()).difference(new_children):
            self.delete_child(self.child_model.objects.get(pk=child_id))

        if self.has_cycle(set()):
            print("relationship has cycle")
            self.update_children(old_children)
            return False
        
        return True

    def has_cycle(self, visited):
        #pdb.set_trace()
        for relation in self.relationship_model.all():
            if relation.child.is_component:
                if relation.pk in visited:
                    return True
                visited.add(relation.pk)
                if relation.child.component.has_cycle(visited):
                    return True
        return False

class Group(Enum):
    Mechanical = "Mechanika"
    Electrical = "Elektryka"
    Pneumatics = "Pneumatyka"

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

class Element(models.Model):
    name = models.CharField(max_length=30)
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
    brand = models.CharField(max_length=30)
    group = models.CharField(
        max_length=30, 
        choices=Group.choices(), 
        default=Group.Electrical
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    def get_all_products(self, amount, component):
        products = [{"amount": amount, "object": self, "component": component}]
        return products


class Project(models.Model, Relationship):
    name = models.CharField(max_length=30)
    leader = models.CharField(max_length=35)
    description = models.TextField()
    
    class Meta:
        unique_together = ['name', 'leader']

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.relationship_model = self.components
        self.child_model = Component

    def get_all_products(self):
        products = []
        for relation in self.components.all():
            child = relation.child
            products.extend(
                child.get_all_products(
                    relation.amount * 1, child
                )
            )
        return products
        

class Component(Element, Relationship):
    IS_COMPONENT = True
    element = models.OneToOneField(
        to=Element, 
        parent_link=True, 
        related_name='component',
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="related_components",
        blank=True, null=True
    )

    def __init__(self, *args, **kwargs):
        super(Component, self).__init__(*args, **kwargs)
        self.relationship_model = self.relationship
        self.child_model = Element

    def get_all_products(self, amount, component):
        products = []
        for relation in self.relationship.all():
            child = relation.child
            if child.is_component:
                products.extend(
                    child.component.get_all_products(
                        relation.amount * amount, component
                    )
                )
            else:
                products.extend(
                    child.product.get_all_products(
                        relation.amount * amount, component
                    )
                )
        return products


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

    def get_id(self):
        return self.child.id

    def get_name(self):
        return self.child.name

    def get_amount(self):
        return self.amount

    class Meta:
        unique_together = ('parent', 'child')


class ProjectComponent(models.Model):
    parent = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="components"
    )
    child = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()

    def get_id(self):
        return self.child.id

    def get_name(self):
        return self.child.name

    def get_amount(self):
        return self.amount

