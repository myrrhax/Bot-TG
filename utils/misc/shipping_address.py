class ShippingAddress:
    """Словарь для хранения адреса"""
    def __init__(self, city: str, street: str, post_address: int, comment: str = None):
        self.city = city
        self.street = street
        self.post_address = post_address
        self.comment = comment
        self.shipping_info = dict()
        self.info = '\n'

    def generate_shipping_query(self):
        # Сделал вывод в таком виде:
        self.shipping_info.update({'Город': self.city, 'Улица': self.street,
                                   'Адрес': self.post_address,
                                   'Комментарий': self.comment})
        self.info = "\n".join("{}: {}".format(k, v) for k, v in self.shipping_info.items())
        return self.info
