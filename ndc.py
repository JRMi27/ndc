#Bonjour et bienvenue dans l'univers de Freeze Cramptélone,
#Vous allez incarner le personnage de Freeze Corleone qui a dérobé les cramptés à la banque d'Apagnan city.
#Mais attention, la police vous recherche et vous devrez vous défendre contre les forces nationales à votre poursuite.
#Pour lui échapper, vous devez utiliser votre revolver pour tirer et éliminer les ennemis, utilisez les touches zqsd pour déplacer votre personnage ainsi que les flèches directionnelles pour choisir la direction de tir
#Attention, plus vous avancez dans les vagues, plus les ennemis sont dangereux.
#Ennemis: Basique (10pts), Rapide - point jaune (25pts), Tank - barre de vie (75pts)
#Quand les ennemis vous touchent, vous perdez une vie, vous en possédez 3. Au bout de ces trois vies votre personnage meurt.
#Appuyez sur G pour recommencer, F pour quitter.

import pyxel
import random

WAVE_CONFIGS = [
    [("basic", 4)],
    [("basic", 4), ("fast", 2)],
    [("basic", 4), ("fast", 3), ("tank", 1)],
    [("basic", 5), ("fast", 4), ("tank", 2)],
    [("basic", 6), ("fast", 5), ("tank", 3)],
]


