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
            firstname=self.validated_data['firstname'],
            lastname=self.validated_data['lastname'],
            phonenumber=self.validated_data['phonenumber'],
            address=self.validated_data['address']
        )
        for product in self.validated_data['products']:
            product_instance = Product.objects.get(id=product['product'])
            order.products.create(
                product=product_instance,
                order=order,
                quantity=product['quantity'],
                price=product_instance.price
            )

        return order
