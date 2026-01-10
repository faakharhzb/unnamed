#version 330 core

in vec3 vert;
in vec2 texcoord;

out vec2 uvs;

void main() {
    uvs = vec2(texcoord);
    gl_Position = vec4(vert.x, vert.y, vert.z, 1.0);
}
