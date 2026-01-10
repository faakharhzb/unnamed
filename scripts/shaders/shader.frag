#version 330 core

uniform sampler2D tex;

in vec2 uvs;

out vec4 f_colour;

void main() {
    vec2 sample_pos = vec2(uvs.x, uvs.y);

    f_colour = vec4(texture(tex, sample_pos).rgb, 1.0);
}
