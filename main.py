import pyxel

class Jeu:
    def __init__(self):
        self.isGameOver = False
        self.timer = 180
        self.w = 128
        self.h = 128
        pyxel.init(self.w, self.h, "NDC 2026")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if (pyxel.frame_count % 30) == 0:
            self.timer -= 1

        if self.timer == 0:
            self.isGameOver = True

        if self.isGameOver:
            pyxel.cls(0)

    def draw(self):
        pyxel.cls(0)
        if not(self.isGameOver):
            timer_border_x = self.w - 16
            timer_border_y = 1
            pyxel.rectb(timer_border_x, timer_border_y, 15, 9, 7)
            pyxel.text(timer_border_x+2, timer_border_y+2, str(self.timer), 7)
        else:
            pyxel.text(self.w // 2 - 15, self.h // 2, "Game Over", 7)

Jeu()