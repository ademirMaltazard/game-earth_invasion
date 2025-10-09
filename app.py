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
cutscene = False

# PLAYER CONFIGS
player = Actor('player_r_idle_0')
player.x = 50
player.y = HEIGHT - player.height * 2
player.running = False
player.speed = 2
player.max_stamin = 50
player.stamin = 0
player.is_firing = False
player.is_jumping = False
player.jump_timer = 0
player.jump_height = 90
player.jump_force = 10
player.direction = 'right'
player.hitbox = {'desloc_x' : 15, 'desloc_y': 26, 'width': 30, 'height': 55}
player.anim_r_idle = {'play': True,'repeat': True, 'index': -1, 'fps': 1, 'timer': 0, 'frames': [ 'player_r_idle_1','player_r_idle_0', 'player_r_idle_0', 'player_r_idle_1', 'player_r_idle_2', 'player_r_idle_2']}
player.anim_l_idle = {'play': True,'repeat': True, 'index': -1, 'fps': 1, 'timer': 0, 'frames': [ 'player_l_idle_1','player_l_idle_0', 'player_l_idle_0', 'player_l_idle_1', 'player_l_idle_2', 'player_l_idle_2']}
player.anim_r_walk = {'play': True,'repeat': True, 'index': -1, 'fps': 1, 'timer': 0, 'frames': ['r_walk_0', 'r_walk_1', 'r_walk_2', 'r_walk_3', 'r_walk_4', 'r_walk_5', 'r_walk_6', 'r_walk_7']}
player.anim_r_firing = {'play': True,'repeat': True, 'index': -1, 'fps': 1, 'timer': 0, 'frames': ['r_firing_0', 'r_firing_1', 'r_firing_2', 'r_firing_3', 'r_firing_4', 'r_firing_5', 'r_firing_6', 'r_firing_7']}
player.anim_l_walk = {'play': True,'repeat': True, 'index': -1, 'fps': 1, 'timer': 0, 'frames': ['l_walk_0', 'l_walk_1', 'l_walk_2', 'l_walk_3', 'l_walk_4', 'l_walk_5', 'l_walk_6', 'l_walk_7']}
player.anim_l_firing = {'play': True,'repeat': True, 'index': -1, 'fps': 1, 'timer': 0, 'frames': ['l_firing_0', 'l_firing_1', 'l_firing_2', 'l_firing_3', 'l_firing_4', 'l_firing_5', 'l_firing_6', 'l_firing_7']}

# GUN CONFIGS
gun = Actor('gun')
gun.x = WIDTH - 80
gun.y = HEIGHT - 30
gun.bullets = []
gun.bullet_timer = 0
gun.reloading = False
gun.reload_time = 100
gun.max_ammo = 30
gun.ammo = 30

# BOSS CONFIGS
boss = Actor('boss')
boss.x = WIDTH/2
boss.y = -50
boss.alive = False
boss.max_life = 500
boss.life = boss.max_life
boss.steps = .5
boss.actual_step = 0
boss.missile_atk = False
boss.r_tentacle_atk = False
boss.l_tentacle_atk = False
boss.dual_tentacle_atk = False
boss.slime_blast_atk = False
boss.atack_rate = 350
boss.clock = 0
boss.tentacle_atk_timer = 0
boss.body = {'desloc_x' : 100, 'desloc_y': 85, 'width': 200, 'height': 100}
boss.right_eye = {'desloc_x' : -30, 'desloc_y': -5, 'width': 40, 'height': 15}
boss.left_eye = {'desloc_x' : 68, 'desloc_y': -5, 'width': 40, 'height': 15}
boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 60}
boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 60}
boss.mouth = {'desloc_x' : 20, 'desloc_y': -10, 'width': 40, 'height': 15}

# BOSS SHOOT CONFIGS
missile = Actor('missile_0')
missile.x = 0
missile.y = boss.y
missile.speed = 1
missile.is_fired = False
missile.hitbox = {'desloc_x' : 6.5, 'desloc_y': -3, 'width': 13, 'height': 18}
missile.anim = {'play': True, 'repeat': True, 'index': 0, 'fps': 1, 'timer': 0, 'frames': ['missile_0', 'missile_1', 'missile_2', 'missile_1']}

# EXPLOSION
explosion = Actor('explosion_0')
explosion.x = 0
explosion.y = 0
explosion.explode = False
explosion.timer = 40
explosion.anim = {'play': True, 'repeat': False, 'index': -1, 'fps': 2, 'timer': 0, 'frames': ['explosion_0', 'explosion_1', 'explosion_2', 'explosion_3', 'explosion_4', 'explosion_5', 'explosion_6','explosion_7', 'explosion_8', 'explosion_9', 'explosion_10']}


