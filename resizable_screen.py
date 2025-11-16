import pygame
import moderngl
from array import array
from pyautogui import size as screen_size



import pygame
import moderngl
from array import array
from pyautogui import size as screen_size


class Mouse:
    def __init__(self, mouse_dict=None):
        if mouse_dict is None:
            mouse_dict = {
                "position_xy": (-1, -1),
                "state": {"left": False, "middle": False, "right": False},
                "clicked": {
                    "up": {"left": False, "middle": False, "right": False},
                    "down": {"left": False, "middle": False, "right": False}
                }
            }
        
        self.data = mouse_dict
        
    @property
    def pos(self):
        return self.data["position_xy"]
    
    @property
    def x(self):
        return self.data["position_xy"][0]
    
    @property
    def y(self):
        return self.data["position_xy"][1]
    
    @property
    def state(self):
        return type('MouseState', (), {
            'left': self.data["state"]["left"],
            'middle': self.data["state"]["middle"], 
            'right': self.data["state"]["right"]
        })()
    
    @property
    def clicked(self):
        up_state = type('ClickState', (), {
            'left': self.data["clicked"]["up"]["left"],
            'middle': self.data["clicked"]["up"]["middle"],
            'right': self.data["clicked"]["up"]["right"]
        })()
        
        down_state = type('ClickState', (), {
            'left': self.data["clicked"]["down"]["left"],
            'middle': self.data["clicked"]["down"]["middle"],
            'right': self.data["clicked"]["down"]["right"]
        })()
        
        return type('MouseClicks', (), {
            'up': up_state,
            'down': down_state
        })()

class DedicatedMouseGuiEventHandler:
    def __init__(self, default_screen_size):
        self.ORIGINAL_SCREEN_SIZE = default_screen_size
        self.current_screen_size = self.ORIGINAL_SCREEN_SIZE
        
        self.mouse = Mouse()


    def change_stored_current_screen_size(self, current_screen_size):
        self.current_screen_size = current_screen_size
    
    def tick(self, mouse_pos, mouse_pressed):
        mouse_pos = (int(mouse_pos[0] * self.ORIGINAL_SCREEN_SIZE[0] / self.current_screen_size[0]),
                     int(mouse_pos[1] * self.ORIGINAL_SCREEN_SIZE[1] / self.current_screen_size[1]))
        
        
        old_mouse_state = self.mouse.data["state"].copy()
        
        self.mouse = Mouse( {
            "position_xy": (mouse_pos),
            "state": {
                "left": mouse_pressed[0],
                "middle": mouse_pressed[1],
                "right": mouse_pressed[2]
            },
            "clicked": {
                "up": {
                    "left": old_mouse_state["left"] and not mouse_pressed[0],
                    "middle": old_mouse_state["middle"] and not mouse_pressed[1],
                    "right": old_mouse_state["right"] and not mouse_pressed[2]
                },
                "down": {
                    "left": not old_mouse_state["left"] and mouse_pressed[0],
                    "middle": not old_mouse_state["middle"] and mouse_pressed[1],
                    "right": not old_mouse_state["right"] and mouse_pressed[2]
                }
            }
        })

