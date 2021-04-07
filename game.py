import random
import pygame

# CONSTANTS
BLOCK_SIZE = 5
BOARD_BLOCKS_X = 10
BOARD_BLOCKS_Y = 10
ROW_SIZE = 10
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
FOOD_IN_VISION = 50
HUNGER = 50


# Player ---------------------------------------------------------------------------------------------------------------
class Head:
    # VISION WIDTH | HEIGHT -> INPUT
    # ADD FITNESS FOR GOOD STUFF ( FOOD IN VISION )
    # TURN LEFT | RIGHT -> OUTPUT

    def __init__(self, x, y, game):
        self.posX = x
        self.posY = y
        self.segments = [Segment(self.posX, self.posY)]
        self.game = game
        self.direction = RIGHT
        self.alive_turns = 0
        self.hunger = HUNGER
        self.points = 500
        self.turn_right_dict = {LEFT :  UP,
                               UP : RIGHT,
                               RIGHT: DOWN,
                               DOWN:LEFT}
        self.turn_left_dict = {LEFT: DOWN,
                               DOWN: RIGHT,
                               RIGHT: UP,
                               UP: LEFT}

    def show(self):
        print("Coordinates X:{}, Y:{}".format(self.posX, self.posY))

    def turn_left(self):
        self.direction = self.turn_left_dict[self.direction]

    def turn_right(self):
        self.direction = self.turn_right_dict[self.direction]

    def move(self):
        if self.direction == UP:
            self.posY -= BLOCK_SIZE
        elif self.direction == DOWN:
            self.posY += BLOCK_SIZE
        elif self.direction == LEFT:
            self.posX -= BLOCK_SIZE
        elif self.direction == RIGHT:
            self.posX += BLOCK_SIZE

        for i in range(len(self.segments) - 1, -1, -1):
            if i > 0:
                self.segments[i].set_pos(self.segments[i - 1].posX, self.segments[i - 1].posY)
            else:
                self.segments[0].set_pos(self.posX, self.posY)

    def draw(self, win):
        # pygame.draw.rect(win, (0, 255, 0), (self.posX, self.posY, BLOCK_SIZE, BLOCK_SIZE))
        segment_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        segment_img.fill((000, 255, 0))
        win.blit(segment_img, (self.posX, self.posY))


    def collideCheck(self, posX, posY):
        # Check collision
        # Out of bounds
        if posX < 0 or posX >= self.game.width or posY < 0 or posY >= self.game.height:
            return True
        # Collision with self
        else:
            for segment in self.segments[1:]:
                if segment.check_collision(posX, posY):
                    return True
        return False

    def food_collect(self):
        if self.game.food.posX == self.posX and self.game.food.posY == self.posY:
            self.hunger = HUNGER
            self.game.food = Food(random.randrange(0, BOARD_BLOCKS_X - 1) * BLOCK_SIZE,
                                  random.randrange(0, BOARD_BLOCKS_Y - 1) * BLOCK_SIZE)
            self.segments.append(
                Segment(self.segments[len(self.segments) - 1].posX, self.segments[len(self.segments) - 1].posY))
            return True
        return False

    # INPUT CONFIGURATIONS

    # Vision 3x3 in front approach
    def checkVision(self):
        vision = []

        if self.direction == UP:
            for i in range(-1, 2):
                for j in range(1, 4):
                    tmp_x = self.posX + (i * BLOCK_SIZE)
                    tmp_y = self.posY - (j * BLOCK_SIZE)
                    if self.game.food.posX == tmp_x and self.game.food.posY == tmp_y:
                        vision.append(1)
                        self.points += FOOD_IN_VISION
                    elif tmp_x < 0 or tmp_x > (BOARD_BLOCKS_X * BLOCK_SIZE) \
                            or tmp_y < 0 or tmp_y > (BOARD_BLOCKS_Y * BLOCK_SIZE):
                        vision.append(-1)
                    else:
                        vision.append(0)

        elif self.direction == DOWN:
            for i in range(-1, 2):
                for j in range(1, 4):
                    tmp_x = self.posX + (i * BLOCK_SIZE)
                    tmp_y = self.posY + (j * BLOCK_SIZE)
                    if self.game.food.posX == tmp_x and self.game.food.posY == tmp_y:
                        vision.append(1)
                        self.points += FOOD_IN_VISION
                    elif tmp_x < 0 or tmp_x > (BOARD_BLOCKS_X * BLOCK_SIZE) \
                            or tmp_y < 0 or tmp_y > (BOARD_BLOCKS_Y * BLOCK_SIZE):
                        vision.append(-1)
                    else:
                        vision.append(0)

        elif self.direction == LEFT:
            for i in range(1, 4):
                for j in range(-1, 2):
                    tmp_x = self.posX - (i * BLOCK_SIZE)
                    tmp_y = self.posY + (j * BLOCK_SIZE)
                    if self.game.food.posX == tmp_x and self.game.food.posY == tmp_y:
                        vision.append(1)
                        self.points += FOOD_IN_VISION
                    elif tmp_x < 0 or tmp_x > (BOARD_BLOCKS_X * BLOCK_SIZE) \
                            or tmp_y < 0 or tmp_y > (BOARD_BLOCKS_Y * BLOCK_SIZE):
                        vision.append(-1)
                    else:
                        vision.append(0)
        else:
            for i in range(1, 4):
                for j in range(-1, 2):
                    tmp_x = self.posX + (i * BLOCK_SIZE)
                    tmp_y = self.posY + (j * BLOCK_SIZE)
                    if self.game.food.posX == tmp_x and self.game.food.posY == tmp_y:
                        vision.append(1)
                        self.points += FOOD_IN_VISION
                    elif tmp_x < 0 or tmp_x > (BOARD_BLOCKS_X * BLOCK_SIZE)\
                            or tmp_y < 0 or tmp_y > (BOARD_BLOCKS_Y * BLOCK_SIZE):
                        vision.append(-1)
                    else:
                        vision.append(0)
        return vision

    # Distance approach
    def checkBoard(self):
        up_distance = self.posY / BLOCK_SIZE
        down_distance = BOARD_BLOCKS_Y - (self.posY / BLOCK_SIZE)
        left_distance = self.posX / BLOCK_SIZE
        right_distance = BOARD_BLOCKS_Y - (self.posY / BLOCK_SIZE)
        food_positionx = self.game.food.posX / BLOCK_SIZE
        food_positiony = self.game.food.posY / BLOCK_SIZE
        food_distancex = abs(food_positionx - (self.posX / BLOCK_SIZE))
        food_distancey = abs(food_positiony - (self.posY / BLOCK_SIZE))
        vision = [up_distance, down_distance, left_distance, right_distance, food_positionx, food_positiony,
                  food_distancex, food_distancey]
        return vision

    # Short Vision approach
    def checkVision2(self):
        vision = []
        if self.direction == UP:
            # Looking Straight
            ahead = self.posY - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, ahead):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY == ahead and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posX - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(left, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX == left and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(right, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX == right and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
        elif self.direction == DOWN:
            # Looking Straight
            ahead = self.posY + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, ahead):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY == ahead and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(left, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX == left and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(right, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX == right and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
        elif self.direction == LEFT:
            # Looking Straight
            ahead = self.posX - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(ahead, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX == ahead and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posY + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, left):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY == left and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posY - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, right):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY == right and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
        else:
            # Looking Straight
            ahead = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(ahead, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX == ahead and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posY - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, left):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY == left and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posY + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, right):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY == right and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)

        return vision

    # Short vision with global line of sight for food
    def checkVision3(self):
        vision = []
        if self.direction == UP:
            # Looking Straight
            ahead = self.posY - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, ahead):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY < self.posY and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posX - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(left, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX < self.posX and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(right, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX > self.posX and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
        elif self.direction == DOWN:
            # Looking Straight
            ahead = self.posY + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, ahead):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY > self.posY and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(left, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX > self.posX and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(right, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX < self.posX and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
        elif self.direction == LEFT:
            # Looking Straight
            ahead = self.posX - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(ahead, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX < self.posX and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posY + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, left):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY > self.posY and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posY - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, right):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY < self.posY and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
        # Direction RIGHT
        else:
            # Looking Straight
            ahead = self.posX + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(ahead, self.posY):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posX > self.posX and self.game.food.posY == self.posY:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Left
            left = self.posY - BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, left):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY < self.posY and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)
            # Looking Right
            right = self.posY + BLOCK_SIZE
            # Safe movement
            if self.collideCheck(self.posX, right):
                vision.append(-1)
            else:
                vision.append(0)
            # Food found
            if self.game.food.posY > self.posY and self.game.food.posX == self.posX:
                vision.append(1)
                self.points += FOOD_IN_VISION
            else:
                vision.append(0)

        return vision


