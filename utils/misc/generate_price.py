async def generate_amount_price(price) -> int:
    price = list(str(price)); price.append('00')

    amount = int(''.join(x for x in price))
    return amount