class PygameLikeGlslScreen:
    DEFAULT_VERT_SHADER_PATH = None
    DEFAULT_FRAG_SHADER_PATH = None
    
    full_screen = pygame.K_f
    DEBUG_MODE = True
    MONITOR_SIZE = screen_size()
    MONITOR_PROPORTIONS = [MONITOR_SIZE[0]/640, MONITOR_SIZE[1]/360]
    
    def __init__(self, pygame_screen_surface: tuple, game_title="", vert_shader=None, frag_shader=None):
        pygame.init()

        self.gl_screen = pygame.display.set_mode(
            pygame_screen_surface,
            pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
        )
        pygame.display.set_caption(game_title)

        self.screen = pygame.Surface(pygame_screen_surface)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)

        self.full_screen = False

        self.vert_shader = self.load_shader(PygameLikeGlslScreen.DEFAULT_VERT_SHADER_PATH, rise_error=False)
        self.frag_shader = self.load_shader(PygameLikeGlslScreen.DEFAULT_FRAG_SHADER_PATH, rise_error=False)

        if vert_shader:
            self.vert_shader = self.load_shader(vert_shader)

        if frag_shader:
            self.frag_shader = self.load_shader(frag_shader)

        if not self.vert_shader:
            self.vert_shader = self.__load_basic_vertex_shaders()

        if not self.frag_shader:
            self.frag_shader = self.__load_basic_fragment_shaders()


        self.name_vert_shader = vert_shader or PygameLikeGlslScreen.DEFAULT_VERT_SHADER_PATH
        self.name_frag_shader = frag_shader or PygameLikeGlslScreen.DEFAULT_FRAG_SHADER_PATH

        #Build GLSL program
        self.program = self.ctx.program(
            vertex_shader=self.vert_shader,
            fragment_shader=self.frag_shader
        )
        self.program["tex"] = 0

        quad_data = array('f', [
            # x     y           u     v
            -1.0,  1.0,         0.0, 1.0,  # top-left
             1.0,  1.0,         1.0, 1.0,  # top-right  
            -1.0, -1.0,         0.0, 0.0,  # bottom-left
             1.0, -1.0,         1.0, 0.0,  # bottom-right
        ])
        self.quad_buffer = self.ctx.buffer(quad_data)

        self.render_object = self.ctx.vertex_array(
            self.program,
            [(self.quad_buffer, "2f 2f", "vert", "texcoord")]
        )

        width, height = self.screen.get_size()
        self.frame_tex = self.ctx.texture((width, height), 4)
        self.frame_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.frame_tex.swizzle = "RGBA" 

        self.mouse_handler = DedicatedMouseGuiEventHandler(pygame_screen_surface)

    def get_screen_size_pygame(self):
        return self.screen.size

    def surf_to_texture(self, surf):
        data = pygame.image.tostring(surf, "RGBA", True)

        texture = self.ctx.texture(surf.get_size(), 4, data)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'RGBA'
        return texture

    def get_frag_loade_shaders(self):
        return self.name_frag_shader
    
    def get_vert_loaded_shaders(self):
        return self.name_vert_shader

    def load_shader(self, file_path: str, rise_error=False):
        """
        this function loads shader
        USE: `frag_shader = LoadShader("shaders/frag_shader.glsl")`
        DATAOUTPUT: string(from file(file.read()))
        """
        if rise_error:
            with open(file_path, 'r') as file:
                return file.read()
        else:
            try:
                with open(file_path, 'r') as file:
                    return file.read()
            except:
                return None

    def fill(self, color):
        """Fills the Pygame surface with the specified color."""
        self.screen.fill(color)

    def blit(self, image: pygame.Surface, cords: list[int]):
        """Blits an image onto the Pygame surface."""
        self.screen.blit(image, cords)

    def display_flip(self, arg=None):
        """Renders the Pygame surface onto the OpenGL screen using shaders."""
        if arg is None:
            arg = {}

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        self.mouse_handler.tick(mouse_pos, mouse_pressed)

        pixel_data = pygame.image.tostring(self.screen, "RGBA", True)
        self.frame_tex.write(pixel_data)

        self.frame_tex.use(0)

        for name, value in arg.items():
            self.program[name] = value

        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        pygame.display.flip()
    
    def change_fullscreen_state(self):
        self.full_screen = not self.full_screen
        if self.full_screen:
            self.gl_screen = pygame.display.set_mode(
                PygameLikeGlslScreen.MONITOR_SIZE, 
                pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF
            )
            self.ctx.viewport = (0, 0, PygameLikeGlslScreen.MONITOR_SIZE[0], PygameLikeGlslScreen.MONITOR_SIZE[1])
            self.mouse_handler.change_stored_current_screen_size(PygameLikeGlslScreen.MONITOR_SIZE)
        else:
            screen_size = self.get_screen_size_pygame()
            self.gl_screen = pygame.display.set_mode(
                screen_size, 
                pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
            )
            self.ctx.viewport = (0, 0, screen_size[0], screen_size[1])
            self.mouse_handler.change_stored_current_screen_size(screen_size)
    
    def change_frag_shader(self, path):
        self.frag_shader = self.load_shader(path)
        self.name_frag_shader = path

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        
    def change_vert_shader(self, path):
        self.vert_shader = self.load_shader(path)
        self.name_vert_shader = path

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
    
    def get_shaders_paths(self) -> tuple:
        """
            returns two paths (vert_shader, frag_shader)
        """
        return (self.name_vert_shader, self.name_frag_shader)
    
    def __load_basic_fragment_shaders(self):
        return """
            #version 330 core

            uniform sampler2D tex;
            in vec2 uvs;
            out vec4 f_color;
            
            void main(){
                f_color = vec4(texture(tex, uvs).rgb, 1.0);
            }
        """
    
    def __load_basic_vertex_shaders(self):
        return """
            #version 330 core

            in vec2 vert;
            in vec2 texcoord;
            out vec2 uvs;

            void main() {
                uvs = texcoord;
                gl_Position = vec4(vert, 0.0, 1.0);
            }
        """
    