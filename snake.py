from machine import UART, Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import time
import random

class Snake:
    def __init__(self):
        self.horizontal = True
        self.diagonal = False
        self.body = [(0,30)]
        self.state = self.pause
        self.length = 8
        self.food = None
        self.score = 0
        
    def start(self):
        self.state()
    
    def game_over(self):
        while pause.value() == 1:
            self.body = [(0,30)]
            oled.fill(0)
            oled.text("Game over!",0,0)
            oled.text(f"Score: {self.score}", 0, 10)
            oled.show()
        if pause.value() == 0:
            oled.fill(0)
            self.score = 0
            self.food_spawn()
            self.state = self.horizontal_move_right
            self.start()
            
        
    def food_spawn(self):
        if not self.food:
            foodx = random.randint(0,126)
            foody = random.randint(0,62)
            self.food = [(foodx,foody), (foodx+1, foody), (foodx, foody+1), (foodx+1, foody+1)]
            oled.pixel(foodx, foody, 1)
            oled.pixel(foodx+1, foody, 1)
            oled.pixel(foodx, foody+1, 1)
            oled.pixel(foodx+1, foody+1, 1)
            oled.show()
        else:
            oled.pixel(self.food[0][0], self.food[0][1], 0)
            oled.pixel(self.food[1][0], self.food[1][1], 0)
            oled.pixel(self.food[2][0], self.food[2][1], 0)
            oled.pixel(self.food[3][0], self.food[3][1], 0)
            self.food = None
            self.food_spawn()
    
    def update_body(self, new_head):
        oled.pixel(new_head[0], new_head[1], 1)
        oled.show()
        self.body.append(new_head)
        if len(self.body) > self.length:
            tail = self.body.pop(0)
            oled.pixel(tail[0], tail[1], 0)
            oled.show()
    
    def pause(self):
        if pause.value() == 0:
            oled.fill(0)
            self.food_spawn()
            if self.horizontal:
                #print('moving horizontal')
                self.state = self.horizontal_move_right
            if self.diagonal:
                print('moving diagonal')
                self.state = self.diagonal_move_down
    
    def horizontal_move_right(self):
        while self.horizontal and turn_left.value() == 1 and turn_right.value() == 1:
            headx, heady = self.body[-1]
            if headx < 127:
                head = (headx+1, heady)
                self.update_body(head)
                for i in range(4):
                    if self.body[-1] == self.food[i]:
                        print(f"length: {self.length}")
                        self.length += 1
                        self.score += 1
                        print(f"length: {self.length}")
                        self.food_spawn()
                        time.sleep(0.1)
                time.sleep(0.1)
            else:
                self.game_over()
        self.diagonal = True
        self.horizontal = False
        if turn_left.value() == 0:
            while turn_left.value() == 0:
                time.sleep(0.05)
            print('turning left')
            self.state = self.diagonal_move_up
        if turn_right.value() == 0:
            while turn_right.value() == 0:
                time.sleep(0.05)
            print('turning right')
            self.state = self.diagonal_move_down
            
    def horizontal_move_left(self):
        while self.horizontal and turn_left.value() == 1 and turn_right.value() == 1:
            headx, heady = self.body[-1]
            if headx > 0:
                head = (headx-1, heady)
                self.update_body(head)
                for i in range(4):
                    if self.body[-1] == self.food[i]:
                        print(f"length: {self.length}")
                        self.length += 1
                        self.score += 1
                        print(f"length: {self.length}")
                        self.food_spawn()
                        time.sleep(0.1)
                time.sleep(0.1)
            else:
                self.game_over()
        self.diagonal = True
        self.horizontal = False
        if turn_left.value() == 0:
            while turn_left.value() == 0:
                time.sleep(0.05)
            print('turning left')
            self.state = self.diagonal_move_down
        if turn_right.value() == 0:
            while turn_right.value() == 0:
                time.sleep(0.05)
            print('turning right')
            self.state = self.diagonal_move_up
    
    def diagonal_move_down(self):
        while self.diagonal and turn_left.value() == 1 and turn_right.value() == 1:
            headx, heady = self.body[-1]
            if heady < 63:
                head = (headx, heady+1)
                self.update_body(head)
                for i in range(4):
                    if self.body[-1] == self.food[i]:
                        print(f"length: {self.length}")
                        self.length += 1
                        self.score += 1
                        print(f"length: {self.length}")
                        self.food_spawn()
                        time.sleep(0.1)
                time.sleep(0.1)
            else:
                self.game_over()
        self.diagonal = False
        self.horizontal = True
        if turn_left.value() == 0:
            while turn_left.value() == 0:
                time.sleep(0.05)
            print('turning left')
            self.state = self.horizontal_move_right
        if turn_right.value() == 0:
            while turn_right.value() == 0:
                time.sleep(0.05)
            print('turning right')
            self.state = self.horizontal_move_left
    
    def diagonal_move_up(self):
        while self.diagonal and turn_left.value() == 1 and turn_right.value() == 1:
            headx, heady = self.body[-1]
            if heady > 0:
                head = (headx, heady-1)
                self.update_body(head)
                for i in range(4):
                    if self.body[-1] == self.food[i]:
                        print(f"length: {self.length}")
                        self.length += 1
                        self.score += 1
                        print(f"length: {self.length}")
                        self.food_spawn()
                        time.sleep(0.1)
                time.sleep(0.1)
            else:
                self.game_over()
        self.diagonal = False
        self.horizontal = True
        if turn_left.value() == 0:
            while turn_left.value() == 0:
                time.sleep(0.05)
            print('turning left')
            self.state = self.horizontal_move_left
        if turn_right.value() == 0:
            while turn_right.value() == 0:
                time.sleep(0.05)
            print('turning right')
            self.state = self.horizontal_move_right
            

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

oled_width = 128
oled_height = 64

oled = SSD1306_I2C(oled_width, oled_height, i2c)

turn_left = Pin(7, Pin.IN, Pin.PULL_UP)

turn_right = Pin(8, Pin.IN, Pin.PULL_UP)

pause = Pin(9, Pin.IN, Pin.PULL_UP)

snake = Snake()

oled.fill(0)

while True:
    snake.start()
