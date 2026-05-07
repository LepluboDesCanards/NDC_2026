import pyxel

class Jeu:
    def __init__(self, w:int, h:int, fps:int):
        self.isGameOver = False
        self.isVictory = False
        self.timer = 180
        self.fps = fps
        self.w = w
        self.h = h
        self.buttons = [Button(83, self.h - self.h // 3 + 2, "Achat:10$")]
        self.towers = []
        self.spawnpoint = (self.w-8, self.h- self.h//3 - 16)
        pyxel.init(self.w, self.h, "NDC 2026")
        self.ennemis = []
        self.distances = []
        self.zones = [[20, 55, False], [56, 55, False], [96, 55, False], [20, 27, False], [56, 27, False], [96, 27, False]]
        pyxel.load("theme.pyxres")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if (pyxel.frame_count % 30) == 0:
            self.timer -= 1

        if self.timer == 0:
            self.isVictory = True
        
        #update pos ennemis
        for ennemi in self.ennemis:
            if ennemi.type == -1:
                self.ennemis.remove(self)

            if ennemi.y <= -8:
                self.isGameOver = True
            ennemi.update()

        #boutons
        for b in self.buttons:
            if b.update() == "Create_Tower" and len([t for t in self.towers if t[0]]) < 18:
                self.create_tower()
        
        #update des tours
        for t in self.towers:
            t[0].update()

        #spawn ennemi toutes les 10 sec
        if (pyxel.frame_count % 300) == 0:
            self.ennemis.append(Ennemi("Goblin"))

    def draw(self):
        pyxel.cls(0)
        if not(self.isGameOver) and not(self.isVictory):
            for y in range(self.h//2):
                for x in range(self.w//2):
                    pyxel.rect(x*2, y*2, 2, 2, 3 if (x + y) % 2 == 0 else 11)

            #chemin
            pyxel.rect(10, 70, 140, 8, 10)
            pyxel.rect(10, 42, 8, 28, 10)
            pyxel.rect(10, 42, 106, 8, 10)
            pyxel.rect(108, 14, 8, 28, 10)
            pyxel.rect(10, 14, 106, 8, 10)
            pyxel.rect(10, 0, 8, 22, 10)

            pyxel.rect(0, self.h - self.h // 3, self.w, self.h // 3, 0)

            # Zone de merge
            pyxel.rect(2, self.h - self.h // 3 + 2, 62, 32, 10)
            pyxel.rectb(2, self.h - self.h // 3 + 2, 62, 32, 9)

            # Poubelle
            pyxel.rect(65, self.h - self.h // 3 + 2, 15, 32, 14)
            pyxel.rectb(65, self.h - self.h // 3 + 2, 15, 32, 8)

            # Boutons
            for b in self.buttons:
                b.draw()

            # Je sais pas quoi faire de cet espace vide...
            pyxel.rect(0, self.h - self.h // 3 + 35, self.w, 7, 7)
            pyxel.text(1, self.h - self.h // 3 + 36, "Fait avec amour et passion ! <3", 0)

            # Zones de tours
            pyxel.rect(20, 55, 10, 10, 10)
            pyxel.rect(56, 55, 10, 10, 10)
            pyxel.rect(96, 55, 10, 10, 10)

            pyxel.rect(20, 27, 10, 10, 10)
            pyxel.rect(56, 27, 10, 10, 10)
            pyxel.rect(96, 27, 10, 10, 10)

            for t in self.towers:
                t[0].draw()      

            timer_border_x = self.w - 16
            timer_border_y = 1
            pyxel.rect(timer_border_x, timer_border_y, 15, 9, 0)
            pyxel.rectb(timer_border_x, timer_border_y, 15, 9, 7)
            pyxel.text(timer_border_x+2, timer_border_y+2, str(self.timer), 7)

            #dessine les ennemis
            for ennemi in self.ennemis:
                ennemi.draw()
        elif self.isVictory:
            pyxel.text(self.w // 2 - 15, self.h // 2, "Victoire !", 3)
        elif self.isGameOver:
            pyxel.text(self.w // 2 - 15, self.h // 2, "Game Over", 8)
    
    def create_tower(self):
        in_ui_towers = len([t for t in self.towers if t[0]])

        if in_ui_towers >= 12:
            y = self.h - self.h // 3 + 23
            in_ui_towers -= 12

        elif in_ui_towers >= 6:
            y = self.h - self.h // 3 + 13
            in_ui_towers -= 6
        else:
            y = y = self.h - self.h // 3 + 3

        x = 4 + (10 * in_ui_towers)
        self.towers.append((Tower(x, y, 1, self), False))

class Button:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self. w = 3 * len(text) + len(text) + 3
        self.h = 9
        self.text = text

    def is_mouse_over(self):
        return (self.x <= pyxel.mouse_x < self.x + self.w) and (self.y <= pyxel.mouse_y < self.y + self.h)

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 5 if not self.is_mouse_over() else 7)
        pyxel.rectb(self.x, self.y, self.w, self.h, 1 if not self.is_mouse_over() else 6)
        pyxel.text(self.x + 2, self.y + 2, self.text, 7 if not self.is_mouse_over() else 0)
    
    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_mouse_over():
            return "Create_Tower"

class Ennemi():
    def __init__(self, type):
        self.w = 128
        self.h = 128
        self.type = type
        self.speed = 0.5
        self.x, self.y = (self.w-8, self.h - self.h//3 - 16)

    def update(self):

        if pyxel.pget(self.x + 4, self.y + 4) == 8:
            self.type = -1

        if self.y == 70:
            self.x -= self.speed
        if 42 < self.y <= 70 and self.x == 10:
            self.y -= self.speed
        if 14 <= self.y <= 42 and self.x < 110:
            self.x += self.speed
        if 14 <= self.y <= 42 and self.x == 110:
            self.y -= self.speed
        if 0 < self.y <= 14 and self.x > 10:
            self.x -= self.speed
        if self.y <= 14 and self.x == 10:
            self.y -= self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0, 0, 1)

class Tower:
    def __init__(self, x, y, lvl, game_state:Jeu, active=False):
        self.x = self.place_x = x
        self.y = self.place_y = y
        self.lvl = lvl
        self.hp = 10 * lvl
        self.dmg = 2 * lvl
        self.active = active
        self.game_state = game_state
        self.tirs_liste = []
    
    def is_mouse_over(self):
        return (self.x <= pyxel.mouse_x < self.x + 8) and (self.y <= pyxel.mouse_y < self.y + 8)
        
    def is_over_zone(self):
        free_zones = [(z[0], z[1]) for z in self.game_state.zones if not z[2]]

        for z in free_zones:
            if (z[0] < pyxel.mouse_x < z[0] + 10) and (z[1] < pyxel.mouse_y < z[1] + 10):
                return z
        return []

    def draw(self): 
        pyxel.blt(self.x, self.y, 0, 16, 8, 8, 8, 0)
        for tir in self.tirs_liste:
            pyxel.rect(tir[0], tir[1], 1, 4, 8)

    def update(self): 
        if self.active:
            if (pyxel.frame_count % 15) == 0:
                self.tirs_liste.append([self.x+4, self.y-4])
                self.tirs_liste = self.tirs_deplacement(self.tirs_liste)
                if len(self.tirs_liste) > 1:
                    self.tirs_liste.pop(-1)
            if (pyxel.frame_count % 150) == 0:
                self.tirs_liste.append([self.x+4, self.y-4])
        else:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                zone = self.is_over_zone()
                if zone != []:
                    self.x = self.place_x = zone[0] + 1
                    self.y = self.place_y = zone[1] + 1

                    self.active = True
                    
            elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if self.is_mouse_over():
                    self.x = pyxel.mouse_x - 4 
                    self.y = pyxel.mouse_y - 4
                else:
                    self.x = self.place_x + 1
                    self.y = self.place_y + 1

    def tirs_deplacement(self, tirs_liste):
        for tir in self.tirs_liste:
            tir[1] -= 2
            if tir[1]<-8:
                self.tirs_liste.remove(tir)
        return self.tirs_liste

if __name__ == "__main__":
    Jeu(128, 128, 30)