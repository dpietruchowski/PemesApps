from django.db import models

class Product(models.Model):
	name = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	dependency = models.ManyToManyField("self", symmetrical=False, blank=True);
