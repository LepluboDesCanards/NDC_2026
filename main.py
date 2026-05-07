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
            return "Create_Tower"


class Jeu:
    def __init__(self, w:int, h:int, fps:int):
        
        self.w = w
        self.h = h
        self.fps = fps
        
        self.buttons = [Button(83, self.h - self.h // 3 + 2, "Achat:10$")]

        self.towers = []

        pyxel.init(w, h, "NDC 2026", fps)

        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)


    def update(self):

        for b in self.buttons:
            b.update()

    def draw(self):
        for y in range(self.h//2):
            for x in range(self.w//2):
                pyxel.rect(x*2, y*2, 2, 2, 3 if (x + y) % 2 == 0 else 11)

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

if __name__ == "__main__":
    Jeu(128, 128, 30)