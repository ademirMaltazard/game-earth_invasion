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

# for menu's
state = 'menu'
actual_state = 'menu' # for back screen more used for confirmation function
menu_options = ["START GAME", "MUSIC: ON", "SOUND: ON", "QUIT GAME"]
game_over_options = ["TRY AGAIN", "MENU", 'QUIT GAME']
confirm_options = ['YES', 'NO']
cutscene = False
game_over_timer = 100
selected_option = 0
selected_confirm = 0
music_on = True
sounds_on = True

# for block double input
input_blocker = False
blocker_count = 0

# PLAYER CONFIGS
player = Actor('player_r_idle_0')
player.x = 50
player.y = HEIGHT - player.height * 2
player.max_life = 2
player.life = player.max_life
player.current_life = []
player.invencible_timer = 200
player.is_invencible = False
player.is_damaged = False
player.running = False
player.speed = 2
player.max_stamin = 50
player.stamin = player.max_stamin
player.is_firing = False
player.is_jumping = False
player.jump_timer = 0
player.jump_height = 90
player.jump_force = 10
player.direction = 'right'
player.hitbox = {'desloc_x' : 15, 'desloc_y': 26, 'width': 30, 'height': 55}
player.anim_r_idle = {'play': True,'repeat': True, 'index': -1, 'change': 10, 'timer': 0, 'frames': [ 'player_r_idle_1','player_r_idle_0', 'player_r_idle_0', 'player_r_idle_1', 'player_r_idle_2', 'player_r_idle_2']}
player.anim_l_idle = {'play': True,'repeat': True, 'index': -1, 'change': 10, 'timer': 0, 'frames': [ 'player_l_idle_1','player_l_idle_0', 'player_l_idle_0', 'player_l_idle_1', 'player_l_idle_2', 'player_l_idle_2']}
player.anim_r_walk = {'play': True,'repeat': True, 'index': -1, 'change': 10, 'timer': 0, 'frames': ['r_walk_0', 'r_walk_1', 'r_walk_2', 'r_walk_3', 'r_walk_4', 'r_walk_5', 'r_walk_6', 'r_walk_7']}
player.anim_r_firing = {'play': True,'repeat': True, 'index': -1, 'change': 10, 'timer': 0, 'frames': ['r_firing_0', 'r_firing_1', 'r_firing_2', 'r_firing_3', 'r_firing_4', 'r_firing_5', 'r_firing_6', 'r_firing_7']}
player.anim_l_walk = {'play': True,'repeat': True, 'index': -1, 'change': 10, 'timer': 0, 'frames': ['l_walk_0', 'l_walk_1', 'l_walk_2', 'l_walk_3', 'l_walk_4', 'l_walk_5', 'l_walk_6', 'l_walk_7']}
player.anim_l_firing = {'play': True,'repeat': True, 'index': -1, 'change': 10, 'timer': 0, 'frames': ['l_firing_0', 'l_firing_1', 'l_firing_2', 'l_firing_3', 'l_firing_4', 'l_firing_5', 'l_firing_6', 'l_firing_7']}

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

fire = Actor('fire_0')
fire.active = False
fire.anim = {'play': True, 'repeat': False, 'index': 1, 'change': 2, 'timer': 0, 'frames': ['fire_0', 'fire_1', 'fire_2', 'fire_3']}
        

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
boss.acid_atk = False
boss.atack_rate = 350
boss.clock = 0
boss.atk_timer = 0
boss.body = {'desloc_x' : 100, 'desloc_y': 85, 'width': 200, 'height': 100}
boss.mouth = {'desloc_x' : 20, 'desloc_y': -10, 'width': 40, 'height': 15}
boss.right_eye = {'desloc_x' : -30, 'desloc_y': -5, 'width': 40, 'height': 15}
boss.left_eye = {'desloc_x' : 68, 'desloc_y': -5, 'width': 40, 'height': 15}
boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 60}
boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 60}
boss.acid = {'desloc_x' : 20, 'desloc_y': -10, 'width': 40, 'height': 15}

