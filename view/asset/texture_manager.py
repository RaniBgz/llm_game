from view.asset.pygame_texture import PygameTexture

class TextureManager:
    def __init__(self):
        self.textures = {}

    def get_texture(self, texture_path):
        if texture_path not in self.textures:
            self.textures[texture_path] = PygameTexture(texture_path)
        return self.textures[texture_path]