#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
uniform sampler2D u_texture_0;
uniform sampler2D u_texture_1;
uniform bool hover;
uniform bool clicked;
uniform bool paused;

void main() {
    float alpha = 1.0;
    vec3 color = paused? texture(u_texture_0, uv_0).rgb : texture(u_texture_1, uv_0).rgb;

    if (hover) {
        color *= 1.1;
    } else if (clicked) {
        color *= 0.9;
    } else {
        alpha = 0.8;
    }

    fragColor = vec4(color, alpha);
}