import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

def play_game():
    pygame.init()

    COLOR_RED = (255, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_GREEN = (0, 255, 0)

    DISPLAY_HEIGHT = 400
    DISPLAY_WIDTH = 600

    FPS = pygame.time.Clock()

    PLAYER_SIZE = (20, 20)
    PLAYER_STEP_UP = [0, -1]
    PLAYER_STEP_DOWN = [0, 1]
    PLAYER_STEP_LEFT = [-1, 0]
    PLAYER_STEP_RIGHT = [1, 0]

    ENEMY_SIZE = (40, 40)
    BONUS_SIZE = (30, 30)

    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    player = pygame.Surface(PLAYER_SIZE)
    player.fill(COLOR_RED)
    player_rect = pygame.Rect((DISPLAY_WIDTH-PLAYER_SIZE[0])/4,
                              (DISPLAY_HEIGHT-PLAYER_SIZE[1])/2,
                              *PLAYER_SIZE)

    def create_enemy():
        enemy = pygame.Surface(ENEMY_SIZE)
        enemy.fill(COLOR_BLACK)
        enemy_rect = pygame.Rect(DISPLAY_WIDTH, random.randint(0, DISPLAY_HEIGHT-ENEMY_SIZE[1]), *ENEMY_SIZE)
        enemy_move = [random.randint(-6, -1), 0]
        return [enemy, enemy_rect, enemy_move]

    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 1500)

    def create_bonus():
        bonus = pygame.Surface(BONUS_SIZE)
        bonus.fill(COLOR_GREEN)
        bonus_rect = pygame.Rect(random.randint(0, DISPLAY_WIDTH-BONUS_SIZE[1]), -BONUS_SIZE[1], *BONUS_SIZE)
        bonus_move = [0, random.randint(1, 3)]
        return [bonus, bonus_rect, bonus_move]

    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 3000)

    enemies = []
    bonuses = []

    playing = True

    while playing:
        FPS.tick(200)
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())

        game_display.fill(COLOR_WHITE)
        game_display.blit(player, player_rect)

        keys = pygame.key.get_pressed()

        if keys[K_UP] and player_rect.top >= 0:
            player_rect = player_rect.move(PLAYER_STEP_UP)
        if keys[K_DOWN] and player_rect.bottom <= DISPLAY_HEIGHT:
            player_rect = player_rect.move(PLAYER_STEP_DOWN)
        if keys[K_LEFT] and player_rect.left >= 0:
            player_rect = player_rect.move(PLAYER_STEP_LEFT)
        if keys[K_RIGHT] and player_rect.right <= DISPLAY_WIDTH:
            player_rect = player_rect.move(PLAYER_STEP_RIGHT)

        for enemy in enemies:
            game_display.blit(enemy[0], enemy[1])
            enemy[1] = enemy[1].move(enemy[2])
            if enemy[1].right < 0:
                enemies.pop(enemies.index(enemy))

        for bonus in bonuses:
            game_display.blit(bonus[0], bonus[1])
            bonus[1] = bonus[1].move(bonus[2])
            if bonus[1].top > DISPLAY_HEIGHT:
                bonuses.pop(bonuses.index(bonus))

        pygame.display.flip()

if __name__ == '__main__':
    play_game()