# BOSS SHOOT CONFIGS
missile = Actor('missile_0')
missile.x = 0
missile.y = boss.y
missile.speed = 1
missile.is_fired = False
missile.hitbox = {'desloc_x' : 6.5, 'desloc_y': -3, 'width': 13, 'height': 18}
missile.anim = {'play': True, 'repeat': True, 'index': 0, 'change': 10, 'timer': 0, 'frames': ['missile_0', 'missile_1', 'missile_2', 'missile_1']}

# EXPLOSION
explosion = Actor('explosion_0')
explosion.x = 0
explosion.y = 0
explosion.explode = False
explosion.timer = 40
explosion.anim = {'play': True, 'repeat': False, 'index': -1, 'change': 3, 'timer': 0, 'frames': ['explosion_0', 'explosion_1', 'explosion_2', 'explosion_3', 'explosion_4', 'explosion_5', 'explosion_6','explosion_7', 'explosion_8', 'explosion_9', 'explosion_10']}

# execute animation
def animate(anim):
    if anim['play'] == True:
        anim['timer'] += 1
        if anim['timer'] % anim['change'] == 0:
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

def get_music():
    if music_on:
        if state == 'playing' or state == 'paused':
            music.play('kubbi')
        else:
            music.play('maze')
    else:
        music.stop()

def get_hitbox(actor, hitbox):
    return Rect(
        actor.x - hitbox['desloc_x'],                 # deslocamento horizontal da posição
        actor.y - hitbox['desloc_y'],                 # deslocamento vertical da posição
        hitbox['width'], hitbox['height']             # largura e altura da hitbox personalizada
    )

def get_base(actor):
    return actor.y + actor.height / 2

def get_idle():
    if player.direction == 'left':
        return animate(player.anim_l_idle)
    elif player.direction == 'right':
        return animate(player.anim_r_idle)

def get_player_life(player):
    for i in range(player.max_life):
        i += 1
        life_point = Actor('life_1')
        life_point.x = 20 * i 
        life_point.y = 20
        life_point.hit = False
        life_point.anim = {'play': True, 'repeat': False, 'index': 1, 'change': 10, 'timer': 0, 'frames': ['life_0', 'life_1', 'life_2', 'life_3', 'life_4']}
        player.current_life.append(life_point)

def damaged():
        for life_point in reversed(player.current_life):
            if life_point.hit == False:
                life_point.hit = True
                player.life -= 1
                player.is_invencible = True
                break           

def restart_game():
    global game_over_timer
    game_over_timer = 100

    # player
    player.x = 50
    player.y = HEIGHT - player.height * 2
    player.life = player.max_life
    player.current_life = []
    player.is_invencible = False
    player.is_damaged = False
    player.running = False
    player.direction = 'right'
    get_player_life(player)

    # gun
    gun.bullets = []
    gun.bullet_timer = 0
    gun.max_ammo = 30
    gun.ammo = 30

    # boss
    boss.x = WIDTH/2
    boss.y = -50
    boss.alive = False
    boss.life = boss.max_life
    boss.steps = .5
    boss.actual_step = 0
    boss.clock = 0

    # missile
    missile.x = 0
    missile.y = boss.y
    missile.is_fired = False

# when key is pressed ------------------------------------------------
def on_key_down(key):
    global selected_option, selected_confirm, confirm_options, menu_options, state, actual_state, input_blocker, music_on, sounds_on

# MENU CONFIGS --------------------------------------------------------
    if state == 'menu' or state == 'paused':
        if input_blocker:
            return
        
        if key == keys.UP or key == keys.W:
            if sounds_on: sounds.switch.play()
            selected_option = (selected_option - 1) % len(menu_options)
        if key == keys.DOWN or key == keys.S:
            if sounds_on: sounds.switch.play()
            selected_option = (selected_option + 1) % len(menu_options)
    
        if key == keys.RETURN:
            if sounds_on: sounds.confirmation.play()
            option = menu_options[selected_option]

            if 'START GAME' in option:
                restart_game()
                state = 'playing'
                get_music()

            if 'CONTINUE' in option:
                if sounds_on: sounds.minimize.play()
                menu_options[0] = 'START GAME'
                state = 'playing'
            
            if 'MUSIC: ON' in option or 'MUSIC: OFF' in option:
                music_on = not music_on
                menu_options[1] = 'MUSIC: ON' if music_on else 'MUSIC: OFF'
                get_music()

            if 'SOUND: ON' in option or 'SOUND: OFF' in option:
                sounds_on = not sounds_on
                menu_options[2] = 'SOUND: ON' if sounds_on else 'SOUND: OFF'

            if 'EXIT' in option:
                if sounds_on: sounds.maximize.play()
                actual_state = 'menu'
                input_blocker = True
                state = 'confirm_exit'
    
