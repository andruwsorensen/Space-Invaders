import pygame
import sys
import random

pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Initialize clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Player:
    def __init__(self, x, y):
        self.lives = 3
        self.original_image = pygame.image.load("player_ship/Fighter/Idle.png")
        self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() // 2, self.original_image.get_height() // 2))
        self.image = pygame.transform.rotate(self.original_image, 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center

    def move_left(self):
        self.rect.x = max(0, self.rect.x - self.speed)
        self.hitbox.center = self.rect.center

    def move_right(self):
        self.rect.x = min(width - self.rect.width, self.rect.x + self.speed)
        self.hitbox.center = self.rect.center

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def collides_with(self, enemy):
        return self.hitbox.colliderect(enemy.hitbox)

class Enemy:
    def __init__(self, x, y):
        self.original_image = pygame.image.load("enemy_ship/PNG_Parts&Spriter_Animation/Ship2/Ship2.png")
        self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() // 2, self.original_image.get_height() // 2))
        self.image = pygame.transform.rotate(self.original_image, 90)  # Rotate 180 degrees to face downwards
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 2  # This will be overwritten in spawn_enemies
        self.direction = 1  # 1 for right, -1 for left
        self.shoot_cooldown = 0
        self.shoot_delay = random.randint(60, 180)  # Random delay between 1-3 seconds
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center
        self.max_y = height * 0.6  # Maximum y-position (60% of screen height)
        self.min_y = 50

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0:
            self.direction = 1
            self.rect.left = 0
            self.rect.y += 20
        elif self.rect.right >= width:
            self.direction = -1
            self.rect.right = width
            self.rect.y += 20
        
        if self.rect.bottom > self.max_y:
            self.rect.bottom = self.max_y
        if self.rect.top < self.min_y:
            self.rect.top = self.min_y
        
        self.hitbox.center = self.rect.center

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            self.shoot_delay = random.randint(60, 180)  # Reset the delay
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None

    def update(self):
        self.move()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def collides_with(self, bullet):
        return self.hitbox.colliderect(bullet.hitbox)

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("player_ship/Fighter/Charge_1.png")
        self.image = pygame.transform.rotate(self.image, -90)  # Rotate to face upwards
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 7
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.7)
        self.hitbox.center = self.rect.center

    def move(self):
        self.rect.y -= self.speed
        self.hitbox.center = self.rect.center

    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

class EnemyBullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("enemy_ship/PNG_Animations/Shots/Shot1/shot1_asset.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.7)
        self.hitbox.center = self.rect.center

    def move(self):
        self.rect.y += self.speed
        self.hitbox.center = self.rect.center

    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

def spawn_enemies(num_enemies, round_number):
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(50, width - 50)
        y = random.randint(50, height // 3)
        enemy = Enemy(x, y)
        enemy.speed = min(2 + round_number * 0.5, 5)  # Increase speed, max out at 5
        enemies.append(enemy)
    return enemies

def game():
    player = Player(width // 2, height - 50)
    round_number = 1
    enemies = spawn_enemies(5 + round_number, round_number)
    bullets = []
    enemy_bullets = []
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(player.shoot())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()

        for enemy in enemies:
            enemy.update()
            bullet = enemy.shoot()
            if bullet:
                enemy_bullets.append(bullet)

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if enemy.collides_with(bullet):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 10
                        break

        for bullet in enemy_bullets[:]:
            bullet.move()
            if bullet.rect.top > height:
                enemy_bullets.remove(bullet)
            elif player.collides_with(bullet):
                if bullet in enemy_bullets:  # Check if bullet is still in the list
                    enemy_bullets.remove(bullet)
                player.lives -= 1
                if player.lives <= 0:
                    if game_over_menu(score):
                        # Reset the game state
                        player = Player(width // 2, height - 50)
                        round_number = 1
                        enemies = spawn_enemies(5 + round_number, round_number)
                        bullets = []
                        enemy_bullets = []
                        score = 0
                    else:
                        running = False
                break  # Exit the loop after collision to avoid multiple hits

        if not enemies:
            round_number += 1
            enemies = spawn_enemies(5 + round_number, round_number)

        screen.fill(BLACK)

        player.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()
        for bullet in enemy_bullets:
            bullet.draw()

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        round_text = font.render(f"Round: {round_number}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(round_text, (width - 150, 10))

        pygame.display.flip()
        clock.tick(FPS)

def game_over_menu(score):
    play_again_button = Button(width//2 - 100, height//2 - 50, 200, 50, "Play Again", WHITE, BLACK, 36)
    quit_button = Button(width//2 - 100, height//2 + 50, 200, 50, "Quit Game", WHITE, BLACK, 36)

    while True:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_clicked(event.pos):
                    return True
                if quit_button.is_clicked(event.pos):
                    return False

        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//4))
        screen.blit(score_text, (width//2 - score_text.get_width()//2, height//3))

        play_again_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

def start_menu():
    start_button = Button(width//2 - 100, height//2 - 50, 200, 50, "Start Game", WHITE, BLACK, 36)
    quit_button = Button(width//2 - 100, height//2 + 50, 200, 50, "Quit Game", WHITE, BLACK, 36)

    while True:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    return True
                if quit_button.is_clicked(event.pos):
                    return False

        start_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

# Add this Button class just above the start_menu function
class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    while True:
        if start_menu():
            game()
        else:
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()