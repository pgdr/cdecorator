import unittest
import cdecorator


VAR = """
attribute float x;
"""
def var():
    x : Attribute[float]



VARS = """
attribute float x;
attribute float y;
attribute float intensity;
varying float v_intensity;
"""
def vars_():
    x : Attribute[float]
    y : Attribute[float]
    intensity : Attribute[float]
    v_intensity : Varying[float]


FUN = """
void main() {
return 0;
}
"""
def fun():
    def main() -> void:
        return 0





class CDecoratorTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(act.strip(), exp.strip())

    def test_var(self):
        self.eqcode(VAR, cdecorator.transpile(var))

    def test_vars(self):
        self.eqcode(VARS, cdecorator.transpile(vars_))

    def test_fun(self):
        self.eqcode(FUN, cdecorator.transpile(fun))


if __name__ == '__main__':
    unittest.main()