# CONFIRM SCREEN CONFIGS --------------------------------------
    if state == 'confirm_exit':
        if input_blocker:
            return
        
        if key == keys.LEFT or key == keys.A:
            if sounds_on: sounds.switch.play()
            selected_confirm = (selected_confirm - 1) % len(confirm_options)
        if key == keys.RIGHT or key == keys.D:
            if sounds_on: sounds.switch.play()
            selected_confirm = (selected_confirm + 1) % len(confirm_options)

        if key == keys.RETURN:
            if sounds_on: sounds.confirmation.play()
            option = confirm_options[selected_confirm]

            if 'YES' in option:
                exit()
            if 'NO' in option:
                if sounds_on: sounds.minimize.play()
                state = actual_state
                input_blocker = True
        
        if key == keys.ESCAPE:
            if sounds_on: sounds.minimize.play()
            state = actual_state
            input_blocker = True

# GAME CONFIGS ---------------------------------------------
    if state == 'playing':
        if (cutscene == False):
            if key == keys.LSHIFT and player.stamin == player.max_stamin and (player.running == False) and (keyboard.left  or keyboard.a or keyboard.right or keyboard.d):
                player.running = True
                player.speed = 4

            # Reolad ammo
            if key == keys.R:
                gun.reloading = True
            
            # 13 = ENTER BUTTON for fire
            if key == 13 and keyboard.w:
                player.is_firing = True
            
        if key == keys.ESCAPE:
            if sounds_on: sounds.maximize.play()
            menu_options[0] = 'CONTINUE'
            state = 'paused'
            actual_state = 'playing'


    if state == 'game_over':
        if input_blocker:
            return
        
        if key == keys.UP or key == keys.W:
            if sounds_on: sounds.switch.play()
            selected_option = (selected_option - 1) % len(game_over_options)
        if key == keys.DOWN or key == keys.S:
            if sounds_on: sounds.switch.play()
            selected_option = (selected_option + 1) % len(game_over_options)
    
        if key == keys.RETURN:
            if sounds_on: sounds.confirmation.play()
            option = game_over_options[selected_option]

            if 'TRY AGAIN' in option:
                restart_game()
                state = 'playing'
                get_music()

            if 'MENU' in option:
                input_blocker = True
                state = 'menu'

            if 'QUIT GAME' in option:
                if sounds_on: sounds.maximize.play()
                actual_state = 'game_over'
                input_blocker = True
                state = 'confirm_exit'


# when key is released -------------------------------------------
def on_key_up(key):
    if state == 'playing':
        if key == keys.LSHIFT:
            player.speed = 2
            player.running = False

        # 13 = ENTER BUTTON
        if key == keys.RETURN:
            player.is_firing = False

music.play('maze')
music.set_volume(0.5)


def update():
    global cutscene, state, game_over_timer, input_blocker, blocker_count, music_on, selected_option


    if input_blocker:
        blocker_count += 1
        selected_option = 0
        if blocker_count > 15:
            input_blocker = False
            blocker_count = 0

    if state == 'playing':
### WORLD ACTIONS ----------------------------------------
        # gravity actions
        if get_base(player) < ground:
            player.y += gravity

        if get_base(player) == ground:
            player.image = get_idle()
        
        # set player in ground
        if get_base(player) > ground:
            player.y = ground - player.height / 2

