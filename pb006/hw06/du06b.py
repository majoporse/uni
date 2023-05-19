# You must not modify these exception classes and their inheritance relations.
class ExceptionA (Exception):
    pass


class ExceptionB (Exception):
    pass


class ExceptionAB (ExceptionA, ExceptionB):
    pass
# end of exception classes


def test(n: int, x: int) -> int:
    # You can change body of this function to throw any exception or behave in
    # other ways. It will be replaced by the tests.
    return n + x


# You must not change the function headers, the function calls inside nor their
# arguments. In case of no exceptions, your modified functions must return the
# same values as the originals.
def keepB(n: int) -> int:
    print(f"entering keepB({n})")
    
    try:
        try:
            x = foo(n)
        except ExceptionAB as e:
            raise e
        except ExceptionA:
            x = 42
            print("ExceptionA caught in keepB")


        try:
            y = bar(x, n)
        except ExceptionAB as e:
            raise e
        except ExceptionA:
            y = 28
            print("ExceptionA caught in keepB")

    except ExceptionAB as e:
            print("ExceptionAB propagated from keepB as ExceptionB")
            raise ExceptionB()

    except ExceptionB as e:
        print("ExceptionB propagated from keepB")
        raise e

    finally:
        print("leaving keepB")
    
    return x + y


def foo(n: int) -> int:
    print(f"entering foo({n})")
    
    try:
        res = bar(n, 0)
    except ExceptionAB:
        print("ExceptionAB caught in foo")
        res = 14
    except (ExceptionA, ExceptionB) as e:
        print("exception propagated from foo")
        raise e
    finally:
        print("leaving foo")
    
    
    return res


def bar(n: int, x: int) -> int:
    print(f"entering bar({n}, {x})")
    
    try:
        res = test(n, x)
    except (ExceptionA, ExceptionB, ExceptionAB) as e:
        print("exception propagated from bar")
        raise e
    finally:
        print("leaving bar")
    
    return res
