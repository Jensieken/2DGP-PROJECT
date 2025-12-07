import os
import random
from pico2d import load_image, draw_rectangle, load_font
import game_framework
import game_world
from state_machine import StateMachine

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

RUN_SPEED_KMPH = 80.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

_hp_font = None
def _get_hp_font():
    global _hp_font
    if _hp_font is None:
        try:
            base_dir = os.path.dirname(__file__)
            font_path = os.path.join(base_dir, 'ENCR10B.TTF')
            # 무조건 ENCR10B.TTF 사용
            _hp_font = load_font(font_path, 16)
        except Exception as e:
            print(f'[Font] ENCR10B.TTF 로드 실패: {font_path} -> {e}')
            _hp_font = None
    return _hp_font

class ResourceManager:
    _images = {}\

    def load_image(key, filename):
        if key in ResourceManager._images:
            return ResourceManager._images[key]

        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'monster_image', filename)
        if not os.path.exists(path):
            print(f'이미지 파일이 없습니다: {path}')
            ResourceManager._images[key] = None
            return None

        try:
            img = load_image(path)
        except Exception as e:
            print(f'이미지 로드 실패: {path} -> {e}')
            img = None

        ResourceManager._images[key] = img
        return img

class AttackHit:

    def __init__(self, x, y, face_dir=1, owner='girl', life_time=0.18, w=60, h=40, damage=None):
        self.x = x
        self.y = y
        self.face_dir = face_dir
        self.owner = owner
        self.life = life_time
        self.w = w
        self.h = h

        if damage is None:
            self.damage = 20 if self.owner == 'girl' else 10
        else:
            self.damage = damage

        if self.owner == 'girl':
            game_world.add_collision_pair('weapon_vs_monster', self, None)
        else:
            game_world.add_collision_pair('monster_vs_player', self, None)
        game_world.add_object(self, 3)

    def update(self):
        self.life -= game_framework.frame_time
        if self.life <= 0:
            try:
                game_world.remove_object(self)
            except Exception:
                pass

    def draw(self):
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)

    def get_bb(self):
        if self.face_dir == 1:
            left = self.x
            right = self.x + self.w
        else:
            left = self.x - self.w
            right = self.x
        bottom = self.y - (self.h // 2)
        top = self.y + (self.h // 2)
        return int(left), int(bottom), int(right), int(top)

    def handle_collision(self, group, other):
        try:
            game_world.remove_object(self)
        except Exception:
            pass


def spawn_attack_hit(x, y, face_dir=1, damage=None, w=None, h=None):
    if w is None:
        w = 60
    if h is None:
        h = 40
    return AttackHit(x + face_dir * 20, y, face_dir=face_dir, owner='girl', damage=damage, w=w, h=h)


def spawn_monster_attack(x, y, face_dir=-1, damage=None):
    return AttackHit(x + face_dir * 20, y, face_dir=face_dir, owner='monster', damage=damage)

class Goblin:
    images = None

    AGGRO_DISTANCE = 250
    ATTACK_RANGE = 60

    def find_player(self):

        for layer in game_world.world:
            for o in layer:
                if getattr(o, '__class__', None).__name__ == 'Girl':
                    return o
        return None

    class Idle:
        IMAGE_KEY = 'idle'
        def __init__(self, goblin):
            self.goblin = goblin
            self.timer = 0.0
            self.duration = 1.0

        def enter(self, e):
            self.goblin.dir = 0
            self.goblin.frame = 0.0
            self.timer = 0.0
            self.duration = random.uniform(0.8, 2.5)
        def exit(self, e):
            pass

        def do(self):
            import game_framework
            frame_count = 1
            self.goblin.frame = (self.goblin.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count
            self.timer += game_framework.frame_time

            player = self.goblin.find_player()
            if player:
                dx = player.x - self.goblin.x
                if abs(dx) <= self.goblin.AGGRO_DISTANCE:
                    self.goblin.face_dir = 1 if dx > 0 else -1
                    self.goblin.dir = self.goblin.face_dir
                    self.goblin.state_machine.change_state(self.goblin.RUN)
                    return

            if self.timer >= self.duration:
                self.goblin.state_machine.change_state(self.goblin.RUN)

        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 1
            fw = img.w // frame_count
            fh = img.h
            frame = int(self.goblin.frame) % frame_count
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)

    class Run:
        IMAGE_KEY = 'run'
        def __init__(self, goblin):
            self.goblin = goblin
            self.timer = 0.0
            self.duration = 1.5
        def enter(self, e):
            self.goblin.frame = 0.0
            self.timer = 0.0
            self.duration = random.uniform(1.0, 3.0)
            if getattr(self.goblin, 'dir', 0) == 0:
                self.goblin.dir = random.choice([-1, 1])
            self.goblin.face_dir = self.goblin.dir

        def exit(self, e):
            pass

        def do(self):
            import game_framework
            frame_count = 4
            self.goblin.frame = (self.goblin.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count

            player = self.goblin.find_player()
            if player:
                dx = player.x - self.goblin.x
                dist = abs(dx)
                if dist <= self.goblin.ATTACK_RANGE:
                    if getattr(self.goblin, 'attack_cooldown', 0.0) <= 0.0:
                        self.goblin.face_dir = 1 if dx > 0 else -1
                        self.goblin.state_machine.change_state(self.goblin.ATTACK)
                        return
                    else:
                        self.goblin.face_dir = 1 if dx > 0 else -1
                elif dist <= self.goblin.AGGRO_DISTANCE:
                    self.goblin.dir = 1 if dx > 0 else -1
                    self.goblin.face_dir = self.goblin.dir

            self.goblin.x += self.goblin.dir * self.goblin.speed * game_framework.frame_time
            if self.goblin.x < 20:
                self.goblin.x = 20; self.goblin.dir = 1; self.goblin.face_dir = 1
            elif self.goblin.x > 1580:
                self.goblin.x = 1580; self.goblin.dir = -1; self.goblin.face_dir = -1

            self.timer += game_framework.frame_time
            if self.timer >= random.uniform(1.0, 3.0):
                if random.random() < 0.25 and getattr(self.goblin, 'attack_cooldown', 0.0) <= 0.0:
                    self.goblin.state_machine.change_state(self.goblin.ATTACK)
                else:
                    self.goblin.state_machine.change_state(self.goblin.IDLE)
        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 4
            fw = img.w // frame_count
            fh = img.h
            frame = int(self.goblin.frame) % frame_count
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)

    class Attack:
        IMAGE_KEY = 'attack'
        def __init__(self, goblin):
            self.goblin = goblin
            self.playing = False
            self._hit_spawned = False
        def enter(self, e):
            self.goblin.frame = 0.0
            self.playing = True
            self._hit_spawned = False
            try:
                self.goblin.attack_cooldown = 2.0
                spawn_monster_attack(self.goblin.x, self.goblin.y, self.goblin.face_dir)
                self._hit_spawned = True
            except Exception:
                pass
        def exit(self, e):
            self.playing = False
            self._hit_spawned = False

        def do(self):
            import game_framework
            frame_count = 3
            if not self.playing: return
            self.goblin.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time
            if self.goblin.frame >= frame_count:
                self.goblin.frame = frame_count - 1
                self.playing = False
                self.goblin.state_machine.change_state(self.goblin.IDLE)

        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 3
            fw = img.w // frame_count
            fh = img.h
            frame = int(min(self.goblin.frame, frame_count - 1))
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)

    class Hit:
        IMAGE_KEY = 'hit'
        def __init__(self, goblin):
            self.goblin = goblin
            self.playing = False
            self.timer = 0.0

        def enter(self, e):
            self.goblin.frame = 0.0
            self.playing = True
            self.timer = 0.0
            knockback = 40
            self.goblin.x += -self.goblin.face_dir * knockback


        def exit(self, e):
            self.playing = False

        def do(self):
            import game_framework
            frame_count = 2
            if not self.playing: return
            self.goblin.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time
            self.timer += game_framework.frame_time
            if self.timer >= 0.4 or self.goblin.frame >= frame_count:
                self.playing = False
                self.goblin.state_machine.change_state(self.goblin.IDLE)

        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 2
            fw = img.w // frame_count
            fh = img.h
            frame = int(min(self.goblin.frame, frame_count - 1))
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)


    def __init__(self, x=400, y=40):

        self.images = {
            'idle': ResourceManager.load_image('idle', 'goblin_idle.png'),
            'run': ResourceManager.load_image('run', 'goblin_run.png'),
            'attack': ResourceManager.load_image('attack', 'goblin_attack.png'),
            'hit': ResourceManager.load_image('hit', 'goblin_hit.png'),
        }

        self.x = x
        self.y = y
        self.frame = 0.0
        self.face_dir = -1  # -1 left, 1 right
        self.dir = 0
        self.speed = 100.0
        self.hp = 30

        self.attack_cooldown = 0.0

        self.IDLE = self.__class__.Idle(self)
        self.RUN = self.__class__.Run(self)
        self.ATTACK = self.__class__.Attack(self)
        self.HIT = self.__class__.Hit(self)

        transitions = {
            self.IDLE: {},
            self.RUN: {},
            self.ATTACK: {},
            self.HIT: {}
        }
        self.state_machine = StateMachine(self.IDLE, transitions)

        game_world.add_collision_pair('weapon_vs_monster', None, self)
        game_world.add_object(self, 2)

    def get_image(self, key):
        return self.images.get(key)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        try:
            if getattr(self, 'attack_cooldown', 0.0) > 0.0:
                import game_framework
                self.attack_cooldown = max(0.0, self.attack_cooldown - game_framework.frame_time)
        except Exception:
            pass

        try:
            font = _get_hp_font()
            if font:
                hp_text = f'HP: {self.hp}'
                font.draw(int(self.x - 20), int(self.y + 60), hp_text, (255, 0, 0))
        except Exception:
            pass

    def get_bb(self):
        w = 40
        h = 60
        left = int(self.x - w // 2)
        right = int(self.x + w // 2)
        bottom = int(self.y - 10)
        top = int(self.y + h - 10)
        return left, bottom, right, top

    def handle_collision(self, group, other):
        try:
            if group == 'weapon_vs_monster':
                damage = getattr(other, 'damage', 20)
                self.hp = max(0, self.hp - damage)
                if self.hp <= 0:
                    try:
                        game_world.remove_object(self)
                    except Exception:
                        pass
                else:
                    try:
                        self.state_machine.change_state(self.HIT)
                    except Exception:
                        pass
        except Exception:
            pass

class MonsterSpawner:
    def __init__(self, count=5, x_range=(200, 1400), y_fixed=40, respawn_interval=3.0, respawn_count=5, max_total_spawns=100):
        self.count = count
        self.x_range = x_range
        self.y_fixed = y_fixed

        self.respawn_interval = respawn_interval
        self.respawn_count = respawn_count
        self.max_total_spawns = max_total_spawns

        self.respawn_timer = 0.0
        self.total_spawned = 0


        self.spawn_initial()

        # game_world에 업데이트를 위해 추가
        game_world.add_object(self, 4)

    def spawn_initial(self):

        for _ in range(self.count):
            if self.total_spawned >= self.max_total_spawns:
                break
            x = random.randint(self.x_range[0], self.x_range[1])
            create_goblin(x, self.y_fixed)
            self.total_spawned += 1

    def update(self):

        import game_framework


        if self.total_spawned >= self.max_total_spawns:
            return

        self.respawn_timer += game_framework.frame_time

        if self.respawn_timer >= self.respawn_interval:
            self.respawn_timer = 0.0

            for _ in range(self.respawn_count):
                if self.total_spawned >= self.max_total_spawns:
                    break
                x = random.randint(self.x_range[0], self.x_range[1])
                create_goblin(x, self.y_fixed)
                self.total_spawned += 1

            print(f"[MonsterSpawner] 총 스폰된 몬스터: {self.total_spawned}/{self.max_total_spawns}")

    def draw(self):
        pass

    def spawn_initial(self):
        for _ in range(self.count):
            x = random.randint(self.x_range[0], self.x_range[1])
            create_goblin(x, self.y_fixed)


def create_goblin(x, y):
    return Goblin(x, y)