import cdecorator

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

void main (void)
{
    v_color = color;
    v_radius = radius;
    v_eye_position = <transform.trackball_view> *
                     <transform.trackball_model> *
                     vec4(position,1.0);
    v_light_direction = normalize(light_position);
    gl_Position = <transform(position)>;
    // stackoverflow.com/questions/8608844/...
    //  ... resizing-point-sprites-based-on-distance-from-the-camera
    vec4 p = <transform.trackball_projection> *
             vec4(radius, radius, v_eye_position.z, v_eye_position.w);
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



print(cdecorator.transpile(transformers))
