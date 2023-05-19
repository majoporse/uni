from typing import Generator, Union


def drink_machine(coffee_price: int, tea_price: int,
                    milk_price: int, sugar_price: int) -> Generator[Union[str, int], bool, None]:
    
    price = 0
    while (yield "Another drink?"):

        if (yield "Coffee (True) or tea (False)?"):
            price += coffee_price
            if (yield "Milk?"):
                price += milk_price
            if (yield "Sugar?"):
                price += sugar_price
        else:
            price += tea_price
            if (yield "Milk?"):
                price += milk_price



    yield price


if __name__ == "__main__":
    order = drink_machine(15, 10, 5, 3)
    
    assert next(order) == "Another drink?"
    assert order.send(True) == "Coffee (True) or tea (False)?"
    assert order.send(True) == "Milk?"
    assert order.send(False) == "Sugar?"
    assert order.send(True) == "Another drink?"
    assert order.send(True) == "Coffee (True) or tea (False)?"
    assert order.send(False) == "Milk?"
    assert order.send(True) == "Another drink?"
    assert order.send(False) == 33