import pgzrun

WIDTH = 500
HEIGHT = 400

# world options
bg = Actor('background')
gravity = 5
ground = 363

# PLAYER CONFIGS
player = Actor('player_idle')
print(player.height)
player.x = WIDTH/2
player.y = HEIGHT - player.height/2 - 5
player.is_jumping = False
player.jump_height = 50
player.jump_force = 8

# BOSS CONFIGS
boss = Actor('boss')
boss.x = WIDTH/2
boss.steps = .5
print(boss.x, boss.y)



def update():
    # world actions
    # gravity actions
    if player.y < ground:
        player.y += gravity
        print(gravity, player.jump_force)
    
    # set player in ground
    if player.y > ground:
        player.y = ground

    # boss moviments
    boss.x += boss.steps
    if boss.x >= 360 or boss.x <= 140:
        boss.steps = boss.steps * -1

    # player moviments
    if keyboard.right and player.x < 475:
        player.x += 2
    if keyboard.left and player.x > 25:
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
        
    



def draw():
    bg.draw()
    player.draw()
    boss.draw()