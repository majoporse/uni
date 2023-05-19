from turtle import forward, left, right
from math import asin, degrees, sqrt, sin, radians


def house(width, height, roof_angle):
    c = sqrt(height**2 + width**2)
    half_angle = roof_angle/2
    roof_side = width / 2 / sin(radians(half_angle))

    for i in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    left(degrees(asin(height/c)))
    forward(c)
    right(90+degrees(asin(height/c)))
    forward(height)
    right(180-degrees(asin(width/c)))
    forward(c)
    right((180-degrees(asin(height/c)))-90+half_angle)
    forward(roof_side)
    right(180-roof_angle)
    forward(roof_side)


def sum_dd_numbers(first_div, second_div):
    total = 0
    for i in range(10, 100):
        if ((i//10)) % first_div == 0 and (i % 10) % second_div == 0:
            total += i
    return total


def nth_unique_smallest_prime_divisor(num, index):
    primes = 0
    i = 2
    while i <= num**(1/2):
        if num % i == 0:
            primes += 1
            while (num % i) == 0:
                num //= i
            if primes == index:
                return i
        i += 1
    if primes == 0 and index == 1 and num != 1:
        return num


def main():
    # you have to check the output of house yourself
    assert sum_dd_numbers(3, 5) == 375
    assert sum_dd_numbers(2, 6) == 424
    assert sum_dd_numbers(3, 8) == 384
    assert nth_unique_smallest_prime_divisor(3, 1) == 3
    assert nth_unique_smallest_prime_divisor(42350, 2) == 5
    assert nth_unique_smallest_prime_divisor(42350, 3) == 7
    assert nth_unique_smallest_prime_divisor(42350, 4) == 11
    assert nth_unique_smallest_prime_divisor(42350, 5) is None


if __name__ == '__main__':
    main()
