import pgzrun
from random import randint

WIDTH = 500
HEIGHT = 400

# world options
bg = Actor('background')
gravity = 5
ground = 363

# PLAYER CONFIGS
player_walk_Frames = ['player_walk_0','player_walk_1', 'player_walk_2', 'player_walk_3']
player = Actor('player_idle')
player.x = WIDTH/2
player.y = HEIGHT - player.height/2 - 5
player.is_jumping = False
player.jump_height = 50
player.jump_force = 8
player.frame_index = 0
player.frame_timer = 0
player.frame_speed = 0.15

# BOSS CONFIGS
boss = Actor('boss')
boss.x = WIDTH/2
boss.steps = .5
boss.atack_rate = 500
boss.clock = 0

# BOSS SHOOT CONFIGS
missil = Actor('missil_0')
missil.x = 0
missil.y = boss.y
missil.speed = 1
missil.images = ['missil_0', 'missil_1']
missil.fps = 10
missil.is_fired = False



def update():
    if keyboard.escape:
        # menu options
        ### TO DO ###
        exit()

    ### WORLD ACTIONS
    # gravity actions
    if player.y < ground:
        player.y += gravity
    
    # set player in ground
    if player.y > ground:
        player.y = ground

    ### PLAYER ACTIONS
    # left and right
    if (keyboard.right or keyboard.d) and player.x < 475:
        player.x += 2
        player.frame_timer += player.frame_speed
        if player.frame_timer >= 1:
            player.frame_timer = 0
            player.frame_index = (player.frame_index + 1) % len(player_walk_Frames)  # próximo frame
            player.image = player_walk_Frames[player.frame_index]            # troca sprite

    if (keyboard.left  or keyboard.a) and player.x > 25:
        player.x -= 2
 
    # check conditions for jump
    if keyboard.space:
        if player.y == ground:
            player.is_jumping = True
        if player.is_jumping:
            player.y -= player.jump_force
    
    # change jump variable when reach max height     
    if player.y <= ground - player.jump_height:
        player.is_jumping = False
   

    ### BOSS ACTIONS
    boss.clock += 1

    # left and right
    boss.x += boss.steps
    if boss.x >= 360 or boss.x <= 140:
        boss.steps = boss.steps * -1
    
    # boss atacks
    if boss.clock == boss.atack_rate:
        missil.x = boss.x
        missil.y = boss.y
        missil.is_fired = True
        boss.clock = 0
        print('atacou')

    # MISSIL ACTIONS
    if missil.y > HEIGHT:
        missil.y = 20
        missil.is_fired = False
        print('missil resetado')

    if missil.is_fired:
        missil.y += missil.speed
        if missil.x > player.x:
            missil.x -= 1
        elif missil.x < player.x:
            missil.x += 1
        print('em trajeto')

    """rand = randint(0, 50)
    if rand == 20:
        missil.x = randint(50, 450)
        print('atacou')

def on_mouse_down(pos, button):
    missil.x = boss.x
    print("Mouse button", button, "clicked at", pos)
    print(missil._rect)"""


### DRAW SPRITES
def draw():
    bg.draw()
    player.draw()
    boss.draw()
    missil.draw()