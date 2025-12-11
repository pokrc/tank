import random
import define as d
from GameX import gameX as game

def main():
    # 游戏初始化部分
    wid, hei = 900, 700
    game.display.set_window(size=(wid, hei), title="Tank War")
    color = game.color
    pen = game.pen()
    my_tick, FPS, winner = 0, 90, 0
    game_time,have_died_time = 0,0
    Running,all_move = True, True
    surface = "main"  # main是主界面，game是游戏界面，wait是缓冲界面
    temp = 0

    # 创建爆炸特效角色(玩家一&玩家二)
    boom1, boom2 = None, None
    # 制作迷宫 & 墙壁
    game_map = None
    wall_group_h = None
    wall_group_s = None
    # 创建坦克 & 属性
    p1 = d.make_tank(1)
    p2 = d.make_tank(2)
    # 加载声音
    mix = game.sound()
    mix.load_sound("boom", "sound/sound_boom.mp3")
    mix.load_sound("biu", "sound/shoot.mp3")
    mix.load_sound("didi", "sound/dudu.wav")
    mix.load_sound("xiu", "sound/xiu.mp3")
    # 创建集
    bullet_group = None  # 子弹
    skill_group = None   # 技能
    bomb_group = None    # 炸弹
    laser_group = None   # 激光
    missile_group = None # 导弹

    while Running:
        game.display.enable_exit()
        game.display.fill(color.white)
        my_tick = (my_tick + 1) % FPS
        game_time += 0.1 * int(my_tick%12==0)

        if surface == "game":
            #显示
            if winner == 0 and game_time == 0:
                p1.show = True
                p2.show = True
            pen.clear()
            p1.shoot_wait -= 1
            p2.shoot_wait -= 1

            # 游戏主要事件运行部分
            if all_move:
                # 技能事件处理
                if int(game_time) % 5 == 0 and game_time >= 5 and my_tick == 0:
                    tx = 1 + random.randint(0, 7) * 2
                    ty = 1 + random.randint(0, 4) * 2
                    x = tx * 50 - 400
                    y = -ty * 50 + 250
                    skill_group.add(d.make_skill(x, y, game_time))
                for s in skill_group:
                    if game_time - s.sur_time >= 10:
                        s.show = False
                        s.died()
                    if s.collide(p1):
                        s.show = False
                        s.died()
                        p1.has_skill = s.name
                    elif s.collide(p2):
                        s.show = False
                        s.died()
                        p2.has_skill = s.name

                # (玩家一&玩家二)的移动部分&子弹部分&技能部分
                # --玩家一
                if game.key.press("w"):
                    p1.forward(2)
                    if p1.collide(wall_group_h) or p1.collide(wall_group_s) or not p1.can_move:
                        p1.forward(-2)
                if game.key.press("s"):
                    p1.forward(-1)
                    if p1.collide(wall_group_h) or p1.collide(wall_group_s) or not p1.can_move:
                        p1.forward(1)
                if game.key.press("d"):
                    p1.facing_angle -= 2
                    if p1.collide(wall_group_h) or p1.collide(wall_group_s) or not p1.can_rotate:
                        p1.facing_angle += 2
                if game.key.press("a"):
                    p1.facing_angle += 2
                    if p1.collide(wall_group_h) or p1.collide(wall_group_s) or not p1.can_rotate:
                        p1.facing_angle -= 2
                if game.key.press("f") and p1.shoot_wait <= 0 and p1.show:
                    if p1.has_skill is None:
                        if p1.bullet_amount <= 5:
                            mix.play_sound("biu")
                            bu = d.make_bullet(p1.position.x, p1.position.y, p1.facing_angle, 0.5)
                            bullet_group.add(bu)
                            p1.bullet_amount += 1
                            p1.shoot_wait = 15
                    else:
                        if p1.has_skill == "地雷":
                            mix.play_sound("didi")
                            p1.shoot_wait = 100
                            bomb_group.add(d.make_bomb(p1.position.x, p1.position.y, game_time, p1.facing_angle))
                        elif p1.has_skill == "激光":
                            mix.play_sound("xiu")
                            p1.shoot_wait = 200
                            laser_group.add(d.make_laser(p1.position.x, p1.position.y, game_time, 1))
                        elif p1.has_skill == "追踪":
                            mix.play_sound("didi")
                            p1.shoot_wait = 1200
                            missile_group.add(d.make_missile(p1.position.x, p1.position.y, game_time, p1.facing_angle, 1))
                        else:
                            print("技能还没做")
                        p1.has_skill = None
                # --玩家二
                if game.key.press("i"):
                    p2.forward(2)
                    if p2.collide(wall_group_h) or p2.collide(wall_group_s) or not p2.can_move:
                        p2.forward(-2)
                if game.key.press("k"):
                    p2.forward(-1)
                    if p2.collide(wall_group_h) or p2.collide(wall_group_s) or not p2.can_move:
                        p2.forward(1)
                if game.key.press("l"):
                    p2.facing_angle -= 2
                    if p2.collide(wall_group_h) or p2.collide(wall_group_s) or not p2.can_rotate:
                        p2.facing_angle += 2
                if game.key.press("j"):
                    p2.facing_angle += 2
                    if p2.collide(wall_group_h) or p2.collide(wall_group_s) or not p2.can_rotate:
                        p2.facing_angle -= 2
                if game.key.press("p") and p2.shoot_wait <= 0 and p2.show:
                    if p2.has_skill is None:
                        if p2.bullet_amount <= 5:
                            mix.play_sound("biu")
                            bu = d.make_bullet(p2.position.x, p2.position.y, p2.facing_angle, 0.51)
                            bullet_group.add(bu)
                            p2.bullet_amount += 1
                            p2.shoot_wait = 15
                    elif p2.has_skill == "激光":
                        mix.play_sound("xiu")
                        p2.shoot_wait = 200
                        laser_group.add(d.make_laser(p2.position.x, p2.position.y, game_time, 2))
                    elif p2.has_skill == "追踪":
                        mix.play_sound("didi")
                        p2.shoot_wait = 1200
                        missile_group.add(d.make_missile(p2.position.x, p2.position.y, game_time, p2.facing_angle, 2))
                    else:
                        if p2.has_skill == "地雷":
                            mix.play_sound("didi")
                            p2.shoot_wait = 100
                            bomb_group.add(d.make_bomb(p2.position.x, p2.position.y, game_time, p2.facing_angle))
                        else:
                            print("技能还没做")
                        p2.has_skill = None
                # --子弹操作处理部分
                for b in bullet_group:
                    # 子弹撞墙侦测 & 子弹拐弯
                    if b.collide(wall_group_h):
                        b.facing_angle = 360 - b.facing_angle
                        b.collide_num += 1
                    elif b.collide(wall_group_s):
                        b.facing_angle = 180 - b.facing_angle
                        b.collide_num += 1
                    # 子弹移动部分 & 检测子弹是否击杀玩家
                    # --子弹存活部分
                    if b.collide_num <= 15:
                        b.forward(3)
                        # 检测是否撞到玩家一
                        if b.collide(p1) and ((b.collide_num >= 1 and b.scale == 0.5) or (b.scale == 0.51)) and p1.show:
                            mix.play_sound("boom")
                            boom1.is_boom = True
                            boom1.position = p1.position
                            if b.scale == 0.5:
                                p1.bullet_amount -= 1
                            else:
                                p2.bullet_amount -= 1
                            b.died()
                            p1.show = False
                        # 检测是否撞到玩家二
                        if b.collide(p2) and ((b.collide_num >= 1 and b.scale == 0.51) or (b.scale == 0.5)) and p2.show:
                            mix.play_sound("boom")
                            boom2.is_boom = True
                            boom2.position = p2.position
                            if b.scale == 0.5:
                                p1.bullet_amount -= 1
                            else:
                                p2.bullet_amount -= 1
                            b.died()
                            p2.show = False
                    # --子弹燃尽部分
                    else:
                        # 检测是谁的子弹，并相应减少子弹存活数
                        if b.scale == 0.5:
                            p1.bullet_amount -= 1
                        else:
                            p2.bullet_amount -= 1
                        b.died()  # 子弹死亡
                # 地雷部分
                for b in bomb_group:
                    if game_time - b.sur_time < 1 and b.move >= 0:
                        b.forward(-1 * b.move)
                        b.move /= 1.04
                        if b.collide(wall_group_h):
                            b.facing_angle = 360 - b.facing_angle
                        elif b.collide(wall_group_s):
                            b.facing_angle = 180 - b.facing_angle
                    else:
                        b.move = 0
                        b.show = False
                        if b.collide(p1):
                            mix.play_sound("boom")
                            boom1.is_boom = True
                            boom1.position = p1.position
                            b.died()
                            p1.show = False
                        if b.collide(p2):
                            mix.play_sound("boom")
                            boom2.is_boom = True
                            boom2.position = p2.position
                            b.died()
                            p2.show = False
                # 激光部分
                for l in laser_group:
                    if game_time - l.sur_time <= 0.5:
                        if l.belong == 1:
                            p1.can_rotate = False
                            p1.can_move = False
                            l.facing_angle = p1.facing_angle
                            l.position.x = p1.position.x
                            l.position.y = p1.position.y
                            l.forward(622)
                            if l.collide(p2) and p2.show:
                                mix.play_sound("boom")
                                boom2.is_boom = True
                                boom2.position = p2.position
                                p2.show = False
                        if l.belong == 2:
                            p2.can_rotate = False
                            p2.can_move = False
                            l.facing_angle = p2.facing_angle
                            l.position.x = p2.position.x
                            l.position.y = p2.position.y
                            l.forward(622)
                            if l.collide(p1) and p1.show:
                                mix.play_sound("boom")
                                boom1.is_boom = True
                                boom1.position = p1.position
                                p1.show = False
                    else:
                        if l.belong == 1:
                            p1.can_rotate = True
                            p1.can_move = True
                            p1.has_skill = None
                        if l.belong == 2:
                            p2.can_rotate = True
                            p2.can_move = True
                            p2.has_skill = None
                        l.show = False
                        l.died()
                # 导弹部分
                for s in missile_group:
                    if game_time - s.sur_time <= 10:
                        if my_tick == 0:
                            mix.play_sound("didi")
                        s.sculpt_number = 0
                        s.forward(2)
                        if s.belong == 1:
                            p1.can_rotate = False
                            if game.key.press("a"):
                                s.facing_angle += 3
                            if game.key.press("d"):
                                s.facing_angle -= 3
                        if s.belong == 2:
                            p2.can_rotate = False
                            if game.key.press("j"):
                                s.facing_angle += 3
                            if game.key.press("l"):
                                s.facing_angle -= 3
                        if s.collide(wall_group_h):
                            s.forward(-10)
                            s.facing_angle = 360 - s.facing_angle
                            s.forward(10)
                        elif s.collide(wall_group_s):
                            s.forward(-10)
                            s.facing_angle = 180 - s.facing_angle
                            s.forward(10)
                        s.next_sculpt()
                        # 击杀判定
                        if s.collide(p1) and game_time - s.sur_time >= 0.3:
                            mix.play_sound("boom")
                            boom1.is_boom = True
                            boom1.position = p1.position
                            s.died()
                            p1.show = False
                            p2.can_move = True
                            p2.has_skill = None
                            p2.can_rotate = True
                            p2.shoot_wait = 0
                        if s.collide(p2) and game_time - s.sur_time >= 0.3:
                            mix.play_sound("boom")
                            boom2.is_boom = True
                            boom2.position = p2.position
                            s.died()
                            p2.show = False
                            p1.can_move = True
                            p1.has_skill = None
                            p1.can_rotate = True
                            p1.shoot_wait = 0
                    else:
                        if s.belong == 1:
                            p1.can_move = True
                            p1.has_skill = None
                            p1.can_rotate = True
                        if s.belong == 2:
                            p2.can_move = True
                            p2.has_skill = None
                            p2.can_rotate = True
                        s.show = False
                        s.died()

                # 爆炸特效(玩家一 & 玩家二)
                if boom1.is_boom:
                    boom1.show = True
                    if my_tick % 5 == 0:
                        boom1.next_sculpt(1)
                    if boom1.sculpt_number == 6:
                        boom1.sculpt_number = 0
                        boom1.show = False
                        boom1.is_boom = False
                if boom2.is_boom:
                    boom2.show = True
                    if my_tick % 5 == 0:
                        boom2.next_sculpt(1)
                    if boom2.sculpt_number == 6:
                        boom2.sculpt_number = 0
                        boom2.show = False
                        boom2.is_boom = False

            # 胜利的判断
            if p1.show is True and p2.show is False:
                winner = 1
            else:
                if p1.show is False and p2.show is True:
                    winner = -1
                else:
                    if p1.show is False and p2.show is False:
                        winner = 0
            if winner != 0 and temp == 0:
                temp = 1
                print(winner)
                have_died_time = game_time
            if have_died_time != 0:
                if game_time - have_died_time > 3:
                    if winner > 0:
                        all_move = False
                        pen.set_color(color.red)
                        pen.write("1 Win!", (0, 0), 100)
                    elif winner < 0:
                        all_move = False
                        pen.set_color(color.green)
                        pen.write("2 Win!", (0, 0), 100)
                    else:
                        all_move = False
                        pen.set_color(color.cyan)
                        pen.write("No Win!", (0, 0), 100)
                    if game_time - have_died_time > 4:
                        print("End")
                        surface = "main"
        elif surface == "main":
            p1.show = False
            p2.show = False
            try:
                for q in wall_group_h:
                    q.show = False
                for q in wall_group_s:
                    q.show = False
                for i in skill_group:
                    i.show = False
                    i.died()
                for i in bullet_group:
                    i.show = False
                    i.died()
                for i in bomb_group:
                    i.show = False
                    i.died()
                for i in laser_group:
                    i.show = False
                    i.died()
                for i in missile_group:
                    i.show = False
                    i.died()
            except:
                pass
            pen.clear()
            pen.write("Tank War", (0, 100), 150)
            if 0 < my_tick < 60:
                pen.write("Press space start game", (0, -130), 40)
            if game.key.press("space") or game.key.press("return"):
                surface = "game"
                game_time = 0
                have_died_time = 0
                winner,temp = 0,0
                all_move = True
                # 创建集
                bullet_group = game.role.new_group()  # 子弹
                skill_group = game.role.new_group()  # 技能
                bomb_group = game.role.new_group()  # 炸弹
                laser_group = game.role.new_group()  # 激光
                missile_group = game.role.new_group()  # 导弹
                # 创建爆炸特效角色(玩家一&玩家二)
                boom1, boom2 = d.make_boom(), d.make_boom()
                # 制作迷宫 & 墙壁
                game_map = d.make_map(17, 11)
                wall_group_h = game.role().new_group()
                wall_group_s = game.role().new_group()
                # --横向墙壁
                for i in range(2, len(game_map) - 1, 2):
                    for j in range(3, len(game_map[i]) - 1, 2):
                        x_, y_ = 50 * j - 400, 50 * -i + 250
                        if game_map[i][j] == '#':
                            wall = d.make_wall(x_, y_, 0, 20)
                            wall_group_h.add(wall)
                wall_1 = d.make_wall(0, 250, 0, 159)
                wall_2 = d.make_wall(0, -250, 0, 159)
                wall_group_h.add(wall_1, wall_2)
                # --纵向墙壁
                for i in range(1, len(game_map), 2):
                    for j in range(2, len(game_map[i]) - 2, 2):
                        x_, y_ = 50 * j - 400, 50 * -i + 250
                        if game_map[i][j] == '#':
                            wall = d.make_wall(x_, y_, 90, 20)
                            wall_group_s.add(wall)
                wall_3 = d.make_wall(-400, 0, 90, 99)
                wall_4 = d.make_wall(400, 0, 90, 99)
                wall_group_s.add(wall_3, wall_4)
                # 创建坦克 & 属性
                p1 = d.make_tank(1)
                p2 = d.make_tank(2)

        game.display.update()
        game.display.tick(FPS)

if __name__ == "__main__":
    main()