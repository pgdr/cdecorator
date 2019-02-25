import unittest
import cdecorator

from . import strip


MATH = """
uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_normal;
attribute vec3 position;
attribute vec3 normal;
varying vec3 v_normal;
varying vec3 v_position;
void main() {
    gl_Position = <transform>;
    vec4 P = m_view * m_model * vec4(position, 1.0);
    v_position = P.xyz / P.w;
    v_normal = vec3(m_normal * vec4(normal, 0.0));
}
"""
def math():
    m_model : uniform[mat4]
    m_view : uniform[mat4]
    m_normal : uniform[mat4]
    position : attribute[vec3]
    normal : attribute[vec3]
    v_normal : varying[vec3]
    v_position : varying[vec3]
    def main():
        gl_Position = ...@transform  # ugly, thanks, I know
        P : vec4 = m_view * m_model * vec4(position, 1.0)
        v_position = P.xyz / P.w
        v_normal = vec3(m_normal * vec4(normal,0.0))


class MathTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(strip(act.strip()), strip(exp.strip()))

    def test_math(self):
        self.eqcode(MATH, cdecorator.transpile(math))


if __name__ == '__main__':
    unittest.main()
