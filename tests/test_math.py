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
        gl_Position = _(transform)  # ugly, thanks, I know
        P : vec4 = m_view * m_model * vec4(position, 1.0)
        v_position = P.xyz / P.w
        v_normal = vec3(m_normal * vec4(normal,0.0))







FRAGMENT = """
varying vec3 v_normal;
varying vec3 v_position;
const vec3 light_position = vec3(1.0, 1.0, 1.0);
const vec3 ambient_color = vec3(0.1, 0.0, 0.0);
const vec3 diffuse_color = vec3(0.75, 0.125, 0.125);
const vec3 specular_color = vec3(1.0, 1.0, 1.0);
const float shininess = 128.0;
const float gamma = 2.2;
void main() {
    vec3 normal = normalize(v_normal);
    vec3 light_direction = normalize(light_position - v_position);
    float lambertian = max(dot(light_direction, normal), 0.0);
    float specular = 0.0;
    if (lambertian > 0.0) {
        vec3 view_direction = normalize(- v_position);
        vec3 half_direction = normalize(light_direction + view_direction);
        float specular_angle = max(dot(half_direction, normal), 0.0);
        specular = pow(specular_angle, shininess);
    }
    vec3 color_linear = ambient_color + lambertian * diffuse_color + specular * specular_color;
    vec3 color_gamma = pow(color_linear, vec3(1.0 / gamma));
    gl_FragColor = vec4(color_gamma, 1.0);
}
"""
def fragment():
    v_normal : varying[vec3]
    v_position : varying[vec3]
    light_position : const[vec3]  = vec3(1.0,1.0,1.0)
    ambient_color  : const[vec3]  = vec3(0.1, 0.0, 0.0)
    diffuse_color  : const[vec3]  = vec3(0.75, 0.125, 0.125)
    specular_color : const[vec3]  = vec3(1.0, 1.0, 1.0)
    shininess      : const[float] = 128.0
    gamma          : const[float] = 2.2

    def main() -> void:
        normal : vec3 = normalize(v_normal)
        light_direction : vec3 = normalize(light_position - v_position)
        lambertian : float = max(dot(light_direction,normal), 0.0)
        specular : float= 0.0
        if lambertian > 0.0:
            view_direction : vec3 = normalize(-v_position)
            half_direction : vec3 = normalize(light_direction + view_direction)
            specular_angle : float = max(dot(half_direction, normal), 0.0)
            specular = pow(specular_angle, shininess);
        color_linear : vec3 = ambient_color + \
                            lambertian * diffuse_color + \
                            specular * specular_color
        color_gamma : vec3  = pow(color_linear, vec3(1.0/gamma))
        gl_FragColor = vec4(color_gamma, 1.0)





TRANSFORMERS = """
uniform vec3 light_position;
attribute vec3 position;
attribute vec3 color;
attribute float radius;
varying float v_size;
varying vec3 v_color;
varying float v_radius;
varying vec4 v_eye_position;
varying vec3 v_light_direction;
void main(void) {
    v_color = color;
    v_radius = radius;
    v_eye_position = <transform.trackball_view> * <transform.trackball_model> * vec4(position,1.0);
    v_light_direction = normalize(light_position);
    gl_Position = <transform(position)>;
    vec4 p = <transform.trackball_projection> * vec4(radius, radius, v_eye_position.z, v_eye_position.w);
    v_size = 512.0 * p.x / p.w;
    gl_PointSize = v_size + 5.0;
}
"""
def transformers():
    light_position : uniform[vec3]
    position : attribute[vec3]
    color : attribute[vec3]
    radius : attribute[float]

    v_size : varying[float]
    v_color : varying[vec3]
    v_radius : varying[float]
    v_eye_position : varying[vec4]
    v_light_direction : varying[vec3]

    def main(void) -> void:
        v_color = color
        v_radius = radius
        v_eye_position = _(transform.trackball_view)  * _(transform.trackball_model) * vec4(position, 1.0)
        v_light_direction = normalize(light_position)
        gl_Position = _(transform(position))

        p : vec4 = _(transform.trackball_projection) * vec4(radius, radius, v_eye_position.z, v_eye_position.w)
        v_size = 512.0 * p.x / p.w
        gl_PointSize = v_size + 5.0








class MathTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(strip(act.strip()), strip(exp.strip()))

    def test_math(self):
        self.eqcode(MATH, cdecorator.transpile(math))

    def test_fragment(self):
        self.eqcode(FRAGMENT, cdecorator.transpile(fragment))

    def test_transformers(self):
        self.eqcode(TRANSFORMERS, cdecorator.transpile(transformers))


if __name__ == '__main__':
    unittest.main()
