#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
uniform float progress;
uniform bool inGeneration;

void main() {
    vec3 color = inGeneration ?
        vec3(0.6, 1.0, 0.6) :
        (uv_0.x < progress ? vec3(0.6, 0.8, 1.0) : vec3(0.5, 0.5, 0.5));
    fragColor = vec4(color, 1.0);
}