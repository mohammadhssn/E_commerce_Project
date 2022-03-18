from apps.catalogue.models import ProductInventory
from apps.checkout.models import DeliveryOption

BASKET_SESSION_KEY = 'basket'


class Basket:
    """
        A Base Basket Class, providing some default behaviors that
        can be inherited or overridden, as necessary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(BASKET_SESSION_KEY)
        if BASKET_SESSION_KEY not in request.session:
            basket = self.session[BASKET_SESSION_KEY] = {}
        self.basket = basket

    def add(self, product, qty):
        """
            Adding and updating the users basket session data
        """

        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.store_price), 'qty': qty}

        self.save()

    def __len__(self):
        """
            Get the basket data and count the qty of item
        """

        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        """
            Collect the product_id in the session data to query the database and return products
        """

        product_ids = self.basket.keys()
        products = ProductInventory.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_subtotal_price(self):
        return sum(int(item['price']) * item['qty'] for item in self.basket.values())

    def get_total_price(self):
        sub_total = sum(int(item['price']) * item['qty'] for item in self.basket.values())
        new_price = 0

        if 'purchase' in self.session:
            new_price = DeliveryOption.objects.get(id=self.session['purchase']['delivery_id']).delivery_price

        total = sub_total + int(new_price)

        return total

    def get_delivery_price(self):
        new_price = 0

        if 'purchase' in self.session:
            new_price = DeliveryOption.objects.get(id=self.session['purchase']['delivery_id']).delivery_price

        return new_price

    def basket_update_delivery(self, delivery_price=0):
        subtotal = sum(int(item['price']) * item['qty'] for item in self.basket.values())
        total = subtotal + int(delivery_price)
        return total

    def delete(self, product):
        """
            Delete item from session data
        """

        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        """
            update quantity item from session data
        """

        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        """
            Clear session
        """

        del self.session[BASKET_SESSION_KEY]
        del self.session['address']
        del self.session['purchase']
        self.save()
