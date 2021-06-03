class ShippingAddressAsDict:
    """Словарь для хранения адреса"""
    def __init__(self, city: str, street: str, post_address: int, region: str):
        self.city = city
        self.street = street
        self.post_code = post_address
        self.region = region
        self.shipping_info = dict()
        self.info = '\n'

    def generate_shipping_query(self):
        # Сделал вывод в таком виде:
        self.shipping_info.update({'Город': self.city, 'Улица': self.street,
                                   'Индекс': self.post_code,
                                   'Область': self.region})
        self.info = "\n".join("{}: {}".format(k, v) for k, v in self.shipping_info.items())
        return self.info
