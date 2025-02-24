from hotkey_manager import HotkeyManager
from objects import *

# Implementar conceito de lista
class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.undo_stack = []
        self.redo_stack = []
        self.load()

        # Criar e configurar o gerenciador de hotkeys
        self.hotkey_manager = HotkeyManager(self)
        self.hotkey_manager.setup_tree()
    
    def add_object(self, obj):
        self.objects.append(obj)
        self.undo_stack.append(('add', obj))  # Empilha a operação de adição

    def remove_object(self, obj):
        """ Remove objeto da cena e empilha para desfazer """
        if obj in self.objects:
            self.objects.remove(obj)
            self.undo_stack.append(('remove', obj))  # Empilha a operação de remoção

    def add_object_from_ui(self, pos, obj_type="cube"):
        """ Adiciona um objeto à cena baseado no tipo """
        obj_map = {
            "cube": Cube,
            "sphere": Sphere,
        }
        
        if obj_type in obj_map:
            new_obj = obj_map[obj_type](self.app, pos=pos) 
            self.add_object(new_obj)

    def undo(self):
        """ Desfaz a última operação (adicionar ou remover objeto) """
        if self.undo_stack:
            last_action, obj = self.undo_stack.pop()
            if last_action == 'add':
                self.remove_object(obj)  # Se a última ação foi adicionar, remove
                self.redo_stack.append(('add', obj))  # Empilha para refazer
            elif last_action == 'remove':
                self.add_object(obj)  # Se a última ação foi remover, adiciona de volta
                self.redo_stack.append(('remove', obj))  # Empilha para refazer
    
    def redo(self):
        """ Refaz a última operação desfeita """
        if self.redo_stack:
            last_action, obj = self.redo_stack.pop()
            if last_action == 'add':
                self.add_object(obj)  # Se a última ação foi desfazer adição, adiciona de volta
            elif last_action == 'remove':
                self.remove_object(obj)  # Se a última ação foi desfazer remoção, remove novamente

    def load(self):
        """ Carrega objetos pré-existentes """
        app = self.app
        add = self.add_object

        add(Cube(app))
        add(Cube(app, tex_id=0, pos=(-2.5, 0, 0), rot=(45, 0, 0), scale=(1, 1, 1)))
        add(Cube(app, tex_id=1, pos=(2.5, 0, 0), rot=(-45,0,0), scale=(1, 1, 1)))
        add(Cube(app, tex_id=2, pos=(-5, 0, 0), rot=(-45,0,0), scale=(1, 1, 1)))
        add(Cube(app, tex_id=2, pos=(5, 0, 0), rot=(-45,0,0), scale=(1, 1, 1)))
        add(Sphere(app, tex_id=3, pos=(7.5, 0, 0)))
    
    def render(self):
        for obj in self.objects:
            obj.render()
    
    def handle_input(self, key):
        """ Chama o gerenciador de hotkeys para lidar com a entrada """
        self.hotkey_manager.handle_key(key)