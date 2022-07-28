import pygame as pg
import random

# инициализация игры
pg.init()

# параметры экрана
width = 600
height = 800
display = pg.display.set_mode((width, height))
pg.display.set_caption('bird')
FPS = pg.time.Clock()
score = 0

# Шрифт
font_type = "font/FARCEB__.TTF"
font_size = 30
font_color = (0, 0, 0)

# параметры птицы
bird_width = 100
bird_height = 73
position_x = 50
position_y = 350
jump = False

# изображение птицы
bird_up = [pg.image.load('image/up.png'), pg.image.load('image/up3.png'), pg.image.load('image/up2.png')]
bird_fall = pg.image.load('image/fall.png')
animation = 6

# параметры труб
trumpet_bot = [pg.image.load('image/small.png'), pg.image.load('image/middle.png'), pg.image.load('image/big.png')]
reverse_trumpet = [pg.image.load('image/reverse_small.png'), pg.image.load('image/reverse_middle.png'),pg.image.load('image/reverse_big.png')]

trumpet_option = [115, 645, 115, 675, 115, 525]
reverse_trumpet_option = [155, 1, 155, 1 , 155, 1]
h_reverse_trumbet = [154, 224, 274]

# Звуки
pg.mixer.music.load("music/Chris Christodoulou feat. Christos Spirakis, Thanasi Moustogiannis - Ashes to As.mp3")
pg.mixer.music.set_volume(0.1)

fly = pg.mixer.Sound("music/fly.mp3")
death = pg.mixer.Sound("music/death.mp3")

# функция игры
def run_game():
    global position_y, jump
    game = True
    background = pg.image.load('image/background.jpg')
    pg.mixer.music.play(-1)

    # Списки труб
    trumpet_array = []
    reverse_array = []
    create_array(trumpet_array)
    create_array_reverse(reverse_array)

    while game:
        # цикл выхода из игры
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
                quit()

        # Управление
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_SPACE]:
            make_jump()
        else:
            fall()

        if pressed_keys[pg.K_ESCAPE]:
            pause()

        # Колизии
        if (position_y >= 720) or (position_y <= 0):
            pg.mixer.Sound.play(death)
            game_over()

        if (collision(trumpet_array)) or (r_collision(reverse_array)):
            pg.mixer.Sound.play(death)
            game_over()

        # Отрисовка и параметры экрана
        pg.display.update()
        display.blit(background, (0, 0))
        FPS.tick(60)

        draw_array(trumpet_array)
        draw_reverse_array(reverse_array)

        print_text("SCORE: " + str(score), 400, 10, font_color, font_type, font_size)
        score_counter(trumpet_array)

# функция падения
def fall():
    global position_y
    position_y += 4
    display.blit(bird_fall, (position_x, position_y))
    pg.display.update()

