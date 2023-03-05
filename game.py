import time
import pygame
import sys
from random import randint


class Enemy:
    def __init__(self, x: float, y: float, size: int, imagePath: str):
        self.x = x
        self.y = y
        self.size = size
        self.imagePath = imagePath
        # f(x) = -(1/5)x + 7
        # when x > 0 and x <= 25
        self.speed = -(1 / 5) * size + 7
        self.isMoving = True

        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)
        self.image = pygame.image.load(self.imagePath)
        self.imageScaled = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, surface: pygame.surface.Surface) -> None:
        if self.isMoving:
            self.y += self.speed
            self.update_rect()

        surface.blit(self.imageScaled, self.rect)

    def update_rect(self) -> None:
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)


def retry(surface: pygame.surface.Surface, hardMode: bool) -> dict:
    answers = {"continue": False, "hard_mode": hardMode}
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r:
                    answers["continue"] = True
                    return answers

                if event.key == pygame.K_h:
                    answers["hard_mode"] = not answers.get("hard_mode")
                    background = pygame.rect.Rect((0, 300), (WINDOW_WIDTH, 50))
                    pygame.draw.rect(windowSurface, BLACK, background)

                    hardModeMessage = "Hard mode: "
                    if answers.get("hard_mode"):
                        hardModeMessage += "on"
                    else:
                        hardModeMessage += "off"

                    hard_mode_status = basicFont.render(hardModeMessage, True, WHITE)
                    hard_mode_status_rect = hard_mode_status.get_rect()
                    hard_mode_status_rect.centerx = WINDOW_WIDTH // 2
                    hard_mode_status_rect.centery = WINDOW_HEIGHT // 2 + 72
                    surface.blit(hard_mode_status, hard_mode_status_rect)

                    pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    mainClock = pygame.time.Clock()

    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500

    windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption("Look out for the obstacles!")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Text
    basicFont = pygame.font.SysFont(None, 48)
    pressRText = basicFont.render("Press 'r' to restart", True, WHITE)
    pressRTextRect = pressRText.get_rect()
    pressRTextRect.centerx = WINDOW_WIDTH // 2
    pressRTextRect.centery = WINDOW_HEIGHT // 2 - 72

    pressEscText = basicFont.render("Press 'esc' to exit", True, WHITE)
    pressEscTextRect = pressEscText.get_rect()
    pressEscTextRect.centerx = WINDOW_WIDTH // 2
    pressEscTextRect.centery = WINDOW_HEIGHT // 2 - 24

    pressHText = basicFont.render("Press 'h' to activate hard mode", True, WHITE)
    pressHTextRect = pressHText.get_rect()
    pressHTextRect.centerx = WINDOW_WIDTH // 2
    pressHTextRect.centery = WINDOW_HEIGHT // 2 + 24

    isHard = False
    hardModeMessage = "Hard mode: "
    if isHard:
        hardModeMessage += "on"
    else:
        hardModeMessage += "off"

    hardModeStatus = basicFont.render(hardModeMessage, True, WHITE)
    hardModeStatusRect = hardModeStatus.get_rect()
    hardModeStatusRect.centerx = WINDOW_WIDTH // 2
    hardModeStatusRect.centery = WINDOW_HEIGHT // 2 + 72

    start = time.time()

    timer = basicFont.render(f"Seconds: {int(time.time() - start)}", True, BLACK)
    timerRect = timer.get_rect()
    timerRect.left = 20
    timerRect.bottom = WINDOW_HEIGHT - 20

    iterations = 0
    modulo = 6

    # Music
    pygame.mixer.music.load("assets/music.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, 57, 1000)

    gameOverSound = pygame.mixer.Sound("assets/gameOver.wav")
    gameOverSound.set_volume(0.4)

    # Game objects
    enemies = []

    player = pygame.rect.Rect(0, 0, 30, 30)
    player.centerx = WINDOW_WIDTH // 2
    player.y = WINDOW_HEIGHT - 50
    playerImage = pygame.image.load("assets/player.png")
    PLAYER_SIZE = 30
    scaledPlayerImage = pygame.transform.scale(playerImage, (PLAYER_SIZE, PLAYER_SIZE))

    offset = 0
    direction = randint(0, 1)

    hardModeSafeZoneRect = pygame.rect.Rect(0, WINDOW_HEIGHT // 3, WINDOW_WIDTH, WINDOW_HEIGHT // 3 - 60)

    pygame.draw.polygon(windowSurface, BLUE, (
        (hardModeSafeZoneRect.left, hardModeSafeZoneRect.top - 30),
        (hardModeSafeZoneRect.right, hardModeSafeZoneRect.top - 30),
        (hardModeSafeZoneRect.right, hardModeSafeZoneRect.bottom + 30),
        (hardModeSafeZoneRect.left, hardModeSafeZoneRect.bottom + 30)))

    while True:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEMOTION:
                player.x = event.pos[0] - PLAYER_SIZE // 2
                player.y = event.pos[1] - PLAYER_SIZE // 2

        iterations += 1

        if iterations % 300 == 0 and modulo > 2:
            iterations = 0
            modulo -= 1

        if iterations % modulo == 0:
            size = randint(10, 25)
            enemies.append(Enemy(randint(size, WINDOW_WIDTH - size), -50, size, "assets/baddie.png"))

        if isHard:
            windowSurface.fill(RED)

            if hardModeSafeZoneRect.top < 25 + 30:
                offset += 1.5
            elif hardModeSafeZoneRect.bottom > WINDOW_HEIGHT - 25:
                offset -= 1.5
            else:
                if iterations % 3 == 0:
                    direction = randint(0, 1)

                if direction:
                    offset += 1.5
                else:
                    offset -= 1.5

            hardModeSafeZoneRect.centery = WINDOW_HEIGHT // 2 + offset

            pygame.draw.polygon(windowSurface, BLUE, (
                (hardModeSafeZoneRect.left, hardModeSafeZoneRect.top - 30),
                (hardModeSafeZoneRect.right, hardModeSafeZoneRect.top - 30),
                (hardModeSafeZoneRect.right, hardModeSafeZoneRect.bottom + 30),
                (hardModeSafeZoneRect.left, hardModeSafeZoneRect.bottom + 30)))

        else:
            windowSurface.fill(WHITE)

        for enemy in enemies:
            enemy.draw(windowSurface)

        windowSurface.blit(scaledPlayerImage, player)

        timer = basicFont.render(f"Seconds: {int(time.time() - start)}", True, BLACK)
        windowSurface.blit(timer, timerRect)

        isOutOfBounds = (player.x <= 0 or player.right >= WINDOW_WIDTH) or (
                player.y <= 0 or player.bottom >= WINDOW_HEIGHT)

        for enemy in enemies[:]:
            # If collides with enemy or is out of bounds or (when in hard mode) has left his safe zone
            if player.colliderect(enemy) or isOutOfBounds or (isHard and not player.colliderect(hardModeSafeZoneRect)):
                menu_background = pygame.rect.Rect((0, 150), (WINDOW_WIDTH, WINDOW_HEIGHT - 300))
                pygame.draw.rect(windowSurface, BLACK, menu_background)
                windowSurface.blit(pressRText, pressRTextRect)
                windowSurface.blit(pressEscText, pressEscTextRect)
                windowSurface.blit(pressHText, pressHTextRect)

                hardModeMessage = "Hard mode: "
                if isHard:
                    hardModeMessage += "on"
                else:
                    hardModeMessage += "off"

                hardModeStatus = basicFont.render(hardModeMessage, True, WHITE)
                hardModeStatusRect = hardModeStatus.get_rect()
                hardModeStatusRect.centerx = WINDOW_WIDTH // 2
                hardModeStatusRect.centery = WINDOW_HEIGHT // 2 + 72
                windowSurface.blit(hardModeStatus, hardModeStatusRect)

                pygame.display.update()

                pygame.mixer.music.stop()
                gameOverSound.play()

                # Death menu
                answer = retry(windowSurface, isHard)

                if answer.get("continue"):
                    modulo = 6
                    iterations = 0
                    enemies = []
                    start = time.time()
                    gameOverSound.stop()
                    pygame.mixer.music.play(-1, 57, 1000)
                    player = pygame.rect.Rect(0, 0, 30, 30)
                    player.centerx = WINDOW_WIDTH // 2
                    player.centery = WINDOW_HEIGHT // 2
                    isOutOfBounds = False
                    isHard = answer.get("hard_mode")

                    if isHard:
                        pygame.display.set_caption("Look out for the obstacles and stay in safe zone!")
                    else:
                        pygame.display.set_caption("Look out for the obstacles!")

                    hardModeSafeZoneRect.centery = WINDOW_HEIGHT // 2
                    offset = 0

                else:
                    pygame.quit()
                    sys.exit()

            elif enemy.y > WINDOW_HEIGHT:
                # Don't look at this too much
                # I don't know why game throws here error sometimes
                try:
                    enemies.remove(enemy)
                except ValueError:
                    pass

        pygame.display.update()

        mainClock.tick(30)
