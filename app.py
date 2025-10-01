from os import environ
import pgzrun
from random import randint

WIDTH = 700
HEIGHT = 500
# Diz ao SDL para centralizar a janela
environ['SDL_VIDEO_CENTERED'] = '1'

# world options
bg = Actor('background')
gravity = 5
ground = HEIGHT - 16

# PLAYER CONFIGS
player = Actor('player_idle')
player.x = WIDTH/2
player.y = HEIGHT - player.height * 2
player.runing = False
player.speed = 2
player.max_stamin = 50
player.stamin = 0
player.is_jumping = False
player.jump_timer = 0
player.jump_height = 90
player.jump_force = 10
player.hitbox = {'desloc_x' : 15, 'desloc_y': 26, 'width': 30, 'height': 55}

# BULLET CONFIGS
bullets = []

# BOSS CONFIGS
boss = Actor('boss')
boss.x = WIDTH/2
boss.max_life = 500
boss.life = boss.max_life
boss.steps = .5
boss.atack_rate = 500
boss.clock = 0
boss.right_eye = {'desloc_x' : -30, 'desloc_y': -5, 'width': 40, 'height': 15}
boss.left_eye = {'desloc_x' : 68, 'desloc_y': -5, 'width': 40, 'height': 15}

# BOSS SHOOT CONFIGS
missile = Actor('missile_0')
missile.x = 0
missile.y = boss.y
missile.speed = 1
missile.frames = ['missile_0', 'missile_1', 'missile_2', 'missile_1',]
missile.frame_index = 0
missile.fps = 0.1
missile.frame_timer = 40
missile.is_fired = False
missile.hitbox = {'desloc_x' : 6.5, 'desloc_y': -3, 'width': 13, 'height': 18}

# EXPLOSION
explosion = Actor('explosion_0')
explosion.x = 0
explosion.y = 0
explosion.explode = False
explosion.timer = 40
explosion.frame_timer = 20
explosion.fps = 0.1
explosion.frame_index = 0
explosion.frames = ['explosion_0', 'explosion_1', 'explosion_2', 'explosion_3']

# get functions
'''def get_hitbox(actor):
    return Rect(
        actor.x - actor.desloc_x,   # deslocamento horizontal da posição
        actor.y - actor.desloc_y,                 # deslocamento vertical da posição
        actor.hitbox_w, actor.hitbox_h          # largura e altura da hitbox personalizada
    )'''

def get_hitbox(actor, hitbox):
    return Rect(
        actor.x - hitbox['desloc_x'],   # deslocamento horizontal da posição
        actor.y - hitbox['desloc_y'],                 # deslocamento vertical da posição
        hitbox['width'], hitbox['height']         # largura e altura da hitbox personalizada
    )

def get_base(actor):
    return actor.y + actor.height / 2

# execute animation
def animate(actor):
    actor.frame_timer += actor.fps
    if actor.frame_timer >= 1:
        actor.frame_timer = 0
        actor.frame_index = (actor.frame_index + 1) % len(actor.frames)
        return actor.frames[actor.frame_index]
    else:
        return actor.frames[actor.frame_index]

# when key is pressed
def on_key_down(key):
    if key == keys.LSHIFT and player.stamin == player.max_stamin and (player.runing == False) and (keyboard.left  or keyboard.a or keyboard.right or keyboard.d):
        player.runing = True
        player.speed = 4

    if (keyboard.up or keyboard.w):
        bullet = Actor('bullet')
        bullet.x = player.x + 15
        bullet.y = player.y - player.height/2
        bullet.damage = 10
        bullet.is_fired = True
        bullets.append(bullet)


# when key is released
def on_key_up(key):
    if key == keys.LSHIFT:
        player.speed = 2
        player.runing = False