### PLAYER ACTIONS ----------------------------------------
        if cutscene == False:
            # left and right
            if (keyboard.right or keyboard.d) and player.x < WIDTH - 25:
                player.direction = 'right'
                player.image = animate(player.anim_r_walk)
                player.x += player.speed
                fire.x += player.speed
            if (keyboard.left  or keyboard.a) and player.x > 25:
                player.direction = 'left'
                player.image = animate(player.anim_l_walk)
                player.x -= player.speed
                fire.x -= player.speed

            # aim
            if keyboard.w or keyboard.up:
                if keyboard.left or keyboard.a:
                    player.image = animate(player.anim_l_firing)
                elif keyboard.right or keyboard.d:
                    player.image = animate(player.anim_r_firing)
                
                # no definitive animation 
                elif player.direction == 'left':
                    player.image = player.anim_l_firing['frames'][0]
                elif player.direction == 'right':
                    player.image = player.anim_r_firing['frames'][0]


            # check conditions for jump
            if keyboard.space:
                if get_base(player) == ground and player.jump_timer > 20 and player.stamin > player.max_stamin / 2:
                    player.is_jumping = True
                    player.stamin -= int(player.max_stamin / 3)
                if player.is_jumping:
                    player.y -= player.jump_force


            # add one tick for timer
            player.jump_timer += 1

        # change jump variable when reach max height
        if (get_base(player) <= ground - player.jump_height):
            player.is_jumping = False
            player.is_damaged = False
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

        if player.is_damaged:
            player.y -= player.jump_force
            if player.direction == 'left':
                player.x += 10
            if player.direction == 'right':
                player.x -= 10

        if player.is_invencible:
            player.invencible_timer -= 1
            if player.invencible_timer == 0:
                print('pode morrer')
                player.is_invencible = False
                player.invencible_timer = 200


        for life_point in player.current_life:
            if life_point.hit:
                life_point.image = animate(life_point.anim)

        if player.life == 0:
            game_over_timer -= 1
            if game_over_timer == 0:
                state = 'game_over'
                if sounds_on: sounds.game_over.play()
                get_music()


        # verify colission player -> missile
        if get_hitbox(player, player.hitbox).colliderect(get_hitbox(missile, missile.hitbox)) or get_hitbox(player, player.hitbox).colliderect(explosion._rect):
            if player.is_invencible == False:
                damaged()
                explosion.x = missile.x
                explosion.y = missile.x
                explosion.explode = True
                explosion.anim['play'] = True
                missile.y = -20
                missile.x = 0
                missile.is_fired = False
                player.is_damaged = True
        
        if get_hitbox(player, player.hitbox).colliderect(get_hitbox(boss, boss.left_tentacle)) or get_hitbox(player, player.hitbox).colliderect(get_hitbox(boss, boss.right_tentacle)) or get_hitbox(player, player.hitbox).colliderect(get_hitbox(boss, boss.acid)):
            if player.is_invencible == False:
                damaged()
                player.is_damaged =True

