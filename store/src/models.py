from django.db import models


class Product(models.Model):
    title = models.TextField()
    category = models.TextField()
    uniq_id = models.TextField(null=True)

    @staticmethod
    def get_product(asked_id: int):
        return Product.objects.get(id=asked_id)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
