from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

CATEGORY_CHOICES = [('other', 'Другой'), ('phone', 'Телефоны'), ('notebook', 'Ноутбуки'), ('tv', 'телевизоры'),
                    ('tablet', 'планшеты')]


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название')
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='other', verbose_name='Категории')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return f"{self.pk}, {self.title}, {self.category}, {self.description}, {self.image}"

    def get_absolute_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.pk})

    def get_average(self):
        product = Product.objects.get(pk=self.pk)
        average = 0
        avg_list = []
        for review in product.product_reviews.all():
            if review.moderated:
                average += review.grade
                avg_list.append(review.grade)
        if average:
            return average / len(avg_list)
        return average

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, blank=False,
                               related_name='users')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='product_reviews')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    grade = models.PositiveIntegerField(verbose_name='Оценка')
    moderated = models.BooleanField(verbose_name='модерировано', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        permissions = [
            ('can_add_moderated_to_the_review', 'Может модерировать отзыв'),
            ('can_view_moderated_to_the_review', 'Может видеть немодерированные отзывы'),
        ]