import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

def angle_to_vector(angle):
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)

class Player:
    def __init__(self):
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 255, 255), [(20, 0), (0, 40), (40, 40)])
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.angle = 0
        self.speed = 0
        self.vel = pygame.Vector2(0, 0)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            ax, ay = angle_to_vector(self.angle)
            self.vel.x += ax * 0.2
            self.vel.y -= ay * 0.2

        self.vel *= 0.99  
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

class Asteroid:
    def __init__(self, x, y, size=3):
        self.size = size
        self.image = pygame.Surface((size * 20, size * 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (size * 10, size * 10), size * 10)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Bullet:
    def __init__(self, x, y, angle):
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        ax, ay = angle_to_vector(angle)
        self.vel = pygame.Vector2(ax * 6, -ay * 6)

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            bullets.remove(self)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

player = Player()
asteroids = [Asteroid(random.randint(0, WIDTH), random.randint(0, HEIGHT), 3) for _ in range(5)]
bullets = []
running = True

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Bullet(player.rect.centerx, player.rect.centery, player.angle))

    player.update()
    for bullet in bullets[:]:
        bullet.update()
    for asteroid in asteroids[:]:
        asteroid.update()

    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if bullet.rect.colliderect(asteroid.rect):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                if asteroid.size > 1:
                    asteroids.append(Asteroid(asteroid.rect.x, asteroid.rect.y, asteroid.size - 1))
                    asteroids.append(Asteroid(asteroid.rect.x, asteroid.rect.y, asteroid.size - 1))
                break

    for asteroid in asteroids:
        if player.rect.colliderect(asteroid.rect):
            running = False  

    player.draw()
    for bullet in bullets:
        bullet.draw()
    for asteroid in asteroids:
        asteroid.draw()

    pygame.display.flip()

pygame.quit()