# execute animation
def animate(anim):
    if anim['play'] == True:
        anim['timer'] += anim['fps']
        if anim['timer'] % 10 == 0:
            anim['timer'] = 0
            anim['index'] = (anim['index'] + 1) % len(anim['frames'])
            if anim['index'] == len(anim['frames']) - 1 and anim['repeat'] == False:
                anim['play'] = False
            return anim['frames'][anim['index']]
        else: 
            return anim['frames'][anim['index']]
    else:
        return anim['frames'][0]
    
# get functions

def get_hitbox(actor, hitbox):
    return Rect(
        actor.x - hitbox['desloc_x'],   # deslocamento horizontal da posição
        actor.y - hitbox['desloc_y'],                 # deslocamento vertical da posição
        hitbox['width'], hitbox['height']         # largura e altura da hitbox personalizada
    )

def get_base(actor):
    return actor.y + actor.height / 2

def get_idle():
    if player.direction == 'left':
        return animate(player.anim_l_idle)
    elif player.direction == 'right':
        return animate(player.anim_r_idle)

# when key is pressed
def on_key_down(key):
    if key == keys.LSHIFT and player.stamin == player.max_stamin and (player.running == False) and (keyboard.left  or keyboard.a or keyboard.right or keyboard.d) and (cutscene == False):
        player.running = True
        player.speed = 4

    if key == keys.R and (cutscene == False):
        gun.reloading = True


# when key is released
def on_key_up(key):
    if key == keys.LSHIFT:
        player.speed = 2
        player.running = False
    
    # set player direction
    if (key == keys.LEFT or key == keys.A) and cutscene == False:
        player.direction = 'left'
    if (key == keys.RIGHT or key == keys.D) and cutscene == False:
        player.direction = 'right'

def on_mouse_down(button):
    if button == 1 and keyboard.w:
        player.is_firing = True

def on_mouse_up(button):
    if button == 1:
        player.is_firing = False


