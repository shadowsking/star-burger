from rest_framework.fields import ListField
from rest_framework.serializers import ModelSerializer

from .models import Order, Product


class OrderSerializer(ModelSerializer):
    products = ListField(allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']

    def create(self):
        order = Order.objects.create(
            firstname=self.initial_data['firstname'],
            lastname=self.initial_data['lastname'],
            phonenumber=self.initial_data['phonenumber'],
            address=self.initial_data['address']
        )
        for product in self.initial_data['products']:
            product_instance = Product.objects.get(id=product['product'])
            order.products.create(
                product=product_instance,
                order=order,
                quantity=product['quantity'],
                price=product_instance.price
            )

        return order
