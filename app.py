import pgzrun
from random import randint

WIDTH = 700
HEIGHT = 500

# world options
bg = Actor('background')
gravity = 5
ground = HEIGHT - 37

# PLAYER CONFIGS
player = Actor('player_idle')
player.x = WIDTH/2
player.y = HEIGHT - player.height/2 - 5
player.runing = False
player.speed = 2
player.max_stamin = 50
player.stamin = 0
player.is_jumping = False
player.jump_timer = 0
player.jump_height = 70
player.jump_force = 10
player.hitbox_w = 30
player.hitbox_h = 60

# BOSS CONFIGS
boss = Actor('boss')
boss.x = WIDTH/2
boss.steps = .5
boss.atack_rate = 500
boss.clock = 0

# BOSS SHOOT CONFIGS
missile = Actor('missile_0')
missile.x = 0
missile.y = boss.y
missile.speed = 1
missile.images = ['missile_0', 'missile_1']
missile.fps = 10
missile.is_fired = False

def get_hitbox(actor):
    return Rect(
        actor.x - actor.hitbox_w/2,   # deslocamento horizontal da posição
        actor.y - 25,                 # deslocamento vertical da posição
        actor.hitbox_w, actor.hitbox_h          # largura e altura da hitbox personalizada
    )

def on_key_down(key):
    if key == keys.LSHIFT and player.stamin == player.max_stamin and (player.runing == False):
        player.runing = True
        player.speed = 4


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
    if player.y < ground:
        player.y += gravity
    
    # set player in ground
    if player.y > ground:
        player.y = ground

    ### PLAYER ACTIONS ----------------------------------------
    # left and right
    if (keyboard.right or keyboard.d) and player.x < WIDTH - 25:
        player.x += player.speed
    if (keyboard.left  or keyboard.a) and player.x > 25:
        player.x -= player.speed
 
    # check conditions for jump
    if keyboard.space:
        if player.y == ground and player.jump_timer > 20:
            player.is_jumping = True
        if player.is_jumping:
            player.y -= player.jump_force

    # add one tick for timer    
    player.jump_timer += 1

    # change jump variable when reach max height
    if (player.y <= ground - player.jump_height):
        player.is_jumping = False
        player.jump_timer = 0

    # charge stamin
    if player.stamin < player.max_stamin and (player.runing == False):
        player.stamin += 0.5
        print(player.stamin)

    if player.stamin <= 0 and on_key_up(keys.LSHIFT):
        player.runing = False
        player.speed = 2

    if player.runing:
        player.stamin -= 1

    # verify colission player missile
    if get_hitbox(player).colliderect(missile._rect):
        print('atingido')
   

    ### BOSS ACTIONS ----------------------------------------
    boss.clock += 1

    # left and right
    boss.x += boss.steps
    if boss.x >= WIDTH - 140 or boss.x <= 140:
        boss.steps = boss.steps * -1
    
    # boss atacks
    if boss.clock == boss.atack_rate:
        missile.x = boss.x
        missile.y = boss.y
        missile.is_fired = True
        boss.clock = 0

    # MISSILE ACTIONS ----------------------------------------
    if missile.y > HEIGHT:
        missile.y = -20
        missile.x = 0
        missile.is_fired = False

    if missile.is_fired:
        missile.y += missile.speed
        if missile.x > player.x:
            missile.x -= 1
        elif missile.x < player.x:
            missile.x += 1

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
    boss.draw()
    missile.draw()
    
    hitbox = get_hitbox(player)
    screen.draw.rect(hitbox, "red")