def update():
    global cutscene

    if keyboard.escape:
        # menu options
        ### TO DO ###
        exit()

    ### WORLD ACTIONS ----------------------------------------
    # gravity actions
    if get_base(player) < ground:
        player.y += gravity

    if get_base(player) == ground:
        player.image = get_idle()
    
    # set player in ground
    if get_base(player) > ground:
        print('down: ', ground, '---', (player.y + player.height / 2), '---', player.y, '---', player.height)
        player.y = ground - player.height / 2

    ### PLAYER ACTIONS ----------------------------------------
    if cutscene == False:
        # left and right
        if (keyboard.right or keyboard.d) and player.x < WIDTH - 25:
            player.anim_r_walk['repeat'] = True
            player.image = animate(player.anim_r_walk)
            player.x += player.speed
        if (keyboard.left  or keyboard.a) and player.x > 25:
            player.anim_l_walk['repeat'] = True
            player.image = animate(player.anim_l_walk)
            player.x -= player.speed

        # aim
        if keyboard.w or keyboard.up:
            if keyboard.left or keyboard.a:
                player.image = animate(player.anim_l_firing)
            elif keyboard.right or keyboard.d:
                player.image = animate(player.anim_r_firing)
    
        # check conditions for jump
        if keyboard.space:
            if get_base(player) == ground and player.jump_timer > 20 and player.stamin > player.max_stamin / 2:
                player.is_jumping = True
                player.stamin -= player.max_stamin / 3
            if player.is_jumping:
                player.y -= player.jump_force


        # add one tick for timer
        player.jump_timer += 1

    # change jump variable when reach max height
    if (get_base(player) <= ground - player.jump_height):
        player.is_jumping = False
        player.jump_timer = 0

    # charge stamin
    if player.stamin < player.max_stamin and (player.running == False):
        player.stamin += 0.5

    # stop player run
    if player.stamin <= 0 and on_key_up(keys.LSHIFT):
        player.running = False
        player.speed = 2

    # decrease stamina when running
    if player.running:
        player.stamin -= 1

    # verify colission player -> missile
    if get_hitbox(player, player.hitbox).colliderect(get_hitbox(missile, missile.hitbox)) or get_hitbox(player, player.hitbox).colliderect(explosion._rect):
        print('atingido')

    
    # acress bullet timer
    gun.bullet_timer += 1

    # create a new bullet
    if player.is_firing and gun.bullet_timer > 20 and gun.ammo > 0 and gun.reloading == False:
        print('bala')
        bullet = Actor('bullet')
        if keyboard.left or keyboard.a:
            bullet.x = player.x + 15
        elif keyboard.right or keyboard.d:
            bullet.x = player.x - 15
        bullet.y = player.y - player.height/2
        bullet.damage = 5
        bullet.is_fired = True
        gun.bullets.append(bullet)
        gun.bullet_timer = 0
        gun.ammo -= 1

    # reload ammo
    if gun.reloading:
        gun.reload_time -= 1
        if gun.reload_time <= 0:
            gun.ammo = gun.max_ammo
            gun.reload_time = 100
            gun.reloading = False
            

    # bullet moviment
    for bullet in gun.bullets:
        bullet.y -= 3

        if bullet.y <= 100:
            bullet.is_fired = False

        # verify collision bullet -> right eye 
        if bullet.colliderect(get_hitbox(boss, boss.right_eye)):
            if bullet.is_fired: boss.life -= bullet.damage
            bullet.is_fired = False
        
        # verify collision bullet -> left eye 
        if bullet.colliderect(get_hitbox(boss, boss.left_eye)):
            if bullet.is_fired: boss.life -= bullet.damage
            bullet.is_fired = False

        if bullet.colliderect(get_hitbox(boss, boss.mouth)):
            if bullet.is_fired: boss.life -= bullet.damage * 2
            bullet.is_fired = False

        if bullet.colliderect(get_hitbox(boss, boss.body)):
            bullet.is_fired = False
        
        # verify collision bullet -> right tentacle 
        if bullet.colliderect(get_hitbox(boss, boss.right_tentacle)):
            bullet.is_fired = False

        # verify collision bullet -> left tentacle 
        if bullet.colliderect(get_hitbox(boss, boss.left_tentacle)):
            bullet.is_fired = False
        


    # remove bullets when getout screen
    gun.bullets[:] = [b for b in gun.bullets if b.is_fired]

    ### BOSS ACTIONS ----------------------------------------
    if boss.alive == False and player.x > WIDTH/3 and boss.y < 140:
        cutscene = True
        boss.y += 1
    
    if boss.y == 140:
        boss.alive = True

    if boss.alive:
        cutscene = False
        boss.clock += 1

        # left and right
        boss.x += boss.steps
        if boss.x >= WIDTH - 140 or boss.x <= 140:
            boss.steps = boss.steps * -1
        
        # boss atack
        if boss.clock == boss.atack_rate:
            attack = randint(0,3)
            boss.actual_steps = boss.steps

            if attack == 0:
                boss.missile_atk = True
                print('ataque missil')
            if attack == 1:
                boss.r_tentacle_atk = True
                print('ataque tentaculo direito')
            if attack == 2:
                boss.l_tentacle_atk = True
                print('ataque tentaculo esquerdo')
            if attack == 3:
                boss.dual_tentacle_atk = True
                print('ataque dos dois tentaculos')


        # MISSILE ACTIONS ----------------------------------------
        # attacking with Missil
        if boss.missile_atk:
            missile.x = boss.x
            missile.y = boss.y
            missile.is_fired = True
            boss.clock = 0
            boss.missile_atk = False

        # colision MISSILE --> GROUND
        if get_base(get_hitbox(missile, missile.hitbox)) >= ground:
            explosion.x = missile.x
            explosion.y = ground - explosion.height / 2
            explosion.explode = True
            explosion.anim['play'] = True
            missile.y = -20
            missile.x = 0
            missile.is_fired = False

        # missile moviment
        if missile.is_fired:
            missile.y += missile.speed
            if missile.x > player.x:
                missile.x -= 1
            elif missile.x < player.x:
                missile.x += 1
            missile.image = animate(missile.anim)

        # EXPLOSION ACTIONS ------------------------------------------------------
        if explosion.explode and explosion.anim['play']:
            # keep the base of image on ground, regardless of the size of the image
            explosion.y = ground - explosion.height / 2
            explosion.image = animate(explosion.anim)
        
        if explosion.anim['play'] == False:
            explosion.x = 0
            explosion.y = -50
            explosion.explode = False

        # TENTACLE ACTIONS ----------------------------------------
        if boss.r_tentacle_atk:
            boss.tentacle_atk_timer += 1
            boss.steps = 0
            if boss.tentacle_atk_timer < 30:
                boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80}
                get_hitbox(boss, boss.right_tentacle)
            elif boss.tentacle_atk_timer < 70:
                boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 300}
                get_hitbox(boss, boss.right_tentacle)
            elif boss.tentacle_atk_timer < 100:
                boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80}
                get_hitbox(boss, boss.right_tentacle)
            else:
                boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 60}
                get_hitbox(boss, boss.right_tentacle)
                boss.tentacle_atk_timer = 0
                boss.r_tentacle_atk = False
                boss.steps = boss.actual_steps
                boss.clock = 0

        if boss.l_tentacle_atk:
            boss.tentacle_atk_timer += 1
            boss.steps = 0
            if boss.tentacle_atk_timer < 30:
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                get_hitbox(boss, boss.left_tentacle)
            elif boss.tentacle_atk_timer < 70:
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 300}
                get_hitbox(boss, boss.left_tentacle)
            elif boss.tentacle_atk_timer < 100:
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                get_hitbox(boss, boss.left_tentacle)
            else:
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 60}
                get_hitbox(boss, boss.left_tentacle)
                boss.tentacle_atk_timer = 0
                boss.l_tentacle_atk = False
                boss.steps = boss.actual_steps
                boss.clock = 0
        
        if boss.dual_tentacle_atk:
            boss.tentacle_atk_timer += 1
            boss.steps = 0
            if boss.tentacle_atk_timer < 30:
                boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80}
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                get_hitbox(boss, boss.right_tentacle)
                get_hitbox(boss, boss.left_tentacle)
            elif boss.tentacle_atk_timer < 70:
                boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 300}
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 300}
                get_hitbox(boss, boss.right_tentacle)
                get_hitbox(boss, boss.left_tentacle)
            elif boss.tentacle_atk_timer < 100:
                boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80}
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                get_hitbox(boss, boss.right_tentacle)
                get_hitbox(boss, boss.left_tentacle)
            else:
                boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 60}
                boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 60}
                get_hitbox(boss, boss.right_tentacle)
                get_hitbox(boss, boss.left_tentacle)
                boss.tentacle_atk_timer = 0
                boss.dual_tentacle_atk = False
                boss.steps = boss.actual_steps
                boss.clock = 0

