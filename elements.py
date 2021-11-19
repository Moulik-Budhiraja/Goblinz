import pygame
from attributes import *
import os


class Text:
    def __init__(self, text: str,  font_size: int, color: tuple = Color.BLACK, position: tuple = (Position.LEFT, Position.TOP), center: tuple = None):
        self.font = pygame.font.SysFont("Anton-Regular", font_size)
        self.color = color
        self.text = text

        self.render()

        position_horizontal, position_vertical = position

        if isinstance(position_horizontal, Position):
            self.position_horizontal = self.horizontal_position(
                position_horizontal)
        else:
            self.position_horizontal = position_horizontal

        if isinstance(position_vertical, Position):
            self.position_vertical = self.vertical_position(position_vertical)
        else:
            self.position_vertical = position_vertical

        if center != None:
            width = center[0]
            height = center[1]

            self.position_horizontal = self.position_horizontal + \
                (width - self.rendered.get_width()) // 2
            self.position_vertical = self.position_vertical + \
                (height - self.rendered.get_height()) // 2

    def render(self):
        self.rendered = self.font.render(self.text, True, self.color)

    def blit(self, surface):
        surface.blit(
            self.rendered, (self.position_horizontal, self.position_vertical))

    def horizontal_position(self, position):
        if position == Position.LEFT:
            return 0
        elif position == Position.RIGHT:
            return WIDTH - self.rendered.get_width()
        elif position == Position.MIDDLE:
            return (WIDTH - self.rendered.get_width()) // 2
        else:
            return 0

    def vertical_position(self, position):
        if position == Position.TOP:
            return 0
        elif position == Position.BOTTOM:
            return HEIGHT - self.rendered.get_height()
        elif position == Position.MIDDLE:
            return (HEIGHT - self.rendered.get_height()) // 2
        else:
            return 0


class Button:
    screens = {ScreenType.TITLE: [], ScreenType.GAME: [], ScreenType.SHOP: []}

    def __init__(self, screen, position: tuple, dimensions: tuple, text='', color=Color.WHITE, text_color=Color.BLACK, font_size=20):
        self.screens[screen].append(self)
        self.width, self.height = dimensions
        self.color = color

        if isinstance(position[0], Position):
            self.x = self.horizontal_position(position[0])
        else:
            self.x = position[0]

        if isinstance(position[1], Position):
            self.y = self.vertical_position(position[1])
        else:
            self.y = position[1]

        self.text = Text(text, font_size, text_color, (self.horizontal_position(
            position[0]), self.vertical_position(position[1])), dimensions)
        self.hitbox = pygame.Rect(
            self.x, self.y, *dimensions)

    def blit(self, surface):
        pygame.draw.rect(surface, self.color, self.hitbox)
        self.text.blit(surface)

    def horizontal_position(self, position):
        if position == Position.LEFT:
            return 0
        elif position == Position.RIGHT:
            return WIDTH - self.width
        elif position == Position.MIDDLE:
            return (WIDTH - self.width) // 2
        else:
            return 0

    def vertical_position(self, position):
        if position == Position.TOP:
            return 0
        elif position == Position.BOTTOM:
            return HEIGHT - self.height
        elif position == Position.MIDDLE:
            return (HEIGHT - self.height) // 2
        else:
            return 0

    def on_click(self, event, function):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hitbox.collidepoint(event.pos):
                function()