# Body of the player
class Segment:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y

    def set_pos(self, x, y):
        self.posX = x
        self.posY = y

    # Detect collision with head, causing the end of game prematurely
    def check_collision(self, posX, posY):
        if self.posX == posX and self.posY == posY:
            # print('Mine: {},{}'.format(self.posX,self.posY))
            # print('Head: {},{}'.format(head.posX,head.posY))
            return True
        return False

    def show(self):
        print("Coordinates X:{}, Y:{}".format(self.posX, self.posY))

    def draw(self, win):
        # pygame.draw.rect(win, (0, 0, 0), (self.posX, self.posY, BLOCK_SIZE, BLOCK_SIZE))
        segment_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        segment_img.fill((0, 0, 0))
        win.blit(segment_img, (self.posX, self.posY))


# Objects --------------------------------------------------------------------------------------------------------------
# Collectible points
class Food:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y

    def draw(self, win):
        # pygame.draw.rect(win, (255, 0, 0), (self.posX, self.posY, BLOCK_SIZE, BLOCK_SIZE))
        segment_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        segment_img.fill((255, 0, 0))
        win.blit(segment_img, (self.posX, self.posY))


# Obstacles, collision with them causes game to end
# TO BE IMPLEMENTED
class Wall:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y


# Game -----------------------------------------------------------------------------------------------------------------
class Game:
    def __init__(self, width, height, id):
        self.width = width
        self.height = height
        self.id = id
        self.screen = pygame.Surface((width, height))
        self.walls = []
        self.food = Food(random.randrange(0, BOARD_BLOCKS_X - 1) * BLOCK_SIZE,
                         random.randrange(0, BOARD_BLOCKS_Y - 1) * BLOCK_SIZE)

    def draw(self):
        self.screen.fill((255, 255, 255))

    def blitScreen(self, glob_screen):
        # determine row
        # 5 games per row
        y_pos = self.id // ROW_SIZE
        # determine position in row
        x_pos = self.id % ROW_SIZE
        distance_x = 0.5 * BOARD_BLOCKS_X * BLOCK_SIZE
        distance_y = 0.5 * BOARD_BLOCKS_Y * BLOCK_SIZE
        glob_screen.blit(self.screen,
                         ((distance_x + ((self.width + distance_x) * x_pos)),
                          (distance_y + ((self.height + distance_y) * y_pos))))


# Draw all elements
def draw_all(game, player, glob_screen):
    game.draw()
    for segment in player.segments:
        segment.draw(game.screen)
    game.food.draw(game.screen)
    player.draw(game.screen)
    game.blitScreen(glob_screen)
    pygame.display.update()
