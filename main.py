from turtle import left

from pygame import *

win_width = 1024
win_height = 768
display.set_caption("cs:go 2D")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)  # задаём цвет согласно цветовой схеме RGB



# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    # метод, в котором реализовано управление спрайтом по кнопкам стрелкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        # перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость
        # сначала движение по горизонтали
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:  # идём направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)  # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif self.x_speed < 0:  # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,
                                     p.rect.right)  # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:  # идём вверх
            for p in platforms_touched:
                self.rect.top = max(self.rect.top,
                                    p.rect.bottom)  # выравниваем верхний край по нижним краям стенок, на кото


class Monster(GameSprite):
    side = "left"

    #x_leftih = 0
    #x_rightih = 0

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    # движение врага
    def update(self):
        if self.rect.x <= 400:  # w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= 900:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

## Создаём окошко
#win_width = 1024
#win_height = 768
#display.set_caption("cs:go 2D")
#window = display.set_mode((win_width, win_height))
#back = (119, 210, 223)  # задаём цвет согласно цветовой схеме RGB

# создаём группу для стен
barriers = sprite.Group()

# создаём стены картинки
#w1 = GameSprite('platform2.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
#w2 = GameSprite('platform2.png', 500, 100, 50, 400)
#w3 = GameSprite('platform2.png', 460, 70, 50, 400)

# добавляем стены в группу
#barriers.add(w1)
#barriers.add(w2)

plane = GameSprite('plane.png', 0, 0, 1024, 768)


left = GameSprite('left.png', 0, 120, 415, 425)
barriers.add(left)

defef = GameSprite('def.png', 580, 670, 200, 100)
barriers.add(defef)

up = GameSprite('up.png', 600, 0, 190, 110)
barriers.add(up)

# создаём спрайты
packman = Player('hero1.png', 30, 0, 30, 80, 0, 0)
monster = Monster('cyborg1.png', win_width - 80, 370, 30, 80, 9)
monster2 = Monster('cyborg1.png', win_width - 180, 370, 30, 80, 12)
monster3 = Monster('cyborg1.png', win_width - 130, 450, 30, 80, 15)
final_sprite = GameSprite('pachka.png', 585, 510, 55, 55)

# переменная, отвечающая за то, как кончилась игра
finish = False
# игровой цикл
run = True
while run:
    time.delay(50)


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                packman.x_speed = -5
            elif e.key == K_d:
                packman.x_speed = 5
            elif e.key == K_w:
                packman.y_speed = -5
            elif e.key == K_s:
                packman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_a:
                packman.x_speed = 0
            elif e.key == K_d:
                packman.x_speed = 0
            elif e.key == K_w:
                packman.y_speed = 0
            elif e.key == K_s:
                packman.y_speed = 0
    if not finish:
        #window.fill(back)  # закрашиваем окно цветом
        # рисуем объекты
        plane.reset()
        left.reset()
        defef.reset()
        up.reset()
        barriers.draw(window)


        monster.reset()
        monster.update()
        monster2.reset()
        monster2.update()
        monster3.reset()
        monster3.update()
        final_sprite.reset()
        #monster3.reset()
        #monster3.update()
        packman.reset()
        # включаем движение
        packman.update()
        # Проверка столкновения героя с врагом и стенами
        if sprite.collide_rect(packman, monster):
            finish = True
            # вычисляем отношение
            img = image.load('game_over.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, monster2):
            finish = True
            # вычисляем отношение
            img = image.load('game_over.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, monster3):
            finish = True
            # вычисляем отношение
            img = image.load('game_over.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('katleta.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    display.update()

