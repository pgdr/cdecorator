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





INCLUDE = """
#include "antialias/outline.glsl"
varying float v_size;
varying vec3 v_color;
varying float v_radius;
varying vec4 v_eye_position;
varying vec3 v_light_direction;
void main() {
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float point_size = v_size  + 5.0;
    float distance = length(P*point_size) - v_size/2;
    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0) {
        discard;
    }
    float z = sqrt(d);
    vec4 pos = v_eye_position;
    pos.z += v_radius*z;
    vec3 pos2 = pos.xyz;
    pos = <transform.trackball_projection> * pos;
    gl_FragDepth = 0.5*pos.z/pos.w + 0.5;
    vec3 normal = vec3(x,y,z);
    float diffuse = clamp(dot(normal, v_light_direction), 0.0, 1.0);
    vec4 color = vec4(0.5 + 0.5*diffuse*v_color, 1.0);
    gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
}
"""
def include():
    __include__("antialias/outline.glsl")
    v_size : varying[float]
    v_color : varying[vec3]
    v_radius : varying[float]
    v_eye_position : varying[vec4]
    v_light_direction : varying[vec3]
    def main() -> void :
        P : vec2 = gl_PointCoord.xy - vec2(0.5,0.5)
        point_size : float = v_size  + 5.0
        distance : float = length(P*point_size) - v_size/2
        texcoord : vec2 = gl_PointCoord* 2.0 - vec2(1.0)
        x : float = texcoord.x
        y : float = texcoord.y
        d : float = 1.0 - x*x - y*y
        if (d <= 0.0):
            discard
        z : float = sqrt(d)
        pos : vec4 = v_eye_position;
        pos.z += v_radius*z
        pos2 : vec3 = pos.xyz
        pos = _(transform.trackball_projection) * pos
        gl_FragDepth = 0.5*(pos.z / pos.w)+0.5
        normal : vec3 = vec3(x,y,z)
        diffuse: float = clamp(dot(normal, v_light_direction), 0.0, 1.0)
        color : vec4 = vec4((0.5 + 0.5*diffuse)*v_color, 1.0)
        gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color)



class MathTest(unittest.TestCase):

    def eqcode(self, act, exp):
        return self.assertEqual(strip(act.strip()), strip(exp.strip()))

    def test_math(self):
        self.eqcode(MATH, cdecorator.transpile(math))

    def test_fragment(self):
        self.eqcode(FRAGMENT, cdecorator.transpile(fragment))

    def test_transformers(self):
        self.eqcode(TRANSFORMERS, cdecorator.transpile(transformers))

    def test_include(self):
        self.eqcode(INCLUDE, cdecorator.transpile(include))


if __name__ == '__main__':
    unittest.main()
