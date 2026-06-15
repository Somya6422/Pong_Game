import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 150, 255)

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game - AI Edition")
clock = pygame.time.Clock()

score_font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 40)

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def move(self, up=True):
        if up and self.y - self.speed >= 0:
            self.y -= self.speed
        elif not up and self.y + self.height + self.speed <= HEIGHT:
            self.y += self.speed
        self.rect.y = self.y
    def ai_move(self, ball):
        if ball.x_vel > 0:
            paddle_center = self.y + self.height / 2
            if paddle_center < ball.y - 10:
                self.move(up=False)
            elif paddle_center > ball.y + 10:
                self.move(up=True)
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.max_vel = 7
        self.x_vel = self.max_vel
        self.y_vel = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = self.x
        self.rect.y = self.y
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
    def reset(self):
        self.x = WIDTH // 2 - self.size // 2
        self.y = HEIGHT // 2 - self.size // 2
        self.x_vel *= -1 
        self.y_vel = 0

def draw_window(surface, left_paddle, right_paddle, ball, left_score, right_score):
    surface.fill(BLACK)
    
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(surface, GRAY, (WIDTH // 2 - 2, i, 4, HEIGHT // 40))

    left_score_text = score_font.render(str(left_score), True, WHITE)
    right_score_text = score_font.render(str(right_score), True, WHITE)
    surface.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    surface.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    left_paddle.draw(surface)
    right_paddle.draw(surface)
    ball.draw(surface)
    pygame.display.update()

def handle_collisions(ball, left_paddle, right_paddle):
    if ball.y + ball.size >= HEIGHT or ball.y <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if left_paddle.rect.colliderect(ball.rect):
            ball.x_vel *= -1
            middle_y = left_paddle.y + left_paddle.height / 2
            difference_in_y = middle_y - ball.y
            reduction_factor = (left_paddle.height / 2) / ball.max_vel
            ball.y_vel = -1 * (difference_in_y / reduction_factor)
    elif ball.x_vel > 0:
        if right_paddle.rect.colliderect(ball.rect):
            ball.x_vel *= -1
            middle_y = right_paddle.y + right_paddle.height / 2
            difference_in_y = middle_y - ball.y
            reduction_factor = (right_paddle.height / 2) / ball.max_vel
            ball.y_vel = -1 * (difference_in_y / reduction_factor)

def show_winner(winner_text):
    screen.fill(BLACK)
    text = score_font.render(winner_text, True, WHITE)
    sub_text = menu_font.render("Press Any Key to Return", True, GRAY)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main_menu():
    run = True
    btn_single = Button(WIDTH // 2 - 150, 200, 300, 60, "Single Player (vs AI)", button_font, DARK_GRAY, WHITE)
    btn_multi = Button(WIDTH // 2 - 150, 280, 300, 60, "Local Multiplayer", button_font, DARK_GRAY, WHITE)
    target_score = "5"
    input_box = pygame.Rect(WIDTH // 2 + 50, 380, 80, 50)
    input_active = False
    while run:
        screen.fill(BLACK)
        title = score_font.render("PONG", True, WHITE)
        score_prompt = menu_font.render("Winning Score:", True, GRAY)
        quit_text = button_font.render("Press ESC to Quit", True, DARK_GRAY)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        screen.blit(score_prompt, (WIDTH // 2 - 200, 390))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 520))
        btn_single.draw(screen)
        btn_multi.draw(screen)
        box_color = BLUE if input_active else DARK_GRAY
        pygame.draw.rect(screen, box_color, input_box, border_radius=5)
        score_text_surface = menu_font.render(target_score, True, WHITE if not input_active else BLACK)
        screen.blit(score_text_surface, (input_box.x + 15, input_box.y + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_single.is_clicked(event):
                final_score = int(target_score) if target_score.isdigit() and int(target_score) > 0 else 5
                return True, final_score 
            if btn_multi.is_clicked(event):
                final_score = int(target_score) if target_score.isdigit() and int(target_score) > 0 else 5
                return False, final_score
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        target_score = target_score[:-1]
                    elif event.unicode.isnumeric() and len(target_score) < 3:
                        target_score += event.unicode

def game_loop(ai_mode, target_score):
    run = True
    left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)
    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(up=True)
        if keys[pygame.K_s]:
            left_paddle.move(up=False)
        if ai_mode:
            right_paddle.ai_move(ball)
        else:
            if keys[pygame.K_UP]:
                right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                right_paddle.move(up=False)
        ball.move()
        handle_collisions(ball, left_paddle, right_paddle)
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x + ball.size > WIDTH:
            left_score += 1
            ball.reset()
        draw_window(screen, left_paddle, right_paddle, ball, left_score, right_score)

        if left_score >= target_score:
            show_winner("Player 1 Wins!")
            run = False
        elif right_score >= target_score:
            winner = "AI Wins!" if ai_mode else "Player 2 Wins!"
            show_winner(winner)
            run = False

if __name__ == '__main__':
    while True:
        ai_enabled, win_score = main_menu()
        game_loop(ai_enabled, win_score)
