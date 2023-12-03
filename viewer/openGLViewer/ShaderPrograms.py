import re

class ShaderPrograms:
    def __init__(self, context):
        self.context = context
        self.shaderPrograms = {}
        self.shaderPrograms['default'] = self.getShaderProgram('default')

    def addShaderProgram(self, fragShaderName, vertexShaderName = None):
        parentDir = '\\'.join(re.split('\\\\|/', __file__)[:-1])

        if not vertexShaderName:
            vertexShaderName = fragShaderName

        with open('{}\\shaders\\{}.vert'.format(parentDir, vertexShaderName)) as vertS:
            vertexShader = vertS.read()

        with open('{}\\shaders\\{}.frag'.format(parentDir, fragShaderName)) as fragS:
            fragmentShader = fragS.read()

        newShaderProgram = self.context.program(vertex_shader=vertexShader, fragment_shader=fragmentShader)
        self.shaderPrograms[fragShaderName] = newShaderProgram
        return newShaderProgram

    def getShaderProgram(self, fragShaderName, vertexShaderName = None):
        if fragShaderName in self.shaderPrograms:
            return self.shaderPrograms[fragShaderName]

        return self.addShaderProgram(fragShaderName, vertexShaderName = vertexShaderName)

    def destroy(self):
        for program in self.shaderPrograms.values():
            program.release()