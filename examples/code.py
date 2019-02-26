#!/usr/bin/env python
import cdecorator

@cdecorator.compile
def main():
    __include__('<stdio.h>')
    def main() -> int:
        printf("Hello, World!\\n")
        return 0


if __name__ == '__main__':
    print(main.main())