### GUN AND BULLET ACTIONS -------------------
        # acress bullet timer
        gun.bullet_timer += 1

        # create a new bullet
        if player.is_firing and gun.bullet_timer > 20 and gun.ammo > 0 and gun.reloading == False and (cutscene == False):
            bullet = Actor('bullet')
            fire.active = True
            fire.anim['play'] = True
            if player.direction == 'left':
                bullet.x = player.x + 7
                fire.x = player.x + 7
            elif player.direction == 'right':
                bullet.x = player.x - 7
                fire.x = player.x - 7
            bullet.y = player.y - player.height/2
            fire.y = player.y - player.height/2 - 5
            bullet.damage = 5
            bullet.is_fired = True
            gun.bullets.append(bullet)
            gun.bullet_timer = 0
            gun.ammo -= 1

        if fire.active:
            fire.image = animate(fire.anim)
            if fire.anim['play'] == False:
                fire.active = False
                fire.anim['index'] = 0
                fire.y = -60

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

            # verify collision bullet -> mouth 
            if bullet.colliderect(get_hitbox(boss, boss.mouth)):
                if boss.acid_atk == 4 and bullet.is_fired: boss.life -= bullet.damage * 2
                bullet.is_fired = False

            # verify collision bullet -> body 
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
        
        if boss.y == 140: boss.alive = True

        if boss.alive:
            cutscene = False
            boss.clock += 1

            # left and right
            boss.x += boss.steps
            if boss.x >= WIDTH - 140 or boss.x <= 140:
                boss.steps = boss.steps * -1
            
            # boss atack
            if boss.clock == boss.atack_rate:
                attack = randint(0,4)
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
                if attack == 4:
                    boss.acid_atk = True
                    print('ataque de acido')


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
                boss.atk_timer += 1
                boss.steps = 0
                if boss.atk_timer < 30:
                    boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80} #for defense
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                    get_hitbox(boss, boss.right_tentacle)
                elif boss.atk_timer < 70:
                    boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 300}
                    get_hitbox(boss, boss.right_tentacle)
                elif boss.atk_timer < 100:
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 60} #normal state
                    boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80}
                    get_hitbox(boss, boss.right_tentacle)
                else:
                    boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 60}
                    get_hitbox(boss, boss.right_tentacle)
                    boss.r_tentacle_atk = False
                    boss.steps = boss.actual_steps
                    boss.atk_timer = 0
                    boss.clock = 0

            if boss.l_tentacle_atk:
                boss.atk_timer += 1
                boss.steps = 0
                if boss.atk_timer < 30:
                    boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80} #for defense
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                    get_hitbox(boss, boss.left_tentacle)
                elif boss.atk_timer < 70:
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 300}
                    get_hitbox(boss, boss.left_tentacle)
                elif boss.atk_timer < 100:
                    boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 60} #normal state
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                    get_hitbox(boss, boss.left_tentacle)
                else:
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 60}
                    get_hitbox(boss, boss.left_tentacle)
                    boss.l_tentacle_atk = False
                    boss.steps = boss.actual_steps
                    boss.atk_timer = 0
                    boss.clock = 0
            
            if boss.dual_tentacle_atk:
                boss.atk_timer += 1
                boss.steps = 0
                if boss.atk_timer < 30:
                    boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80}
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                    get_hitbox(boss, boss.right_tentacle)
                    get_hitbox(boss, boss.left_tentacle)
                elif boss.atk_timer < 70:
                    boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 300}
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 300}
                    get_hitbox(boss, boss.right_tentacle)
                    get_hitbox(boss, boss.left_tentacle)
                elif boss.atk_timer < 100:
                    boss.right_tentacle = {'desloc_x' : -18, 'desloc_y': -30, 'width': 130, 'height': 80}
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 130, 'height': 80}
                    get_hitbox(boss, boss.right_tentacle)
                    get_hitbox(boss, boss.left_tentacle)
                else:
                    boss.right_tentacle = {'desloc_x' : -68, 'desloc_y': -30, 'width': 60, 'height': 60}
                    boss.left_tentacle = {'desloc_x' : 130, 'desloc_y': -30, 'width': 60, 'height': 60}
                    get_hitbox(boss, boss.right_tentacle)
                    get_hitbox(boss, boss.left_tentacle)
                    boss.dual_tentacle_atk = False
                    boss.steps = boss.actual_steps
                    boss.atk_timer = 0
                    boss.clock = 0
            
            # on development
            if boss.acid_atk:
                boss.atk_timer += 1
                boss.steps = 0
                if boss.atk_timer < 30:
                    boss.acid = {'desloc_x' : 15, 'desloc_y': -10, 'width': 30, 'height': 70}
                    get_hitbox(boss, boss.acid)
                elif boss.atk_timer < 70:
                    boss.acid = {'desloc_x' : 15, 'desloc_y': -10, 'width': 30, 'height': 150}
                    get_hitbox(boss, boss.acid)
                elif boss.atk_timer < 100:
                    boss.acid = {'desloc_x' : 15, 'desloc_y': -10, 'width': 30, 'height': 330}
                    get_hitbox(boss, boss.acid)
                else:
                    boss.acid = {'desloc_x' : 15, 'desloc_y': -10, 'width': 30, 'height': 15}
                    get_hitbox(boss, boss.acid)
                    boss.acid_atk = False
                    boss.steps = boss.actual_steps
                    boss.atk_timer = 0
                    boss.clock = 0


