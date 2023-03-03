key_switch_camera = 'c'
key_switch_mode = 'z'

key_forward = 'w'
key_back = 's'
key_left = 'a'
key_right = 'd'
key_up = 'e'
key_down = 'q'
key_turn_left = 'n'
key_turn_right = 'm'

key_build = 'v'
key_destroy  = 'c'

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparenTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def key_turn_left(self):
        self.hero.setH((self.hero.getH() +5) % 360)

    def key_turn_right(self):
        self.hero.setH((self.hero.getH() -5) % 360)    

    def Look_at(self, angle):
        x_form = round(self.hero.getx())   
        y_form = round(self.hero.gety())
        z_form = round(self.hero.getz())     

        dx, gy = self.check_dir(angle)
        x_to = x_form + dx
        y_to = y_form + dy
        return x_to, y_to, z_form

    def just_move(self, engle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)    

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65 :
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1) 
        elif angle <= 245:
            return (-1, 1) 
        elif angle <= 290:
            return (-1, 0)          
        elif angle <= 335:
            return (-1, -1)
        else:
            return(0, -1)    
                        
    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
 
    def Left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)  

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] +1 
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlocks(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlocks(pos)
        else:
            self.land.delBlockForm(pos)    

    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward,self.forward)
        base.accept(key_forward + '-repeat', self.turn_left)
        base.accept(key_back,self.back )
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left )
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right,self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)
