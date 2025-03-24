from machine import UART, Pin, I2C, ADC # type: ignore
from ssd1306 import SSD1306_I2C # type: ignore
import time
import random

#SW0 = start, SW1 = right, SW2 = left

class Snake:
    def __init__(self, speed, width, height):
        self.width = width
        self.height = height
        self.horizontal = True
        self.diagonal = False
        self.body = [(1,30)]
        self.state = self.pause
        self.length = 8
        self.food = None
        self.score = 0
        #Sets the speed of the snake. The high value means slower and low value means faster.
        self.speed = speed
        
    def snake_speed(self):
        if self.speed - self.score*20 <= 0:
            self.speed = 1
        else:
            self.speed -= self.score*20
        
    def start(self):
        self.state()
        
    def borders(self):
        for x in range(self.width):
            oled.pixel(x,0,1)
            oled.pixel(x,self.height-1,1)
        for y in range(self.height):
            oled.pixel(0,y,1)
            oled.pixel(self.width-1, y, 1)
        oled.show()
            
    
    def game_over(self):
        while pause.value() == 1:
            self.horizontal = True
            self.diagonal = False
            self.body = [(1,30)]
            oled.fill(0)
            oled.text("Game over!",0,0)
            oled.text(f"Score: {self.score}", 0, 10)
            oled.text("Press start to", 0, 20)
            oled.text("play!", 0, 30)
            oled.show()
        if pause.value() == 0:
            oled.fill(0)
            self.score = 0
            self.food_spawn()
            self.state = self.horizontal_move_right
            self.borders()
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
        oled.text("Press start to", 0, 0)
        oled.text("play!", 0, 10)
        oled.show()
        if pause.value() == 0:
            oled.fill(0)
            self.borders()
            self.food_spawn()
            if self.horizontal:
                self.state = self.horizontal_move_right
            if self.diagonal:
                self.state = self.diagonal_move_down
    
    def horizontal_move_right(self):
        while self.horizontal and turn_left.value() == 1 and turn_right.value() == 1:
            headx, heady = self.body[-1]
            if headx < self.width-1:
                head = (headx+1, heady)
                self.update_body(head)
                for i in range(4):
                    if self.body[-1] == self.food[i]:
                        self.length += 2
                        self.score += 1
                        self.food_spawn()
                        time.sleep_ms(self.speed)
                        self.snake_speed()
                time.sleep_ms(self.speed)
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
                        self.length += 2
                        self.score += 1
                        self.food_spawn()
                        time.sleep_ms(self.speed)
                        self.snake_speed()
                time.sleep_ms(self.speed)
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
            if heady < self.height-1:
                head = (headx, heady+1)
                self.update_body(head)
                for i in range(4):
                    if self.body[-1] == self.food[i]:
                        self.length += 2
                        self.score += 1
                        self.food_spawn()
                        time.sleep_ms(self.speed)
                        self.snake_speed()
                time.sleep_ms(self.speed)
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
                        self.length += 2
                        self.score += 1
                        self.food_spawn()
                        time.sleep_ms(self.speed)
                        self.snake_speed()
                time.sleep_ms(self.speed)
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

#Set the snakes initial speed. It is time.sleep_ms value -> higher value means slower snake and lower value means faster snake
snake = Snake(100, oled_width, oled_height)

oled.fill(0)

while True:
    snake.start()
