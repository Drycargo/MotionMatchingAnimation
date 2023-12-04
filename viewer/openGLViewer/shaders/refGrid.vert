#version 330 core

layout (location = 0) in vec3 in_position;

out vec3 fragWorldPos;

uniform mat4 projectionMat;
uniform mat4 viewMat;
uniform mat4 modelMat;

void main() {
    fragWorldPos = vec3(modelMat * vec4(in_position, 1.0));
    gl_Position = projectionMat * viewMat * modelMat * vec4(in_position, 1.0);
}