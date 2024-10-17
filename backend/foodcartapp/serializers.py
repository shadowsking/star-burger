from rest_framework.serializers import ModelSerializer

from .models import Order, OrderedProduct


class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderedProduct
        fields = ['product', 'quantity']

    def create(self, **validated_data):
        return OrderedProduct.objects.create(**validated_data)


class OrderSerializer(ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']

    def create(self, products=None, **validated_data):
        order = Order.objects.create(**validated_data)
        for product in products:
            serializer = OrderProductSerializer(product)
            serializer.create(
                order=order,
                price=product['product'].price,
                **product
            )

        return order
