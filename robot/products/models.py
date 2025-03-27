from django.db import models



class DiscountGroup(models.Model):
    title = models.CharField(unique=True, max_length=100)
    meta = models.TextField(max_length=400, blank=True)
    amount = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title + ' - ' + self.amount


class IntDetail(models.Model):
    title = models.CharField(max_length=255)
    value = models.IntegerField()


class FloatDetail(models.Model):
    title = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return self.title


class Detail(models.Model):
    title = models.CharField(max_length=255)
    value = models.TextField(max_length=500)

    def __str__(self):
        return self.title


class Product(models.Model):
    """Product model."""
    STATUSES = (
        ('P', "Published"),
        ('D', "Draft"),
        ('A', "Archived")
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    meta = models.TextField(max_length=400)
    description = models.TextField()
    org_price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField("products/thumbnail/%Y-%m/")

    status = models.CharField(max_length=1, choices=STATUSES, default='F')
    is_exist = models.BooleanField(default=False)

    images = models.ManyToManyField("medstore.Image")
    videos = models.ManyToManyField("medstore.Video")
    tags = models.ManyToManyField("sort.Tag")
    categories = models.ManyToManyField("sort.Category")
    detailes = models.ManyToManyField(Detail)
    float_detailes = models.ManyToManyField(FloatDetail)
    int_details = models.ManyToManyField(IntDetail)
    Purchases = models.PositiveIntegerField(default=1)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    discount = models.SmallIntegerField(default=0)
    discount_group = models.ForeignKey(DiscountGroup, on_delete=models.DO_NOTHING, blank=True)


    def __str__(self):
        return self.title + ' | ' + self.created_at

    @property
    def get_sell_price(self):
        min = self.org_price * ((100-self.discount)/100)
        if self.discount_group:
            group_price = self.org_price * ((100-self.discount_group.amount)/100)
            if min>group_price:
                min = group_price
        return min


class Ad(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title
