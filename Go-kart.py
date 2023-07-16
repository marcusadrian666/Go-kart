import pygame
import random

# 初始化游戏
pygame.init()

# 设置游戏窗口尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Go Kart Racing")

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
car_image = pygame.image.load("car.png")  # 加载卡丁车图像

# 定义卡丁车类
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 限制卡丁车在窗口范围内移动
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

# 定义障碍物类
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(screen_height - self.rect.height)

    def update(self):
        self.rect.y += 3

        # 当障碍物移出屏幕时重新生成
        if self.rect.y > screen_height:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -self.rect.height)

# 创建游戏精灵组
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# 创建卡丁车实例
car = Car()
all_sprites.add(car)

# 创建障碍物实例
for i in range(10):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                car.speed_x = 5
            elif event.key == pygame.K_UP:
                car.speed_y = -5
            elif event.key == pygame.K_DOWN:
                car.speed_y = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car.speed_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car.speed_y = 0

    # 更新游戏精灵
    all_sprites.update()

    # 检测卡丁车与障碍物的碰撞
    hits = pygame.sprite.spritecollide(car, obstacles, False)
    if hits:
        running = False

    # 清空屏幕
    screen.fill(black)

    # 绘制游戏精灵
    all_sprites.draw(screen)

    # 更新屏幕显示
    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(60)

# 游戏结束
pygame.quit()
