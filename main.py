import pyxel

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
            print("'Create_Tower' Triggered")
            return "Create_Tower"


class Jeu:
    def __init__(self, w:int, h:int, fps:int):
        
        self.w = w
        self.h = h
        self.fps = fps
        
        self.buttons = [Button(83, self.h - self.h // 3 + 2, "Achat:10$")]

        self.towers = []

        pyxel.init(w, h, "NDC 2026", fps)

        pyxel.load("./theme.pyxres")
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)


    def update(self):

        for b in self.buttons:
            if b.update() == "Create_Tower" and len([t for t in self.towers if t[0]]) < 18:
                self.create_tower()
        
        for t in self.towers:
            t[0].update()

    def draw(self):
        for y in range(self.h//2):
            for x in range(self.w//2):
                pyxel.rect(x*2, y*2, 2, 2, 14 if (x + y) % 2 == 0 else 15)

        pyxel.rect(0, self.h - self.h // 3, self.w, self.h // 3, 0)

        pyxel.rect(10, 70, 140, 8, 10)
        pyxel.rect(10, 42, 8, 28, 10)
        pyxel.rect(10, 42, 106, 8, 10)
        pyxel.rect(108, 14, 8, 28, 10)
        pyxel.rect(10, 14, 106, 8, 10)
        pyxel.rect(10, 0, 8, 22, 10)

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
        pyxel.text(1, self.h - self.h // 3 + 36, "Fait avec amour et passion ! <3" if len(self.towers) == 0 else "Pas trop vite avec les tours !", 0)
        

        for t in self.towers:
            t[0].draw()            

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
        self.towers.append((Tower(x, y, 1), False))

class Tower:

    def __init__(self, x, y, lvl, active=False):
        self.x = x
        self.y = y
        self.lvl = lvl

        self.hp = 10 * lvl
        self.dmg = 2 * lvl

        self.active = active
    
    def is_mouse_over(self):
        return (self.x <= pyxel.mouse_x < self.x + 8) and (self.y <= pyxel.mouse_y < self.y + 8)

    def draw(self): 
        pyxel.blt(self.x, self.y, 0, 16, 8, 8, 8, 0)


    def update(self):
        
        if self.active:
            pass
        else:
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.is_mouse_over():
                self.x = pyxel.mouse_x - 4 
                self.y = pyxel.mouse_y - 4


if __name__ == "__main__":
    Jeu(128, 128, 30)