import cdecorator


@cdecorator.transpile
def C():
    def main() -> int:
        return 7
print(C)


@cdecorator.compile
def D():
    def main() -> int:
        return 7
print(D.main())
print(type(D.main))


@cdecorator.compile
def E():
    __include__("<stdio.h>")
    def main() -> int:
        print("hello world\\n")
        return 0
E.main()
