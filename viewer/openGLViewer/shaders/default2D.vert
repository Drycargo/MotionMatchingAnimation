#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec2 in_position;

out vec2 uv_0;


void main() {
    uv_0 = in_texcoord_0;
    gl_Position = vec4(in_position, 0.0, 1.0);
}

/*
uniform mat4 projectionMat;
uniform mat4 viewMat;

void main() {
    uv_0 = in_texcoord_0;
    fragWorldPos = vec3(vec4(in_position, 0.0, 1.0));
    gl_Position = projectionMat * viewMat * vec4(in_position, 0.0, 1.0);
}
*/