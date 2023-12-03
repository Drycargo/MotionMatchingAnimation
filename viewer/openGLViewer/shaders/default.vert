#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

out vec2 uv_0;
out vec3 normal;
out vec3 fragWorldPos;

uniform mat4 projectionMat;
uniform mat4 viewMat;
uniform mat4 modelMat;

void main() {
    uv_0 = in_texcoord_0;
    normal = mat3(transpose(inverse(modelMat))) * normalize(in_normal);
    fragWorldPos = vec3(modelMat * vec4(in_position, 1.0));
    gl_Position = projectionMat * viewMat * modelMat * vec4(in_position, 1.0);
}