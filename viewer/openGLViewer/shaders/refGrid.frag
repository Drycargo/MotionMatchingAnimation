#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 fragWorldPos;

uniform float gridWidth;
uniform float lineWidth;
uniform float axisAmp;

void main() {
    float alpha = 0.0;

    vec2 distsFromGrid = min(mod(fragWorldPos.xz, gridWidth), vec2(gridWidth) - mod(fragWorldPos.xz, gridWidth));
    if (distsFromGrid[0] <= lineWidth || distsFromGrid[1] <= lineWidth
        || abs(fragWorldPos.x) <= lineWidth * axisAmp
        || abs(fragWorldPos.z) <= lineWidth * axisAmp) {
        alpha = 1.0;
    } else {
        alpha = 0.0;
    }

    fragColor = vec4(vec3(1.0), alpha);
}