### DRAW SPRITES ----------------------------------------
def draw():
    if state == 'menu':
        screen.clear()

        # background
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (100, 100, 100))
        
        # show title
        screen.draw.filled_rect(Rect((0, 140), (WIDTH, 10)), (200, 0, 0))
        screen.draw.text('EARTH INVASION', (WIDTH * 0.25 + 3, 162), fontsize=60, color="gray")
        screen.draw.text('EARTH INVASION', (WIDTH * 0.25, 160), fontsize=60, color="black")
        screen.draw.filled_rect(Rect((0, 210), (WIDTH, 10)), (200, 0, 0))

        # show menu option
        for i, text in enumerate(menu_options):
            y = 250 + i * 30
            color = 'red' if i == selected_option else ('gray')
            screen.draw.text(text, (WIDTH * 0.2 + 2, y + 1), fontsize=25, color='black')
            screen.draw.text(text, (WIDTH * 0.2, y), fontsize=25, color=color)
        arrow_x = WIDTH * 0.2 - 15
        arrow_y = 250 + selected_option * 30
        screen.draw.text('>', (arrow_x+2, arrow_y+1), fontsize=25, color='black')
        screen.draw.text('>', (arrow_x, arrow_y), fontsize=25, color='red')

    if state == 'confirm_exit':
        # background confirm windown
        screen.draw.filled_rect(Rect((int(WIDTH*.25 - 5), int(HEIGHT*.25 - 5)), (WIDTH*.5 + 10, HEIGHT*.5 + 10)), (0, 0, 0))
        screen.draw.filled_rect(Rect((int(WIDTH*.25), int(HEIGHT*.25)), (WIDTH*.5, HEIGHT*.5)), (100, 100, 100))
        
        # confirm windown title
        screen.draw.text('ARE YOU SURE?', center=(WIDTH/2+2, HEIGHT/2-49), fontsize=25, color='black')
        screen.draw.text('ARE YOU SURE?', center=(WIDTH/2, HEIGHT/2-50), fontsize=25, color='gray')
        
        # confirm windown options
        for i, text in enumerate(confirm_options):
            x = 255 + i * 150
            color = 'red' if i == selected_confirm else ('gray')
            screen.draw.text(text, (x + 2, 270 + 1), fontsize=25, color='black')
            screen.draw.text(text, (x, 270), fontsize=25, color=color)
        arrow_x = 255 + selected_confirm * 150 - 15
        arrow_y = 268
        screen.draw.text('>', (arrow_x+2, arrow_y+1), fontsize=25, color='black')
        screen.draw.text('>', (arrow_x, arrow_y), fontsize=25, color='red')


    # game 
    if state == 'playing':
        bg.draw()

        player.draw()
        screen.draw.rect(get_hitbox(player, player.hitbox), 'blue') # FOR DEBUG
        
        # boss
        boss.draw()
        if boss.alive:
            # boss life bar
            screen.draw.filled_rect(Rect((440, 20), (boss.life / 2, 10)), (200, 0, 0))
            screen.draw.rect(Rect((440, 20), (boss.max_life/2, 10)), (0, 0, 0))
            screen.draw.text(str(boss.life), (668, 33), fontsize=20, color="white")

            screen.draw.rect(get_hitbox(boss, boss.body), 'pink') # FOR DEBUG
            screen.draw.rect(get_hitbox(boss, boss.right_eye), 'blue') # FOR DEBUG
            screen.draw.rect(get_hitbox(boss, boss.left_eye), 'blue') # FOR DEBUG
            screen.draw.rect(get_hitbox(boss, boss.right_tentacle), 'red') # FOR DEBUG
            screen.draw.rect(get_hitbox(boss, boss.left_tentacle), 'gray') # FOR DEBUG
            screen.draw.rect(get_hitbox(boss, boss.mouth), 'green') # FOR DEBUG
            screen.draw.rect(get_hitbox(boss, boss.acid), 'green') # FOR DEBUG
        
        
        # bullet
        if len(gun.bullets) > 0:
            for bullet in gun.bullets:
                if bullet.is_fired:
                    bullet.draw()
                    fire.draw()
                    screen.draw.rect(bullet._rect, 'red') # FOR DEBUG

        # missile
        if missile.is_fired:
            missile.draw()
            screen.draw.rect(get_hitbox(missile, missile.hitbox), 'blue') # FOR DEBUG

        # explosion
        if explosion.explode:
            explosion.draw()

