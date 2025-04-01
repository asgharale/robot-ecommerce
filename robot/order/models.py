from django.db import models


class Order(models.Model):
    ORDER_STATUS = (
        ('P', 'Pending'),
        ('PR', 'Processing'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
        ('R', 'Refunded'),
    )

    customer = models.ForeignKey("user.CUser", on_delete=models.SET_NULL, null=True, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=2, choices=ORDER_STATUS, default='P')
    billing_address = models.ForeignKey("user.Address", on_delete=models.SET_NULL, null=True, related_name='billing_orders')
    shipping_address = models.ForeignKey("user.Address", on_delete=models.SET_NULL, null=True, related_name='shipping_orders')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    """Order item for order list."""
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, blank=False, null=False)
    product_name = models.CharField(max_length=200)  # Store product name in case product is deleted
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of purchase
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in order {self.order.order_number}"


