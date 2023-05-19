# Napište predikát, který ověří, zda je číslo ‹number› palindrom,
# zapíšeme-li jej v desítkové soustavě. Palindrom se vyznačuje tím,
# že je stejný při čtení zleva i zprava.

def is_palindrome(number):
    positions = 0
    n = number
    while n>0:
        positions +=1
        n//=10
    for i in range(positions):
        if (number //10**i)%10 != (number//10**(positions-1-i))%10:
            return False
    return True

def main():
    assert is_palindrome(7)
    assert is_palindrome(1221)
    assert is_palindrome(12121)
    assert not is_palindrome(1212)
    assert not is_palindrome(12345)


if __name__ == "__main__":
    main()