""" TEST 
    rand = randint(0, 50)
    if rand == 20:
        missile.x = randint(50, 450)
        print('atacou')
"""


### DRAW SPRITES ----------------------------------------
def draw():
    bg.draw()

    player.draw()
    if gun.reloading:
        screen.draw.filled_rect(Rect((gun.x - gun.width/2, gun.y - 20), (gun.reload_time/3, 5)), ('gray'))
    gun.draw()
    screen.draw.text(str(gun.ammo), (WIDTH - 60, HEIGHT - 40), fontsize=40, color="black")

    # exibition of stamin bar           X                                Y                            W         H        COLOR
    screen.draw.filled_rect(Rect((player.x - player.width / 4, player.y - player.height + 20), (player.stamin/2, 5)), (200, 150, 0))
    screen.draw.rect(Rect((player.x - player.width / 4, player.y - player.height + 20), (player.max_stamin/2, 5)), (200, 150, 0))
    #------------------------------
    
    screen.draw.rect(get_hitbox(player, player.hitbox), 'blue') # FOR DEBUG
    
    # boss
    boss.draw()
    if boss.alive:
        screen.draw.filled_rect(Rect((440, 20), (boss.life / 2, 10)), (200, 0, 0))
        screen.draw.rect(Rect((440, 20), (boss.max_life/2, 10)), (0, 0, 0))
        screen.draw.text(str(boss.life), (668, 33), fontsize=20, color="white")

        screen.draw.rect(get_hitbox(boss, boss.body), 'pink') # FOR DEBUG
        screen.draw.rect(get_hitbox(boss, boss.right_eye), 'blue') # FOR DEBUG
        screen.draw.rect(get_hitbox(boss, boss.left_eye), 'blue') # FOR DEBUG
        screen.draw.rect(get_hitbox(boss, boss.right_tentacle), 'red') # FOR DEBUG
        screen.draw.rect(get_hitbox(boss, boss.left_tentacle), 'gray') # FOR DEBUG
        screen.draw.rect(get_hitbox(boss, boss.mouth), 'green') # FOR DEBUG
    
    
    # bullet
    if len(gun.bullets) > 0:
        for bullet in gun.bullets:
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
    # ground line FOR DEBUG
    screen.draw.rect(Rect((0, ground), (WIDTH, 2)), ('blue'))