# функция прыжка
def make_jump():
    global position_y, jump, animation
    pg.mixer.Sound.play(fly)
    pg.mixer.Sound.set_volume(fly, 0.1)
    jump = True
    position_y -= 10
    
    # анимация
    if animation == 12:
        animation = 0

    display.blit(bird_up[animation // 6], (position_x, position_y))
    animation += 1

# трубы снизу
class Trumpets:
    def __init__(self, x, y, width_t, img, speed):
        self.x = x
        self.y = y
        self.width_t = width_t
        self.img = img
        self.speed = speed

    # Функция движения
    def move(self):
        if self.x >= -self.width_t:
            display.blit(self.img, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            self.x = width + 12 + random.randrange(- 8, 6)
            return False

    # Возвращаюший прикол)
    def return_trumpet(self, radius, y, width_t, img):
        self.x = radius
        self.y = y
        self.width_t = width_t
        self.img = img

        display.blit(self.img, (self.x, self.y))

# трубы сверху
class Reverse:
    def __init__(self, x_r, y_r, width_r, img_r, speed_r, col):
        self.x_r = x_r
        self.y_r = y_r
        self.width_r = width_r
        self.img_r = img_r
        self.speed_r = speed_r
        self.col = col

    # Функция движения
    def move(self):
        if self.x_r >= -self.width_r:
            display.blit(self.img_r, (self.x_r, self.y_r))
            self.x_r -= self.speed_r
            return True
        else:
            self.x_r = width + 12 + random.randrange(- 8, 6)
            return False

    # Возвращаюший прикол) 2.0
    def return_trumpet_reverse(self, radius_r, y_r, width_r, img_r, col):
        self.x_r = radius_r
        self.y_r = y_r
        self.width_r = width_r
        self.img_r = img_r
        self.col = col

        display.blit(self.img_r, (self.x_r, self.y_r))

# фунции создания труб
def create_array(array):
    pos = [width, 150, 300, 450, 600]

    for i in range (0, 5):
        if i == 0:
            choice = random.randrange(0, 3)
            img = trumpet_bot[choice]
            width_a = trumpet_option[choice * 2]
            height_a = trumpet_option[choice * 2 + 1]

            array.append(Trumpets(width, height_a, width_a, img, 4))
        else:
            choice = random.randrange(0, 3)
            img = trumpet_bot[choice]
            width_a = trumpet_option[choice * 2]
            height_a = trumpet_option[choice * 2 + 1]

            array.append(Trumpets(width + pos[i], height_a, width_a, img, 4))

def create_array_reverse(array):
    pos = [width, 150, 300, 450, 600]

    for i in range(0, 5):
        if i == 0:
            choice_r = random.randrange(0, 3)
            img_r = reverse_trumpet[choice_r]
            width_r = reverse_trumpet_option[choice_r * 2]
            height_r = reverse_trumpet_option[choice_r * 2 + 1]
            col = h_reverse_trumbet[choice_r]

            array.append(Reverse(width, height_r, width_r, img_r, 4, col))
        else:
            choice_r = random.randrange(0, 3)
            img_r = reverse_trumpet[choice_r]
            width_r = reverse_trumpet_option[choice_r * 2]
            height_r = reverse_trumpet_option[choice_r * 2 + 1]
            col = h_reverse_trumbet[choice_r]

            array.append(Reverse(width + pos[i], height_r, width_r, img_r, 4, col))

# Поиск радиуса от последней трубы, чтобы заспавнить новую
def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < width:
        radius = width
        if radius - maximum < 10:
            radius += 3
    else:
        radius = maximum

    choice = random.randrange(0, 5)

    if choice == 0:
        radius += random.randrange(1, 5)
    else:
        radius += random.randrange(2, 5)

    return radius

def find_radius_reverse(array_r):
    maximum = max(array_r[0].x_r, array_r[1].x_r, array_r[2].x_r)

    if maximum < width:
        radius_r = width
        if radius_r - maximum < 10:
            radius_r += 3
    else:
        radius_r = maximum

    choice_r = random.randrange(0, 5)

    if choice_r == 0:
        radius_r += random.randrange(1, 5)
    else:
        radius_r += random.randrange(2, 5)

    return radius_r

# Отрисовка труб
def draw_array(array):
    for Trumpets in array:
        check = Trumpets.move()

        if not check:
            radius = find_radius(array)
            choice = random.randrange(0, 3)
            img = trumpet_bot[choice]
            width_a = trumpet_option[choice * 2]
            height_a = trumpet_option[choice * 2 + 1]

            Trumpets.return_trumpet(radius, height_a, width_a, img)

def draw_reverse_array(array_r):
    for reverse in array_r:
        check = reverse.move()

        if not check:
            radius_r = find_radius_reverse(array_r)
            choice_r = random.randrange(0, 3)
            img_r = reverse_trumpet[choice_r]
            width_r = reverse_trumpet_option[choice_r * 2]
            height_r = reverse_trumpet_option[choice_r * 2 + 1]

            if choice_r == 3:
                col = h_reverse_trumbet[choice_r - 1]
            else:
                col = h_reverse_trumbet[choice_r]

            reverse.return_trumpet_reverse(radius_r, height_r, width_r, img_r, col)

# Колизии
def collision(barriers):
    for barrier in barriers:

        if position_y + bird_height >= barrier.y:
            if barrier.x <= position_x <= barrier.x + barrier.width_t:
                return True
            elif barrier.x <= position_x + bird_width <= barrier.x + barrier.width_t:
                return True
    return False

def r_collision(barriers_reverse):
    for barrier_r in barriers_reverse:
        
        if position_y <= barrier_r.y_r + barrier_r.col: 
            if barrier_r.x_r <= position_x <= barrier_r.x_r + barrier_r.width_r:
                return True
            elif barrier_r.x_r <= position_x + bird_width <= barrier_r.x_r + barrier_r.width_r:
                return True
    return False

# Функция вывода текста на экран
def print_text(message, x, y, font_color, font_type, font_size):
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))

# Счетчик очков
def score_counter(barriers):
    global score
    
    for barrier in barriers:
        if position_x > barrier.x:
            score += 1

    return (score - 1)

# Пауза
def pause():
    paused = True
    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
                quit()

        print_text("Пауза....Раздови кнопку Enter, если хочешь продожить.",
                    10, 300, font_color, font_type = "font/ua-BRAND-regular.otf", font_size = 19)
        print_text("Но если хочешь выйти, ебаника по кнопке F1.", 10, 330, font_color, font_type = "font/ua-BRAND-regular.otf", font_size = 19)

        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_RETURN]:
            paused = False
        if pressed_keys[pg.K_F1]:
            quit()

        pg.display.update()
        FPS.tick(60)
            
# конец игры
def game_over():
    global score
    over = True

    while over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
                quit() 

        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_RETURN]:
            score = 0
            run_game()

        if pressed_keys[pg.K_ESCAPE]:
            quit() 
        
        print_text("Вы проиграли...ваш счет " + str(score), 10, 300, font_color, font_type = "font/ua-BRAND-regular.otf", font_size = 30)
        print_text("Для перезапуска нажмите Enter, для выхода ESC", 10, 350, font_color, font_type = "font/ua-BRAND-regular.otf", font_size = 20)

        pg.display.update()
        FPS.tick(60)

run_game() 
