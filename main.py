import pygame
from elements import *
from attributes import *
pygame.init()

FPS = 60


class Screen:
    TITLE = 0
    GAME = 1
    SHOP = 2
    GUI = 3

    def __init__(self, game):
        self.game = game
        self.WIN = game.WIN

    def draw(self):
        """Draws elements for each frame
        """
        pass

    def events(self, event):
        """Parses Events for each frame"""
        pass

    def compute(self):
        """Computes live elements on screen"""
        pass

    def clear(self):
        """Runs at the start of each frame, use to clear any buffers"""
        pass


class Title(Screen):
    def __init__(self, *args):
        super().__init__(*args)

        self.type = ScreenType.TITLE

        self.play_button = Button(self.type, (Position.MIDDLE, Position.MIDDLE), (200, 50),
                                  "Play", color=Color.GOBLIN_PURPLE, text_color=Color.WHITE, font_size=30)

    def draw(self):
        self.WIN.fill(Color.WHITE)

        Text("GOBLINZ", 120, Color.GOBLIN_GREEN,
             (Position.MIDDLE, HEIGHT // 10)).blit(self.WIN)

        self.play_button.blit(self.WIN)

    def events(self, event):
        self.play_button.on_click(event, self.play)

    def play(self):
        self.game.current_screen = Screen.GAME


class Game(Screen):
    def __init__(self, game):
        super().__init__(game)

        self.type = ScreenType.GAME

        self.goblin = Goblin()
        self.child = Child()

        self.move_dir = []

        self.show_hitboxes = False

    def draw(self):
        self.WIN.fill(Color.WHITE)

        Text("This is game", 120, Color.GOBLIN_GREEN,
             (Position.MIDDLE, HEIGHT // 10)).blit(self.WIN)

        self.child.blit(self.WIN, hitboxes=self.show_hitboxes)
        self.goblin.blit(self.WIN, hitboxes=self.show_hitboxes)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                if self.show_hitboxes:
                    self.show_hitboxes = False
                else:
                    self.show_hitboxes = True

            if event.key == pygame.K_r:
                self.child.not_die()

    def compute(self):
        self.goblin.move(pygame.key.get_pressed())
        self.goblin.animate()

        if self.goblin.feet_hitbox.colliderect(self.child.head_hitbox):
            if self.goblin.jump_count < 0:
                if self.child.alive:
                    self.goblin.jump_count = 10
                self.child.die()


class GUI(Screen):
    def __init__(self, game):
        super().__init__(game)

        self.type = ScreenType.GUI

    def draw(self):
        pass

    def events(self, event):
        pass

    def compute(self):
        pass


class Main:
    def __init__(self):
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Goblinz")

        self.clock = pygame.time.Clock()

        Screen.TITLE = Title(self)
        Screen.GAME = Game(self)
        Screen.GUI = GUI(self)

        self.current_screen = Screen.TITLE

    def gameloop(self):
        run = True
        while run:
            self.current_screen.clear()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                self.current_screen.events(event)

            if run == False:
                pygame.quit()
                break

            self.current_screen.compute()
            self.current_screen.draw()

            pygame.display.update()

            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Main()
    game.gameloop()
