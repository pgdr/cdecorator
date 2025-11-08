import cdecorator
import sys


def decorateif(T):
    return cdecorator.compile if T else cdecorator.transpile


comp = True
if len(sys.argv) != 2:
    exit("Usage: forloop c|t")
if sys.argv[1] == "t":
    comp = False


@decorateif(comp)
def C():
    __include__("<stdio.h>")

    def main() -> int:
        v: tuple[int] = (1, 2, 3, 4, 5, 6)
        x: int = 0
        n: int = 6
        for i in (1, 2, 3):
            x += v[i]
            print(x,v[i])
        return x


if comp:
    print(C.main())
else:
    print(C)
