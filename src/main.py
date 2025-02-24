import pygame as pg
import numpy as np
import moderngl as mgl
import sys
from objects import *
from camera import Camera
from scene import Scene
from light import Light
from mesh import Mesh

class GraphicsEngine:
    def __init__(self, window_size=(1600,900)):
        pg.init()
        self.WIN_SIZE=window_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        
        # Create opengl context
        self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ui_surface = pg.Surface(self.WIN_SIZE, pg.SRCALPHA)
        
        # Mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        
        # Spacing 
        self.objects_added = []
        self.spacing = 2

        # Detect and use existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        
        # Light
        self.light = Light()

        # Initializing camera
        self.camera = Camera(self)

        # Mesh
        self.mesh = Mesh(self)

        # Scene - Load object
        self.scene = Scene(self)

    def calculate_next_position(self):
        """Calcula a próxima posição com base nos objetos já adicionados"""
        if len(self.objects_added) == 0:
            return np.array([0.0, 0.0, -5.0])  # Primeira posição, no centro

        # Pega a última posição do último objeto adicionado e soma o espaçamento
        last_position = self.objects_added[-1]
        next_position = last_position + np.array([self.spacing, 0.0, 0.0])  # Espaça no eixo X

        return next_position

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

            # Detecta a tecla pressionada para adicionar objetos
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_0:  
                    position = self.calculate_next_position()
                    self.scene.add_object_from_ui(position, "cube")  # Passa a posição calculada
                    self.objects_added.append(position)  # Armazena a posição do novo objeto
                elif event.key == pg.K_1:  
                    position = self.calculate_next_position()
                    self.scene.add_object_from_ui(position, "sphere")  # Passa a posição calculada
                    self.objects_added.append(position)
                if event.key == pg.K_z: 
                    self.scene.undo()
                if event.key == pg.K_y:  
                    self.scene.redo()

    def render(self):
        self.ctx.clear(color=(0.22, 0.16, 0.18))
        self.scene.render()
        pg.display.flip()
    
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)
    
if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()