#------------------------------------------------------------------------------
        # SCREEN HUD
        for life_point in player.current_life:
            life_point.draw()
        
        # screen.draw.text(str(player.life), (60, 40), fontsize=40, color="red") # FOR DEBUG
        # reload time bar 
        if gun.reloading:
            screen.draw.filled_rect(Rect((gun.x - gun.width/2, gun.y - 20), (gun.reload_time/3, 5)), ('gray'))

        # gun icon
        gun.draw()
        
        # exibition of ammo value 
        screen.draw.text(str(gun.ammo), (WIDTH - 60, HEIGHT - 40), fontsize=40, color="black")

        # exibition of stamin bar           X                                Y                            W         H        COLOR
        screen.draw.filled_rect(Rect((player.x - player.width / 4, player.y - player.height + 20), (player.stamin/2, 5)), (200, 150, 0))
        screen.draw.rect(Rect((player.x - player.width / 4, player.y - player.height + 20), (player.max_stamin/2, 5)), (200, 150, 0))
        
    if state == 'paused':
        # background confirm windown
        screen.draw.filled_rect(Rect((int(WIDTH*.25 - 5), int(HEIGHT*.25 - 5)), (WIDTH*.5 + 10, HEIGHT*.5 + 10)), (0, 0, 0))
        screen.draw.filled_rect(Rect((int(WIDTH*.25), int(HEIGHT*.25)), (WIDTH*.5, HEIGHT*.5)), (100, 100, 100))
        
        # confirm windown title
        screen.draw.text('PAUSE', center=(WIDTH/2+2, HEIGHT/2 - 69), fontsize=25, color='black')
        screen.draw.text('PAUSE', center=(WIDTH/2, HEIGHT/2 - 70), fontsize=25, color='gray')

        # show pause menu options
        for i, text in enumerate(menu_options):
            y = 240 + i * 30
            color = 'red' if i == selected_option else ('gray')
            screen.draw.text(text, (WIDTH * 0.42 + 2, y + 1), fontsize=25, color='black')
            screen.draw.text(text, (WIDTH * 0.42, y), fontsize=25, color=color)
        arrow_x = WIDTH * 0.42 - 15
        arrow_y = 240 + selected_option * 30
        screen.draw.text('>', (arrow_x+2, arrow_y+1), fontsize=25, color='black')
        screen.draw.text('>', (arrow_x, arrow_y), fontsize=25, color='red')
        

# GAME OVER SCREEN ------------------------------------------------------------
    if state == 'game_over':
        screen.clear()

        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (100, 100, 100))
        screen.draw.filled_rect(Rect((0, 140), (WIDTH, 10)), (200, 0, 0))
        screen.draw.text('GAME OVER', (WIDTH * 0.32 + 2, 160), fontsize=60, color="gray")
        screen.draw.text('GAME OVER', (WIDTH * 0.32, 162), fontsize=60, color="black")
        screen.draw.filled_rect(Rect((0, 210), (WIDTH, 10)), (200, 0, 0))

#       # show menu option
        for i, text in enumerate(game_over_options):
            y = 250 + i * 30
            color = 'red' if i == selected_option else ('gray')
            screen.draw.text(text, (WIDTH * 0.2 + 2, y + 1), fontsize=25, color='black')
            screen.draw.text(text, (WIDTH * 0.2, y), fontsize=25, color=color)
        arrow_x = WIDTH * 0.2 - 15
        arrow_y = 250 + selected_option * 30
        screen.draw.text('>', (arrow_x+2, arrow_y+1), fontsize=25, color='black')
        screen.draw.text('>', (arrow_x, arrow_y), fontsize=25, color='red')
