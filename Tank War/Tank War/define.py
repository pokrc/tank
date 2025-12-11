from GameX import gameX as game
import random

# 制作子弹
def make_bullet(x,y,angle,size):
    bullet = game.role(_staticmethod=True)
    bullet.add_sculpt("img/bullet.gif")
    bullet.scale = size # 0.5
    bullet.position.x = x
    bullet.position.y = y
    bullet.facing_angle = angle
    bullet.collide_num = 0
    return bullet

# 制作墙
def make_wall(x,y,angle,width):
    wall = game.role(_staticmethod=True)
    wall.add_sculpt("img/block.gif")
    wall.position.x = x
    wall.position.y = y
    wall.scale = 0.005
    wall.facing_angle = angle
    wall.high_scale = 0.7
    wall.width_scale = width
    return wall

#制作爆炸特效
def make_boom():
    boom = game.role()
    boom.is_boom = False
    for i in [1, 2, 3, 4, 5, 6, 7]:
        boom.add_sculpt(f"img/boom{i}.gif")
    boom.show = False
    boom.sculpt_number = 0
    boom.scale = 0.5
    boom.adjust_layer("bottom")
    return boom

# 制作坦克
def make_tank(player):
    p = game.role()
    p.add_sculpt(f"img/p{player}.gif")
    p.scale = 0.08
    rand = random.randint(0, 179)
    rand *= 2
    p.facing_angle = rand
    p.bullet_amount = 0
    p.shoot_wait = 0
    p.has_skill = None
    x,y = random.randint(0,1),random.randint(0,4)
    x = 1 + x*2 + (player-1)*8
    y = 1 + y*2
    p.position.x,p.position.y = x * 50 - 400, -y * 50 + 250
    p.can_move = True
    p.can_rotate = True
    return p

# 制作迷宫
def in_map(x, y, game_map):
    return 0 <= x < len(game_map) and 0 <= y < len(game_map[0])
def dfs_map(game_map, x, y):
    directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if in_map(nx, ny,game_map) and game_map[nx][ny] == '#':
            game_map[x + dx // 2][y + dy // 2] = ' '
            game_map[nx][ny] = ' '
            dfs_map(game_map, nx, ny)
def make_map(width,height):
    gp = []
    for i in range(height):  # 迷宫的高度
        gp.append([])
        for j in range(width):  # 迷宫的宽度
            gp[i].append('#')
    gp[1][1] = ' '
    dfs_map(gp, 1, 1)
    for _ in range(25):
        r_x = random.randint(2, height-2)
        if r_x % 2 == 0: r_x -= 1
        r_y = random.randint(2, width-2)
        if r_y % 2 == 0: r_y -= 1
        # 确保在通路附近生成
        if gp[r_x][r_y] == '#' and (
            gp[r_x - 1][r_y] == ' ' or gp[r_x + 1][r_y] == ' ' or
            gp[r_x][r_y - 1] == ' ' or gp[r_x][r_y + 1] == ' '
        ):
            gp[r_x][r_y] = ' '
    return gp

# 制作技能
def make_skill(x,y,time):
    skill_list = ["img/bomb.gif","img/skill_light.gif","img/wifi.gif"]
    skill_name = ["地雷","激光","追踪"]
    skill = game.role(_staticmethod=True)
    r = random.randint(0, 2)
    skill.sc = r
    skill.name = skill_name[r]
    skill.add_sculpt(skill_list[r])
    skill.position.x = x
    skill.position.y = y
    skill.scale = 0.3
    skill.sur_time = time
    return skill
def make_bomb(x,y,time,towards):
    bomb = game.role(_staticmethod=True)
    bomb.add_sculpt("img/bomb.gif")
    bomb.position.x = x
    bomb.position.y = y
    bomb.scale = 0.3
    bomb.sur_time = time
    bomb.facing_angle = towards
    bomb.move = 5
    return bomb
def make_laser(x,y,time,belong):
    laser = game.role()
    laser.add_sculpt("img/light.gif")
    laser.position.x = x
    laser.position.y = y
    laser.scale = 0.02
    laser.width_scale = 500
    laser.sur_time = time
    laser.belong = belong
    return laser
def make_missile(x,y,time,towards,belong):
    missile = game.role()
    missile.add_sculpt("img/bullet.gif","img/Tank_Missile.gif")
    missile.position.x = x
    missile.position.y = y
    missile.scale = 0.2
    missile.sur_time = time
    missile.facing_angle = towards
    missile.belong = belong
    return missile

# 求法部分
'''
                   _ooOoo_
                  o8888888o
                  88" = "88
                  (| -_- |)
                  o\  ~  /o
              _____/'---'\_____
             '   |||     |||   '
            '     \|     |/     '
           ./  |||||  :  |||||   \.
           |  _||||| ::: |||||_   |
           | __|||| ::::: ||||__  |
             佛祖保佑,永无BUG,顺利运行
            非静心无以明智,非宁静无以致远
'''