class Jeu:

    def __init__(self):
        pyxel.init(128, 128, title="Nuit du code", fps=60)
        pyxel.load('theme.pyxres')
        pyxel.playm(0)
        self.score = 0
        self.wave = 1
        self.wave_timer = 0
        self.ennemies = []
        self.potions = [Potion() for _ in range(3)]
        self.character = Character()
        self.game_over = False
        self.spawn_wave(self.wave)
        pyxel.run(self.update, self.draw)

    def get_wave_config(self, wave_num):
        if wave_num <= len(WAVE_CONFIGS):
            return WAVE_CONFIGS[wave_num - 1]
        extra = wave_num - len(WAVE_CONFIGS)
        return [
            ("basic", 6 + extra),
            ("fast", 5 + extra),
            ("tank", 3 + (extra // 2))
        ]

    def spawn_wave(self, wave_num):
        self.ennemies = []
        for enemy_type, count in self.get_wave_config(wave_num):
            for _ in range(count):
                self.ennemies.append(Enemy(enemy_type))
        self.wave_timer = 120

    def update_potions(self):
        for potion in self.potions[:]:
            if self.character.collision(potion):
                if potion.type == "speed":
                    self.character.speed = min(self.character.base_speed + 1.0, 3.0)
                    self.character.speed_timer = 480
                elif potion.type == "heal":
                    self.character.life = min(self.character.life + 1, 3)
                elif potion.type == "shield":
                    self.character.shield_timer = max(self.character.shield_timer, 240)
                self.potions.remove(potion)
        if not self.potions:
            self.spawn_potions()

    def spawn_potions(self):
        potions = []
        count = random.randint(2, 3)
        if self.character.life < 3 and random.random() < 0.4:
            potions.append(Potion("heal"))
            count -= 1
        for _ in range(count):
            potions.append(Potion())
        self.potions = potions

    def update(self):
        if self.game_over:
            if pyxel.btn(pyxel.KEY_G):
                self.reset_game()
            if pyxel.btn(pyxel.KEY_F):
                pyxel.quit()
            return

        self.character.update(self.ennemies)
        self.update_potions()
        for enemy in self.ennemies:
            enemy.update(self.character)

        for enemy in self.character.collisiontirs(self.ennemies):
            self.score += enemy.points

        if not self.ennemies:
            self.wave += 1
            self.spawn_wave(self.wave)

        if self.wave_timer > 0:
            self.wave_timer -= 1

        if self.character.life == 0:
            self.game_over = True

    def draw(self):
        pyxel.cls(0)
        if not self.game_over:
            self.character.draw()
            for potion in self.potions:
                potion.draw()
            for enemy in self.ennemies:
                enemy.draw()
            pyxel.text(2, 2, "Vies:" + str(self.character.life), 7)
            pyxel.text(2, 10, "Score:" + str(self.score), 10)
            pyxel.text(2, 18, "Vague:" + str(self.wave), 7)
            if self.character.speed_timer > 0:
                pyxel.text(72, 2, "SPD " + str(self.character.speed_timer // 60 + 1) + "s", 10)
            if self.character.shield_timer > 0:
                pyxel.text(72, 10, "SCU " + str(self.character.shield_timer // 60 + 1) + "s", 12)
            if self.wave_timer > 60:
                msg = "VAGUE " + str(self.wave) + " !"
                pyxel.text(64 - len(msg) * 2, 55, msg, 10)
        else:
            self.draw_game_over()

    def draw_game_over(self):
        pyxel.cls(7)
        pyxel.text(15, 44, "On ta vole tes cramptes", 0)
        pyxel.text(25, 54, "Score: " + str(self.score), 8)
        pyxel.text(25, 64, "Vague: " + str(self.wave), 8)
        pyxel.text(15, 84, "Appuie sur F pour quitter", 0)
        pyxel.text(10, 94, "Appuie sur G pour recommencer", 0)

    def reset_game(self):
        self.score = 0
        self.wave = 1
        self.character.life = 3
        self.character.speed = 1.0
        self.character.x = 64
        self.character.y = 64
        self.character.tirs.clear()
        self.character.invincible = 0
        self.character.orientation = 1
        self.character.droitegauche = 1
        self.character.speed_timer = 0
        self.character.shield_timer = 0
        self.potions = [Potion() for _ in range(3)]
        self.game_over = False
        self.spawn_wave(self.wave)
        pyxel.stop(0)
        pyxel.playm(0)


class Potion:
    def __init__(self, potion_type=None):
        self.x = float(random.randint(4, 116))
        self.y = float(random.randint(4, 116))
        self.type = potion_type if potion_type else random.choice(["speed", "heal", "shield"])

    def draw(self):
        ix, iy = int(self.x), int(self.y)
        pyxel.blt(ix, iy, 0, 16, 16, 8, 8, 11)
        if self.type == "speed":
            pyxel.pset(ix + 3, iy + 3, 10)
            pyxel.pset(ix + 4, iy + 3, 10)
        elif self.type == "heal":
            pyxel.pset(ix + 3, iy + 3, 14)
            pyxel.pset(ix + 4, iy + 3, 14)
        elif self.type == "shield":
            pyxel.pset(ix + 3, iy + 3, 12)
            pyxel.pset(ix + 4, iy + 3, 12)


class Character:
    TIRS_VELOCITY = 2.5

    def __init__(self):
        self.x = 64
        self.y = 64
        self.base_speed = 1.0
        self.speed = 1.0
        self.speed_timer = 0
        self.shield_timer = 0
        self.life = 3
        self.tirs = []
        self.invincible = 0
        self.orientation = 1
        self.droitegauche = 1
        self.skin = 1

    def deplacement(self):
        if pyxel.btn(pyxel.KEY_D) and self.x < 112:
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_Q) and self.x > 0:
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_S) and self.y < 112:
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_Z) and self.y > 0:
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_UP):
            self.orientation = 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.orientation = 2
            self.droitegauche = 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.orientation = 3
        if pyxel.btn(pyxel.KEY_LEFT):
            self.orientation = 4
            self.droitegauche = 2

    def tir(self):
        if pyxel.frame_count % 30 == 0:
            cx, cy = self.x + 8, self.y + 8
            if self.orientation == 1:
                self.tirs.append([1, cx, self.y])
            elif self.orientation == 2:
                self.tirs.append([2, self.x + 16, cy])
            elif self.orientation == 3:
                self.tirs.append([3, cx, self.y + 16])
            elif self.orientation == 4:
                self.tirs.append([4, self.x, cy])

    def collision(self, autre):
        return (
            self.x < autre.x + 8
            and self.x + 8 > autre.x
            and self.y < autre.y + 8
            and self.y + 8 > autre.y
        )

    def collisiontirs(self, ennemies):
        killed = []
        for tir in self.tirs[:]:
            for ennemi in ennemies[:]:
                if (tir[1] < ennemi.x + 8
                        and tir[1] + 8 > ennemi.x
                        and tir[2] < ennemi.y + 8
                        and tir[2] + 8 > ennemi.y):
                    if tir in self.tirs:
                        self.tirs.remove(tir)
                    ennemi.hp -= 1
                    if ennemi.hp <= 0:
                        ennemies.remove(ennemi)
                        killed.append(ennemi)
                    break
        return killed

    def update(self, ennemies):
        self.deplacement()
        self.tir()

        for tir in self.tirs[:]:
            if tir[0] == 1:
                tir[2] -= self.TIRS_VELOCITY
            elif tir[0] == 2:
                tir[1] += self.TIRS_VELOCITY
            elif tir[0] == 3:
                tir[2] += self.TIRS_VELOCITY
            elif tir[0] == 4:
                tir[1] -= self.TIRS_VELOCITY
            if tir[1] < -8 or tir[1] > 136 or tir[2] < -8 or tir[2] > 136:
                if tir in self.tirs:
                    self.tirs.remove(tir)

        if self.speed_timer > 0:
            self.speed_timer -= 1
            if self.speed_timer == 0:
                self.speed = self.base_speed

        if self.shield_timer > 0:
            self.shield_timer -= 1

        protected = self.invincible > 0 or self.shield_timer > 0
        if self.invincible > 0:
            self.invincible -= 1

        if not protected:
            for enemy in ennemies:
                if self.collision(enemy):
                    self.life -= 1
                    self.x = 64
                    self.y = 64
                    self.invincible = 90
                    for e in ennemies:
                        side = random.randint(0, 3)
                        if side == 0:
                            e.x, e.y = float(random.randint(0, 120)), -8.0
                        elif side == 1:
                            e.x, e.y = float(random.randint(0, 120)), 128.0
                        elif side == 2:
                            e.x, e.y = -8.0, float(random.randint(0, 120))
                        else:
                            e.x, e.y = 128.0, float(random.randint(0, 120))
                    if self.life > 0:
                        pyxel.play(2, 20)
                    else:
                        pyxel.play(0, 21)
                    break

        if pyxel.frame_count % 30 == 0:
            self.skin = 2 if self.skin == 1 else 1

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, 128, 128, 11)

        # Clignote pendant l'invincibilité post-hit (toutes les 5 frames)
        hide = self.invincible > 0 and (self.invincible // 5) % 2 == 0
        if not hide:
            if self.droitegauche == 1:
                sx = 0 if self.skin == 1 else 16
            else:
                sx = 32 if self.skin == 1 else 48
            pyxel.blt(int(self.x), int(self.y), 0, sx, 0, 15, 15, 11)

        if self.shield_timer > 0:
            pyxel.rectb(int(self.x) - 2, int(self.y) - 2, 19, 19, 12)

        for tir in self.tirs:
            pyxel.rect(int(tir[1]), int(tir[2]), 2, 2, 10)

        if pyxel.btn(pyxel.KEY_SPACE):
            pyxel.text(int(self.x) + 10, int(self.y) - 6, "skkrt paw", 7)


class Enemy:
    def __init__(self, enemy_type="basic"):
        side = random.randint(0, 3)
        if side == 0:
            self.x = float(random.randint(0, 120))
            self.y = -8.0
        elif side == 1:
            self.x = float(random.randint(0, 120))
            self.y = 128.0
        elif side == 2:
            self.x = -8.0
            self.y = float(random.randint(0, 120))
        else:
            self.x = 128.0
            self.y = float(random.randint(0, 120))

        self.type = enemy_type
        if enemy_type == "basic":
            self.speed = 0.3
            self.hp = 1
            self.points = 10
        elif enemy_type == "fast":
            self.speed = 0.5
            self.hp = 1
            self.points = 25
        elif enemy_type == "tank":
            self.speed = 0.15
            self.hp = 3
            self.points = 75

    def update(self, character):
        if self.x < character.x:
            self.x += self.speed
        else:
            self.x -= self.speed
        if self.y < character.y:
            self.y += self.speed
        else:
            self.y -= self.speed

    def draw(self):
        ix, iy = int(self.x), int(self.y)
        pyxel.blt(ix, iy, 0, 32, 24, 8, 8, 11)
        if self.type == "fast":
            # Point jaune au-dessus pour identifier les rapides
            pyxel.pset(ix + 3, iy - 2, 10)
            pyxel.pset(ix + 4, iy - 2, 10)
        elif self.type == "tank":
            # Barre de vie rouge au-dessus pour les tanks
            pyxel.rect(ix, iy - 4, 8, 2, 0)
            pyxel.rect(ix, iy - 4, max(1, int(8 * self.hp / 3)), 2, 8)


Jeu()
