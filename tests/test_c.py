import unittest
import cdecorator

from . import strip

PRT = """
void main() {
    printf("Hello, world!\\n");
    return 0;
}
"""
def prt():
    def main():
        print('Hello, world!\\n')
        return 0



TWO_ARGS = """
float xyz(float x, int z) {
    printf("lolercode\\n");
    int y = 4;
    return x * y * z;
}
"""
def two_args():
    def xyz(x : float, z : int) -> float:
        print("lolercode\\n")
        y : int = 4
        return x*y*z


class MathTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(strip(act.strip()), strip(exp.strip()))

    def test_prt(self):
        self.eqcode(PRT, cdecorator.transpile(prt))

    def test_two(self):
        self.eqcode(TWO_ARGS, cdecorator.transpile(two_args))


if __name__ == '__main__':
    unittest.main()
