import unittest
import cdecorator


VAR = """
attribute float x;
"""
@cdecorator.transpiler('var')
def var():
    x : Attribute[float]



VARS = """
attribute float x;
attribute float y;
attribute float intensity;
varying float v_intensity;
"""
@cdecorator.transpiler('vars')
def vars_():
    x : Attribute[float]
    y : Attribute[float]
    intensity : Attribute[float]
    v_intensity : Varying[float]




VERTEX = """
attribute float x;
attribute float y;
attribute float intensity;

varying float v_intensity;
void main (void)
{
    v_intensity = intensity;
    gl_Position = vec4(x, y, 0.0, 1.0);
}
"""
@cdecorator.transpiler('vertex')
def vertex():
    x : Attribute[float]
    y : Attribute[float]
    intensity : Attribute[float]
    v_intensity : Varying[float]

    #def main() -> void:
    #    v_intensity = intensity
    #    gl_Position = vec(x, y, 0.0, 1.0)





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
    #def main() -> void:
        #gl_FragColor = vec4(0, v_intensity, 0, 1)



class CDecoratorDecoratorsTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(act.strip(), exp.strip())

    def test_var(self):
        self.eqcode(VAR, var())

    def test_vars(self):
        self.eqcode(VARS, vars_())

    def test_vertex(self):
        #self.eqcode(VERTEX, _vertex())
        pass



if __name__ == '__main__':
    unittest.main()
