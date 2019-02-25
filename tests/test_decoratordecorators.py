import unittest
import cdecorator
from . import strip


VAR = """
attribute float x;
"""
@cdecorator.transpiler('var')
def var():
    x : attribute[float]



VARS = """
attribute float x;
attribute float y;
attribute float intensity;
varying float v_intensity;
"""
@cdecorator.transpiler('vars')
def vars_():
    x : attribute[float]
    y : attribute[float]
    intensity : attribute[float]
    v_intensity : varying[float]




VERTEX = """
attribute float x;
attribute float y;
attribute float intensity;
varying float v_intensity;
v_intensity = intensity;
gl_Position = vec4(x, y, 0.0, 1.0);
"""
@cdecorator.transpiler('vertex')
def vertex():
    x : attribute[float]
    y : attribute[float]
    intensity : attribute[float]
    v_intensity : varying[float]

    #def main() -> void:
    v_intensity = intensity
    gl_Position = vec4(x, y, 0.0, 1.0)





FRAGMENT = """
varying float v_intensity;
void main()
{
    gl_FragColor = vec4(0,v_intensity,0,1);
}
"""
@cdecorator.transpiler('fragment')
def fragment():
    v_intensity : Varying[float]
    gl_FragColor = vec4(0, v_intensity, 0, 1)



class CDecoratorDecoratorsTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(strip(act.strip()), strip(exp.strip()))

    def test_var(self):
        self.eqcode(VAR, var())

    def test_vars(self):
        self.eqcode(VARS, vars_())

    def test_vertex(self):
        self.eqcode(VERTEX, vertex())


if __name__ == '__main__':
    unittest.main()
