import pyxel

class Jeu:
    def __init__(self, w:int, h:int, fps:int):
        
        
        pyxel.init(w, h, "NDC 2026", fps)

        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)


    def update(self): pass

    def draw(self):
        pyxel.cls(0)

if __name__ == "__main__":
    Jeu(128, 128, 60)