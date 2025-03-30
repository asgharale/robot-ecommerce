from django.db import models


class OrderItem(models.Model):
    """Order item for order list."""
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, blank=False, null=False)


# class order(models.Model):
    