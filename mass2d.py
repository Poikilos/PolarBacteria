class Mass2D(Widget):
    pos = None
    directionRadians = None
    speedReductionPPF = None
    speedPPF = None
    _rectangle_instruction = None
    _rotate_instruction = None
    
    def __init__(self, **kwargs):
        super(Projectile, self).__init__(**kwargs) 
        
        self._rectangle_instruction = Rectangle(pos=(0,0), size=(20,20))
        self._rotate_instruction = Rotate(origin=self.getCenterPoint(), angle=0)
        
        self.canvas.add(PushMatrix())
        self.canvas.add(self._rotate_instruction)
        self._color_instruction = Color(1,1,1,1)
        self.canvas.add(self._color_instruction)
        self.canvas.add(self._rectangle_instruction)
        self.canvas.add(PopMatrix())
    
    def start(self, position, speedPPF, speedDecreasePPF, directionRadians, id):
        self.id = id
        self.speedPPF = speedPPF
        self.speedReductionPPF = speedDecreasePPF
        self.pos = float(position[0]), float(position[1]) #copy the coordinates to a new point
        self.directionRadians = directionRadians
        
    def refresh(self):
        if (self.speedReductionPPF is not None):
            self.speedPPF -= self.speedReductionPPF
    
    def setCenterPointCoordinates(self, x, y):
        self.freePos = float(x), self.freePos[1]
        self.freePos = self.freePos[0], float(y)
        self._change_instructions()

    def setCenterPoint(self, pos):
        self.freePos = float(pos[0]), self.freePos[1]
        self.freePos = self.freePos[0], float(pos[1])
        self._change_instructions()
        
    def getCenterPoint(self):
        return self.freePos[0], self.freePos[1]