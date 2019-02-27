#!/usr/bin/env python
import cdecorator

@cdecorator.compile
def main():
    __include__('<stdio.h>')

    def xyz(x : float) -> float:
        print("lolercode\\n")
        y : int = 4
        return x*y

    def main() -> int:
        print("%f\\n", xyz(2.123))
        print("Hello, World!\\n")
        return 0


if __name__ == '__main__':
    print(main.main())
