import phonenumbers
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def validate(order):
    required_fields = {
        'products': list,
        'firstname': str,
        'lastname': str,
        'phonenumber': str,
        'address': str
    }
    missing_fields = set(required_fields).difference(order)
    if missing_fields:
        return {'error': f'{", ".join(missing_fields)} - required fields'}

    empty_values_fields = list(filter(lambda k: not order.get(k), required_fields))
    if empty_values_fields:
        return {'error': f'{", ".join(empty_values_fields)} - this fields cannot be empty'}

    for field in required_fields:
        if not isinstance(order[field], required_fields[field]):
            continue

        return {'error': f'The key {field} is not {(required_fields[field].__name__)}'}

    for product in order.get('products'):
        if not Product.objects.filter(pk=product['product']):
            return {'error': 'Invalid primary key'}

    parsed_number = phonenumbers.parse(order['phonenumber'], 'RU')
    if not phonenumbers.is_valid_number(parsed_number):
        return {'error': 'Invalid phone number has been entered'}


@api_view(['POST'])
def register_order(request):
    data = request.data
    content = validate(data)
    if content:
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        phonenumber=data['phonenumber'],
        address=data['address']
    )
    for product in data['products']:
        product_instance = Product.objects.get(id=product['product'])
        order.products.create(
            product=product_instance,
            order=order,
            quantity=product['quantity']
        )

    # TODO это лишь заглушка
    return JsonResponse({})
