from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F
from phonenumber_field.modelfields import PhoneNumberField


class OrderQuerySet(models.QuerySet):
    def orders(self, excluded_statuses=None):
        return (
            self.annotate(amount=Sum(F('products__price') * F("products__quantity")))
            .exclude(status__in=excluded_statuses or [])
            .order_by("id")
        )


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        accepted = ('Принят',) * 2
        preparing = ('Готовится',) * 2
        delivery = ('Доставка',) * 2
        delivered = ('Доставлен',) * 2
        cancelled = ('Отменен',) * 2

    firstname = models.CharField(
        'имя',
        max_length=50
    )
    lastname = models.CharField(
        'фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField('номер телефона', db_index=True)
    address = models.CharField(
        max_length=50,
        verbose_name='адрес'
    )
    status = models.CharField(
        'статус заказа',
        max_length=50,
        choices=Status.choices,
        default=Status.accepted,
        db_index=True
    )
    comment = models.TextField(
        verbose_name='комментарий',
        blank=True
    )

    objects = OrderQuerySet().as_manager()

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.lastname} {self.firstname}'


class OrderedProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='продукт',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='заказ',
    )
    quantity = models.IntegerField(
        verbose_name='количество',
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = 'заказанные продукты'

    def __str__(self):
        return f"{self.order} {self.product} {self.quantity}"
