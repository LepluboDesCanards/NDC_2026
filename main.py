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
        self.list_ennemis = []
        pyxel.load("theme.pyxres")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if (pyxel.frame_count % 30) == 0:
            self.timer -= 1

        if self.timer == 0:
            self.isVictory = True
        
        #update pos ennemis
        for ennemi in self.list_ennemis:
            if ennemi.y <= -8:
                self.isGameOver = True
            ennemi.update()

        for b in self.buttons:
            b.update()

        #spawn ennemi toutes les 10 sec
        if (pyxel.frame_count % 300) == 0:
            self.list_ennemis.append(Ennemi("Goblin"))

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
            timer_border_x = self.w - 16
            timer_border_y = 1
            pyxel.rect(timer_border_x, timer_border_y, 15, 9, 0)
            pyxel.rectb(timer_border_x, timer_border_y, 15, 9, 7)
            pyxel.text(timer_border_x+2, timer_border_y+2, str(self.timer), 7)

            #dessine les ennemis
            for ennemi in self.list_ennemis:
                ennemi.draw()
        elif self.isVictory:
            pyxel.text(self.w // 2 - 15, self.h // 2, "Victoire !", 3)
        elif self.isGameOver:
            pyxel.text(self.w // 2 - 15, self.h // 2, "Game Over", 8)


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
        self.speed = 1
        self.x, self.y = (self.w-8, self.h - self.h//3 - 16)
        self.vie = {"1": 10}

    def update(self):
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

if __name__ == "__main__":
    Jeu(128, 128, 30)