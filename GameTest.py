import pygame
import math
import time
import json

pygame.init()

WIDTH, HEIGHT = 1440, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GTA VI 2")
pygame.mouse.set_visible(True)
pygame.event.set_grab(True)
font = pygame.font.SysFont("Times", 15, bold=True)
with open("data.json", "r") as file:
    wmap = json.load(file)
world_map = wmap
with open("spawn.json", "r") as file:
    sp = json.load(file)
spawn = sp
player_x, player_y = spawn
with open("espawn.json", "r") as file:
    esp = json.load(file)
espawn = esp
enemy_x, enemy_y = espawn

player_angle = 0
FOV = math.pi / 3
num_rays = 160
max_depth = 15
clock = pygame.time.Clock()

def draw_enemy():
        dx = enemy_x - player_x
        dy = enemy_y - player_y
        distt = math.sqrt(dx**2 + dy**2)
        enemy_angle = math.atan2(dy, dx)
        relative_angle = enemy_angle - player_angle
        print(distt, relative_angle)
        if abs(relative_angle) < FOV / 2:
            print("ENNEMI VISIBLE")
        else:
            print("ENNEMI HORS CHAMP")

def respawning():
    font = pygame.font.SysFont("Times", 15, bold=True)
    bouton_war = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
    win.fill((21,10,210))
    time.sleep(2)
    res = font.render("RESPAWNING", True, (255, 255, 255))
    win.blit(res, (bouton_war.x + 100, bouton_war.y + 15))
    time.sleep(2)

def collisions(x, y):
    nx = int(x)
    ny = int(y)
    if world_map[nx][ny] == 1:
        return False
    else:
        return True

def cast_rays():
    global player_x, player_y
    start_angle = player_angle - FOV / 2
    for ray in range(num_rays):
        ray_angle = start_angle + (ray / num_rays) * FOV
        dist = 0
        hit = False
        
        while not hit and dist < max_depth:
            dist += 0.05
            x = int(player_x + dist * math.cos(ray_angle))
            y = int(player_y + dist * math.sin(ray_angle))
            try:
                if world_map[x][y] == 1:
                    hit = True
            except IndexError:
                player_x, player_y = spawn
                respawning()
                break

        h = 200 / (dist + 0.0001)
        c = 125 / (1 + dist * dist * 0.1)
        color = (c, c, c)
        pygame.draw.rect(win, color, (ray * (WIDTH/num_rays), HEIGHT/2 - h/2, WIDTH/num_rays, h))



def draw_crosshair():
    cx, cy = WIDTH//2, HEIGHT//2
    pygame.draw.line(win, (255,255,255), (cx-10, cy), (cx+10, cy), 2)
    pygame.draw.line(win, (255,255,255), (cx, cy-10), (cx, cy+10), 2)
    
def show_menu(events):
    global game_state
    global press
    global game_over
    global keys
    game_state = "menu"
    pygame.mouse.set_visible(True)
    win.fill((255,255,255))
    
    
    bouton_jeu = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
    bouton_opt = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 10, 200, 50)
    bouton_war = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)

    pygame.draw.rect(win, (0, 0, 0), bouton_jeu)
    pygame.draw.rect(win, (0, 0, 0), bouton_opt)
    text_jouer = font.render("Jouer", True, (255, 255, 255))
    text_warning = font.render("Salut !", True, (0, 0, 0))
    text_options = font.render("Options", True, (255, 255, 255))
    win.blit(text_jouer, (bouton_jeu.x + 70, bouton_jeu.y + 15))
    win.blit(text_options, (bouton_opt.x + 60, bouton_opt.y + 15))
    win.blit(text_warning, (bouton_war.x + 100, bouton_war.y + 15))


    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()
            if bouton_jeu.collidepoint(pos):
                game_state = "jeu"
            elif bouton_opt.collidepoint(pos):
                game_state = "options"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_over = True 


def show_options(events):
    global game_state
    global pose
    global keys
    global win
    global WIDTH
    global HEIGHT
    game_state = "options"
    win.fill((255,255,255))
    fullscrn_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
    pygame.draw.rect(win, (0, 0, 0), fullscrn_btn)
    text_fullscrn = font.render("Plein ecran", True, (255, 255, 255))
    win.blit(text_fullscrn, (fullscrn_btn.x + 70, fullscrn_btn.y + 15))

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos() 
            if fullscrn_btn.collidepoint(pos):
                if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
                    win = pygame.display.set_mode((WIDTH, HEIGHT))
                else:
                    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    pygame.event.set_grab(True)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                game_state = "menu"
    pygame.display.update()

def play_game(events):
    global game_state
    global game_over
    global keys
    global player_angle
    global player_x
    global player_y
    game_state = "jeu"
    pygame.mouse.set_visible(False)

    for e in events:
        if e.type == pygame.QUIT:
            game_over = True
            return
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                game_state = "menu"
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:    
            newx = player_x + math.cos(player_angle) * 0.05
            newy = player_y + math.sin(player_angle) * 0.05
            check = collisions(newx, newy)
            if check == True:
                player_x += math.cos(player_angle) * 0.05
                player_y += math.sin(player_angle) * 0.05
            else:
                pass
    if keys[pygame.K_s]:
            newx = player_x - math.cos(player_angle) * 0.05
            newy = player_y - math.sin(player_angle) * 0.05
            check = collisions(newx, newy)
            if check == True:
                player_x -= math.cos(player_angle) * 0.05
                player_y -= math.sin(player_angle) * 0.05
            else:
                pass
    if keys[pygame.K_q]:
            newx = player_x + math.sin(player_angle) * 0.025
            newy = player_y - math.cos(player_angle) * 0.025
            check = collisions(newx, newy)
            if check == True:
                player_x += math.sin(player_angle) * 0.025
                player_y -= math.cos(player_angle) * 0.025
            else:
                pass
    if keys[pygame.K_d]:  
            newx = player_x - math.sin(player_angle) * 0.025
            newy = player_y + math.cos(player_angle) * 0.025
            check = collisions(newx, newy)
            if check == True:
                player_x -= math.sin(player_angle) * 0.025
                player_y += math.cos(player_angle) * 0.025
            else:
                pass
    

    # Mouse movement
    dx, dy = pygame.mouse.get_rel()
    player_angle += dx * 0.002

    win.fill((0,0,0))
    cast_rays()
    draw_crosshair()
    draw_enemy()
    pygame.display.flip()
    clock.tick(60)

game_state = "menu"
game_over = False
while not game_over:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            game_over = True
    if game_state == "menu":
        show_menu(events)
    elif game_state == "options":
        show_options(events)
    elif game_state == "jeu":
        play_game(events)
pygame.quit()
quit()