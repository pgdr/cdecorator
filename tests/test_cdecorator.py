import unittest
import cdecorator
from . import strip

CALL = """
float x = f(3);
"""
def call():
    x : float = f(3)

VAR = """
attribute float x;
"""
def var():
    x : attribute[float]


VARS = """
attribute float x;
attribute float y;
attribute float intensity;
varying float v_intensity;
"""
def vars_():
    x : attribute[float]
    y : attribute[float]
    intensity : attribute[float]
    v_intensity : varying[float]


VARASS = """
const float x = 3.0;
"""
def varass():
    x : const[float] = 3.0


FUN = """
void main() {
float x = f(3);
return x;
}
"""
def fun():
    def main() -> void:
        x : float = f(3)
        return x

VERTEX = """
attribute float x;
attribute float y;
attribute float intensity;
varying float v_intensity;
void main(void) {
    v_intensity = intensity;
    gl_Position = vec4(x, y, 0.0, 1.0);
}
"""
def vertex():
    x : attribute[float]
    y : attribute[float]
    intensity : attribute[float]
    v_intensity : varying[float]
    def main(void) -> void:
        v_intensity = intensity
        gl_Position = vec4(x, y, 0.0, 1.0)


FRAGMENT = """
varying float v_intensity;
void main() {
    gl_FragColor = vec4(0, v_intensity, 0, 1);
}
"""
def fragment():
    v_intensity : varying[float]
    def main() -> void:
        gl_FragColor = vec4(0,v_intensity,0,1)


class CDecoratorTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(strip(act.strip()), strip(exp.strip()))

    def test_call(self):
        self.eqcode(CALL, cdecorator.transpile(call))

    def test_var(self):
        self.eqcode(VAR, cdecorator.transpile(var))

    def test_varass(self):
        self.eqcode(VARASS, cdecorator.transpile(varass))

    def test_vars(self):
        self.eqcode(VARS, cdecorator.transpile(vars_))

    def test_fun(self):
        self.eqcode(FUN, cdecorator.transpile(fun))

    def test_vertex(self):
        self.eqcode(VERTEX, cdecorator.transpile(vertex))

    def test_fragment(self):
        self.eqcode(FRAGMENT, cdecorator.transpile(fragment))


if __name__ == '__main__':
    unittest.main()
