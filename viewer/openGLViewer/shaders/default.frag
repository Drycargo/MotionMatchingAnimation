#version 330 core

layout (location = 0) out vec4 fragColor;
in vec2 uv_0;
in vec3 normal;
in vec3 fragWorldPos;

uniform sampler2D u_texture_0;

struct Light {
    vec3 position;
    vec3 ambientI;
    vec3 diffuseI;
    vec3 specularI;
};

uniform Light u_light;
uniform vec3 camWorldPos;

vec3 getLighted(vec3 color) {
    vec3 refinedNormal = normalize(normal);

    // Ambient
    vec3 ambient = u_light.ambientI;

    // Diffuse
    vec3 lightInDir = normalize(fragWorldPos - u_light.position);
    vec3 diffuse = max(0.0, dot(-lightInDir, refinedNormal)) * u_light.diffuseI;

    // Specular
    vec3 camOutDir = normalize(camWorldPos - fragWorldPos);
    vec3 lightOutDir = reflect(lightInDir, refinedNormal);
    vec3 specular = pow(max(0.0, dot(camOutDir, lightOutDir)), 32.0) * u_light.specularI;

    return color * (ambient + diffuse + specular);
}

void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;

    // gamma correction
    float gamma = 2.2;
    color = pow(getLighted(pow(color, vec3(gamma))), 1/vec3(gamma));
    fragColor = vec4(color, 1.0);
}