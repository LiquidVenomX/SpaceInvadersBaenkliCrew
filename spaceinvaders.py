import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Fenstergröß  e
WIDTH, HEIGHT = 800, 600

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Spieler
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5

# Schuss
bullet_size = 5
bullet_speed = 7
bullets = []

# Gegner (Parkbank Animation)
class Parkbench(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.images = [pygame.image.load(image)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_speed = 10
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

# Gruppen für animierte Objekte, Gegner und Schüsse der Gegner
animated_objects = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Geschwindigkeit der Spieler, Gegner und Schüsse der Gegner
player_speed = 5
enemy_speed = 2
enemy_bullet_speed = 5

# Funktion zum Erstellen eines neuen Gegners
def create_enemy():
    return Parkbench(random.randint(0, WIDTH - player_size), 0, 'bench2.png')

# Score und Leben
score = 0
lives = 5
continue_count = 3

# Initialisierung des Fensters
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BänkliCrew-SpaceInvaders2024")  # Geänderter Titel

# Schriftart für den Text
font = pygame.font.Font(None, 36)

# Funktion für die Anzeige des Hauptmenüs
def show_menu():
    menu_text = font.render("BänkliCrew-SpaceInvaders2024", True, WHITE)  # Geänderter Titel
    start_text = font.render("Drücke 'S' um zu starten", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))

# Funktion für die Anzeige des Game Over-Bildschirms
def show_game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    continue_text = font.render(f"Continue: {continue_count}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 70))

# Spieler-Animation
player_animation = Parkbench(player_x, player_y, 'bench1.png')
animated_objects.add(player_animation)

# Schleife für das Spiel
running = True
in_menu = True
game_over = False
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if in_menu and event.key == pygame.K_s:
                in_menu = False
            elif not in_menu and not game_over and event.key == pygame.K_SPACE:
                bullets.append([player_animation.rect.x + player_size // 2, player_animation.rect.y])

    if in_menu:
        show_menu()
    elif game_over:
        show_game_over()
        continue_text = font.render(f"Drücke 'C' um fortzusetzen", True, WHITE)
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 130))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_c] and continue_count > 0:
            # Fortsetzen
            game_over = False
            continue_count -= 1
            lives = 5
            score = 0
    else:
        keys = pygame.key.get_pressed()
        player_animation.rect.x -= keys[pygame.K_LEFT] * player_speed
        player_animation.rect.x += keys[pygame.K_RIGHT] * player_speed

        # Begrenzung der Spielerbewegung
        player_animation.rect.x = max(0, min(WIDTH - player_size, player_animation.rect.x))

        # Hinzufügen neuer Gegner
        if random.randint(0, 100) < 5:
            new_enemy = create_enemy()
            enemies.add(new_enemy)

        # Kollisionserkennung für Schüsse und Gegner
        for bullet in bullets:
            for enemy in enemies:
                if (
                    bullet[0] > enemy.rect.x
                    and bullet[0] < enemy.rect.x + enemy.rect.width
                    and bullet[1] > enemy.rect.y
                    and bullet[1] < enemy.rect.y + enemy.rect.height
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10

        # Kollisionserkennung für Spieler und Gegner
        for enemy in enemies:
            if player_animation.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                lives -= 1

        # Überprüfen, ob Leben aufgebraucht sind
        if lives <= 0:
            game_over = True

        # Bewegung der Schüsse
        for bullet in bullets:
            bullet[1] -= bullet_speed
            pygame.draw.circle(screen, RED, (bullet[0], bullet[1]), bullet_size)

        # Entfernen außerhalb des Bildschirms befindlicher Schüsse
        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        # Bewegung der Gegner
        for enemy in enemies:
            enemy.rect.y += enemy_speed
            enemy.update()
            screen.blit(enemy.image, enemy.rect)

        # Anzeige von Leben und Score
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Bewegung der animierten Objekte
    for animated_object in animated_objects:
        animated_object.update()
        screen.blit(animated_object.image, animated_object.rect)

    pygame.display.flip()
    clock.tick(60)

# Beenden von Pygame
pygame.quit()   