class Goblin:
    goblins = [pygame.image.load(os.path.join(
        "assets", "goblins", f"Goblin {i}.png")) for i in range(1, 6)]
    idle_goblin = pygame.image.load(
        os.path.join("assets", "goblins", "Goblin idle.png"))
    jump_goblins = [pygame.image.load(os.path.join(
        "assets", "goblins", f"Goblin Jump {i}.png")) for i in range(1, 4)]

    goblins = [pygame.transform.scale(i, (200, 200)) for i in goblins]
    idle_goblin = pygame.transform.scale(idle_goblin, (200, 200))
    jump_goblins = [pygame.transform.scale(
        i, (200, 200)) for i in jump_goblins]

    inverse_goblins = [pygame.transform.flip(
        i, True, False) for i in goblins]
    inverse_idle_goblin = pygame.transform.flip(
        idle_goblin, True, False)
    inverse_jump_goblins = [pygame.transform.flip(
        i, True, False) for i in jump_goblins]

    def __init__(self, location: tuple = (450, 275), size: tuple = (200, 200)):
        # Load goblins
        self.current_goblin = self.idle_goblin
        self.idle = True

        # MOVEMENT

        self.x, self.y = location
        self.width, self.height = size
        self.VEL = 7

        self.is_jumping = False
        self.jump_count = 10

        # TEXTURES

        self.facing = Direction.RIGHT
        self.last_facing = Direction.RIGHT

        self.frame = 0

        # HITBOXS

        self.hitbox = pygame.Rect(
            self.x + self.width * 0.2, self.y + self.height * 0.2, self.width * 0.6, self.height * 0.7)

        self.feet_hitbox = pygame.Rect(
            self.x + self.width * 0.3, self.y + self.height * 0.8, self.width * 0.4, self.height * 0.1)

    def blit(self, surface, hitboxes: bool = False):
        surface.blit(self.current_goblin, (self.x, self.y))
        if hitboxes:
            pygame.draw.rect(surface, Color.RED, self.hitbox, 2)
            pygame.draw.rect(surface, Color.RED, self.feet_hitbox, 2)

    def move(self, keys: list):
        dir = []
        if keys[pygame.K_LEFT]:
            dir.append(Direction.LEFT)
        if keys[pygame.K_RIGHT]:
            dir.append(Direction.RIGHT)
        if keys[pygame.K_UP]:
            if not self.is_jumping:
                self.is_jumping = True
                self.jump_count = 10

        for i in dir:
            if i == Direction.UP:
                self.y -= self.VEL

            elif i == Direction.DOWN:
                self.y += self.VEL

            elif i == Direction.LEFT:
                self.x -= self.VEL
                self.facing = Direction.LEFT

            elif i == Direction.RIGHT:
                self.x += self.VEL
                self.facing = Direction.RIGHT

        if self.is_jumping:
            if self.y <= 275:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) // 4 * neg
                self.jump_count -= 0.5
            else:
                self.is_jumping = False
                self.jump_count = 10
                self.y = 275

        if dir == []:
            self.idle = True

        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox.x = self.x + self.width * 0.2
        self.hitbox.y = self.y + self.height * 0.2

        self.feet_hitbox.x = self.x + self.width * 0.3
        self.feet_hitbox.y = self.y + self.height * 0.8

    def animate(self):
        self.frame += 1

        if self.idle:
            if self.facing == Direction.RIGHT:
                self.current_goblin = self.idle_goblin
            else:
                self.current_goblin = self.inverse_idle_goblin
            self.idle = False
            self.frame = 0

        else:
            if self.facing == Direction.RIGHT:
                self.current_goblin = self.goblins[int((self.frame // 5) % 5)]
            else:
                self.current_goblin = self.inverse_goblins[int((
                    self.frame // 5) % 5)]

        if self.is_jumping:
            if self.facing == Direction.RIGHT:
                if self.jump_count > 0:
                    self.current_goblin = self.jump_goblins[0]
                elif self.jump_count > -6:
                    self.current_goblin = self.jump_goblins[1]
                else:
                    self.current_goblin = self.jump_goblins[2]
            else:
                if self.jump_count > 0:
                    self.current_goblin = self.inverse_jump_goblins[0]
                elif self.jump_count > -6:
                    self.current_goblin = self.inverse_jump_goblins[1]
                else:
                    self.current_goblin = self.inverse_jump_goblins[2]


class Child:
    def __init__(self, location: tuple = (650, 330), size: tuple = (150, 150)):
        self.child = pygame.image.load(os.path.join(
            "assets", "goblins", "Goblin test.png"))
        self.child = pygame.transform.scale(self.child, size)

        self.x, self.y = location
        self.width, self.height = size
        self.VEL = 5

        self.facing = Direction.RIGHT
        self.last_facing = Direction.RIGHT

        self.alive = True

        # HITBOXS

        self.hitbox = pygame.Rect(self.x + self.width * 0.2, self.y +
                                  self.height * 0.2, self.width * 0.6, self.height * 0.65)

        self.head_hitbox = pygame.Rect(
            self.x + self.width * 0.2, self.y + self.height * 0.2, self.width * 0.6, self.height * 0.2)

    def blit(self, surface, hitboxes: bool = False):
        surface.blit(self.child, (self.x, self.y))
        if hitboxes:
            pygame.draw.rect(surface, Color.RED, self.hitbox, 2)
            pygame.draw.rect(surface, Color.RED, self.head_hitbox, 2)

    def move(self, dir: list):
        pass

    def update_hitbox(self):
        self.hitbox.x = self.x + self.width * 0.2
        self.hitbox.y = self.y + self.height * 0.2

        self.head_hitbox.x = self.x + self.width * 0.2
        self.head_hitbox.y = self.y + self.height * 0.2

    def animate(self):
        if self.facing != self.last_facing:
            self.last_facing = self.facing

    def not_die(self):
        if not self.alive:
            self.alive = True
            self.child = pygame.transform.rotate(self.child, -90)

    def die(self):
        if self.alive:
            self.child = pygame.transform.rotate(self.child, 90)
            self.alive = False
