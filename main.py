import pygame
import pygame_menu
import random

pygame.init()

W, H = 700, 600
FPS = 60
clock = pygame.time.Clock()

back = 'back.jpg'

difficulty = 1

ball_y = None
ballx, bally = 5, -5
SPEED = 8  
PLAYER_SPEED = 8  
BOUNCED = 0
BOUNCED_2 = 0

player = None
enemy = None
player_2 = None
ball = None

AI_win = False
Human_win = False

window = pygame.display.set_mode((W, H))

background = pygame.transform.scale(
    pygame.image.load(back), 
    (W, H)
)

def set_diff(selected, value):
    global difficulty
    difficulty = value


pygame.font.init()
font = pygame.font.SysFont('Impact', 40)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, playerx, playery, player_height, player_width):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (player_width, player_height))
        self.rect = self.image.get_rect()
        self.rect.x = playerx
        self.rect.y = playery
        self.player_height = player_height
        self.player_width = player_width

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ball(GameSprite):
    def __init__(self, player_image, playerx, playery, player_height, player_width):
        super().__init__(player_image, playerx, playery, player_height, player_width)

    def moving(self):
        global AI_win, Human_win, ball_y, ballx, bally
        self.rect.x += ballx
        self.rect.y += bally

        if self.rect.y <= 0 or self.rect.y >= H - self.player_height: 
            bally *= -1

        if self.rect.x >= W: 
            Human_win = True
        elif self.rect.x <= 0: 
            AI_win = True

        ball_y = self.rect.y

class Enemy(GameSprite):
    def __init__(self, player_image, playerx, playery, player_height, player_width):
        super().__init__(player_image, playerx, playery, player_height, player_width)

    def moving(self):
        global SPEED, difficulty
        error_margin = random.uniform(-8, 8) if random.random() < 0.3 else 0
        target_y = ball_y + error_margin

        if target_y is not None:
            if self.rect.y > target_y:
                self.rect.y -= SPEED - difficulty
            elif self.rect.y < target_y:
                self.rect.y += SPEED - difficulty

            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > H - self.player_height:
                self.rect.y = H - self.player_height


class Player(GameSprite):
    def __init__(self, player_image, playerx, playery, player_height, player_width, keys):
        super().__init__(player_image, playerx, playery, player_height, player_width)
        self.keys = keys

    def moving(self):
        keys = pygame.key.get_pressed()
        
        if keys[self.keys['up']] and self.rect.y > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[self.keys['down']] and self.rect.y < H - self.player_height: 
            self.rect.y += PLAYER_SPEED


def ai():
    global player, enemy, ball
    player = Player('image.png', 10, 250, 100, 35, keys={'up': pygame.K_UP, 'down': pygame.K_DOWN})
    enemy = Enemy('image.png', 640, 250, 100, 35)
    ball = Ball('ball.png', 295, 240, 35, 35)
    return player, enemy, ball

def not_ai():
    global player, player_2, ball
    player = Player('image.png', 10, 250, 100, 35, keys={'up': pygame.K_w, 'down': pygame.K_s})
    player_2 = Player('image.png', 640, 250, 100, 35, keys={'up': pygame.K_UP, 'down': pygame.K_DOWN})
    ball = Ball('ball.png', 295, 240, 35, 35)
    return player, player_2, ball

def reset_game():
    global AI_win, Human_win, ballx, bally, PLAYER_SPEED, SPEED, BOUNCED, player, player_2, enemy, BOUNCED_2
    ball.rect.x, ball.rect.y = 295, 240
    player.rect.y = 250
    player.rect.x = 10
    try:
        enemy.rect.y = 250
        enemy.rect.x = 640
    except:
        player_2.rect.y = 250
        player_2.rect.x = 640
    AI_win, Human_win = False, False
    ballx, bally = 5, -5
    PLAYER_SPEED, SPEED = 8, 8
    BOUNCED, BOUNCED_2 = 0, 0

def ball_bounce():
    global ballx, bally, SPEED, PLAYER_SPEED, BOUNCED
    random_angle = random.uniform(-1, 1)

    if pygame.sprite.collide_rect(ball, player):
        ballx = abs(ballx) + 0.5
        bally += random_angle
        PLAYER_SPEED += 0.3  
        BOUNCED += 1

    elif pygame.sprite.collide_rect(ball, enemy):
        ballx = -abs(ballx) - 0.5
        bally += random_angle
        SPEED += 0.3 

def ball_bounce_not_ai():
    global ballx, bally, SPEED, PLAYER_SPEED, BOUNCED, BOUNCED_2 
    random_angle = random.uniform(-1, 1)

    if pygame.sprite.collide_rect(ball, player):
        ballx = abs(ballx) + 0.5
        bally += random_angle
        PLAYER_SPEED += 0.3  
        BOUNCED += 1

    elif pygame.sprite.collide_rect(ball, player_2):
        ballx = -abs(ballx) - 0.5
        bally += random_angle
        SPEED += 0.3 
        BOUNCED_2 += 1

def ai_game():
    global PLAYER_SPEED, SPEED, BALL, ballx, bally
    player, enemy, ball = ai()
    reset_game()
    if difficulty == 1:
        PLAYER_SPEED, SPEED = 9, 6.5
        ballx, bally = 4, -4
    elif difficulty == 2:
        PLAYER_SPEED, SPEED = 8, 8
        ballx, bally = 5, -5
    elif difficulty == 3:
        PLAYER_SPEED, SPEED = 6.5, 9
        ballx, bally = 5.8, -5.8
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu()

        window.blit(background, (0, 0))
        text_bounced = font.render(f'Отбито: {BOUNCED} раз', True, (255, 255, 255))
        window.blit(text_bounced, (10, 40))
        player.reset()
        enemy.reset()
        player.moving()
        ball.moving()
        ball.reset()
        enemy.moving()
        ball_bounce()

        clock.tick(FPS)
        pygame.display.flip()

        if AI_win or Human_win:
            reset_game()
            break

def not_ai_game():
    global PLAYER_SPEED, BALL, ballx, bally
    player, player_2, ball = not_ai()
    reset_game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu()

        window.blit(background, (0, 0))
        text_bounced = font.render(f'Отбито: {BOUNCED} раз', True, (255, 255, 255))
        text_bounced_2 = font.render(f'Отбито: {BOUNCED_2} раз', True, (255, 255, 255))
        window.blit(text_bounced, (10, 40))
        window.blit(text_bounced_2, (500, 40))
        player.reset()
        player_2.reset()
        player.moving()
        ball.moving()
        ball.reset()
        player_2.moving()
        ball_bounce_not_ai()

        clock.tick(FPS)
        pygame.display.flip()

        if AI_win or Human_win:
            reset_game()
            break



def start_menu():
    global AI_win, BOUNCED, difficulty
    if AI_win:
        text = f'Вы проиграли, ваш результат: {BOUNCED}'
    else:
        text = 'Ping-Pong'
    menu = pygame_menu.Menu(text, W, H, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Игра с компьютером', ai_game)
    menu.add.selector(
        'Сложность', 
        [('Легко', 1), ('Средне', 2), ('Сложно', 3)], 
        onchange=set_diff
    )
    menu.add.button('Игра с другом', not_ai_game)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(window)

if __name__ == "__main__":
    start_menu()
