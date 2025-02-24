class DecisionTreeNode:
    def __init__(self, action=None):
        self.action = action  # Ação a ser tomada nesse nó (caso seja uma folha)
        self.children = []    # Filhos (nós subsequentes)

    def add_child(self, child):
        """ Adiciona um filho a esse nó """
        self.children.append(child)

class HotkeyManager:
    def __init__(self, scene):
        self.scene = scene
        self.root = DecisionTreeNode()

    def setup_tree(self):
        """ Configura a árvore de decisão para as hotkeys """
        root = self.root

        # Filhos da raiz - as ações podem ser: Adicionar, Transladar, Rotacionar.
        add_actions = [DecisionTreeNode("Add Cube"),
                       DecisionTreeNode("Add Sphere")]
        
        move_actions = [DecisionTreeNode("Move Left"),
                        DecisionTreeNode("Move Right"),
                        DecisionTreeNode("Move Up"),
                        DecisionTreeNode("Move Down")]
        
        rotate_actions = [DecisionTreeNode("Rotate Clockwise"),
                          DecisionTreeNode("Rotate Counterclockwise")]
        
        # Adicionando ações de adicionar, mover e rotacionar
        root.add_child(add_actions[0])  # Add Cubo
        root.add_child(add_actions[1])  # Add Esfera
        
        root.add_child(move_actions[0])  # Esquerda
        root.add_child(move_actions[1])  # Direita
        root.add_child(move_actions[2])  # Cima
        root.add_child(move_actions[3])  # Baixo
        
        root.add_child(rotate_actions[0])  # Rotacionar no sentido horário
        root.add_child(rotate_actions[1])  # Rotacionar no sentido anti-horário

    def handle_key(self, key):
        """ Interpreta a tecla pressionada e executa a ação associada """
        if 0 <= key < len(self.root.children):
            action = self.root.children[key].action
            self.execute_action(action)
        else:
            print("Tecla não mapeada!")

    def execute_action(self, action):
        """ Executa a ação associada à hotkey """
        if action:
            print(f"Ação Executada: {action}")
            # Dependendo da ação, invocar métodos na classe `Scene`
            if action == "Add Cube":
                self.scene.add_object_from_ui(self.scene.objects[-1].pos, obj_type="cube")
            elif action == "Add Sphere":
                self.scene.add_object_from_ui(self.scene.objects[-1].pos, obj_type="sphere")
            elif action == "Move Left":
                self.move_object("left")
            elif action == "Move Right":
                self.move_object("right")
            elif action == "Move Up":
                self.move_object("up")
            elif action == "Move Down":
                self.move_object("down")
            elif action == "Rotate Clockwise":
                self.rotate_object("clockwise")
            elif action == "Rotate Counterclockwise":
                self.rotate_object("counterclockwise")
        
    def move_object(self, direction):
        """ Mover o último objeto da cena para a direção especificada """
        obj = self.scene.objects[-1]
        step = 0.5  # Tamanho do passo para movimento
        if direction == "left":
            obj.pos = (obj.pos[0] - step, obj.pos[1], obj.pos[2])
        elif direction == "right":
            obj.pos = (obj.pos[0] + step, obj.pos[1], obj.pos[2])
        elif direction == "up":
            obj.pos = (obj.pos[0], obj.pos[1] + step, obj.pos[2])
        elif direction == "down":
            obj.pos = (obj.pos[0], obj.pos[1] - step, obj.pos[2])
        obj.m_model = obj.get_model_matrix()  # Atualiza o modelo

    def rotate_object(self, direction):
        """ Rotaciona o último objeto da cena """
        obj = self.scene.objects[-1]
        step = 5  # Ângulo de rotação
        if direction == "clockwise":
            obj.rot = (obj.rot[0], obj.rot[1] + step, obj.rot[2])
        elif direction == "counterclockwise":
            obj.rot = (obj.rot[0], obj.rot[1] - step, obj.rot[2])
        obj.m_model = obj.get_model_matrix()  # Atualiza o modelo