def update():
    if keyboard.escape:
        # menu options
        ### TO DO ###
        exit()

    ### WORLD ACTIONS ----------------------------------------
    # gravity actions
    if get_base(player) < ground:
        player.y += gravity
    
    # set player in ground
    if get_base(player) > ground:
        player.y = ground - player.height / 2

    ### PLAYER ACTIONS ----------------------------------------
    # left and right
    if (keyboard.right or keyboard.d) and player.x < WIDTH - 25:
        player.x += player.speed
    if (keyboard.left  or keyboard.a) and player.x > 25:
        player.x -= player.speed
 
    # check conditions for jump
    if keyboard.space:
        if get_base(player) == ground and player.jump_timer > 20:
            player.is_jumping = True
            player.stamin -= player.max_stamin / 2
        if player.is_jumping:
            player.y -= player.jump_force

    # add one tick for timer
    player.jump_timer += 1

    # change jump variable when reach max height
    if (get_base(player) <= ground - player.jump_height):
        player.is_jumping = False
        player.jump_timer = 0

    # charge stamin
    if player.stamin < player.max_stamin and (player.runing == False):
        player.stamin += 0.5

    # stop player run
    if player.stamin <= 0 and on_key_up(keys.LSHIFT):
        player.runing = False
        player.speed = 2

    # decrease stamina when runing
    if player.runing:
        player.stamin -= 1

    # verify colission player -> missile
    if get_hitbox(player, player.hitbox).colliderect(get_hitbox(missile, missile.hitbox)):
        print('atingido')
    
    # set bullet moviment
    for bullet in bullets:
        bullet.y -= 3

        if bullet.colliderect(get_hitbox(boss, boss.right_eye)):
            if bullet.is_fired: boss.life -= 5
            bullet.is_fired = False

    # remove bullets when getout screen
    bullets[:] = [b for b in bullets if (b.y > 100 or b.is_fired==False)]

    ### BOSS ACTIONS ----------------------------------------
    boss.clock += 1

    # left and right
    boss.x += boss.steps
    if boss.x >= WIDTH - 140 or boss.x <= 140:
        boss.steps = boss.steps * -1
    
    # boss atack
    if boss.clock == boss.atack_rate:
        missile.x = boss.x
        missile.y = boss.y
        missile.is_fired = True
        boss.clock = 0

    # MISSILE ACTIONS ----------------------------------------
    # 
    if get_base(get_hitbox(missile, missile.hitbox)) >= ground:
        explosion.x = missile.x
        explosion.y = missile.y - 15
        explosion.explode = True
        missile.y = -20
        missile.x = 0
        missile.is_fired = False

    # fired
    if missile.is_fired:
        missile.y += missile.speed
        if missile.x > player.x:
            missile.x -= 1
        elif missile.x < player.x:
            missile.x += 1
        # avança o contador de tempo
        missile.image = animate(missile)

    # EXPLOSION ACTIONS
    if explosion.explode and explosion.timer > 0:
        explosion.timer -= 1
        explosion.image = animate(explosion)
    
    if explosion.timer <= 0:
        explosion.timer = 30
        explosion.explode = False

""" TEST 
    rand = randint(0, 50)
    if rand == 20:
        missile.x = randint(50, 450)
        print('atacou')

def on_mouse_down(pos, button):
    missile.x = boss.x
    print("Mouse button", button, "clicked at", pos)
    print(missile._rect)
"""


### DRAW SPRITES ----------------------------------------
def draw():
    bg.draw()

    player.draw()
    screen.draw.rect(get_hitbox(player, player.hitbox), 'blue') # FOR DEBUG
    
    boss.draw()
    screen.draw.filled_rect(Rect((boss.x - boss.max_life/4, 50), (boss.life / 2, 5)), (200, 0, 0))
    screen.draw.rect(Rect((boss.x - boss.max_life/4, 50), (boss.max_life/2, 5)), (0, 0, 0))
    screen.draw.text(str(boss.life), (boss.x - boss.max_life/4, 60), fontsize=40, color="white")

    # boss eyes
    screen.draw.rect(get_hitbox(boss, boss.right_eye), 'blue') # FOR DEBUG
    screen.draw.rect(get_hitbox(boss, boss.left_eye), 'blue') # FOR DEBUG
    
    # bullet
    if len(bullets) > 0:
        for bullet in bullets:
            if bullet.is_fired:
                bullet.draw()
                screen.draw.rect(bullet._rect, 'red')

    # missile
    if missile.is_fired:
        missile.draw()
        screen.draw.rect(get_hitbox(missile, missile.hitbox), 'blue') # FOR DEBUG

    # explosion
    if explosion.explode:
        explosion.draw()

    #--------------------
    # exibition of stamin bar           X                                Y                            W         H        COLOR
    screen.draw.filled_rect(Rect((player.x - player.width / 4, player.y - player.height + 20), (player.stamin/2, 5)), (200, 150, 0))
    screen.draw.rect(Rect((player.x - player.width / 4, player.y - player.height + 20), (player.max_stamin/2, 5)), (200, 150, 0))
    #------------------------------
    
    # ground line FOR DEBUG
    screen.draw.rect(Rect((0, ground), (WIDTH, 2)), ('blue'))