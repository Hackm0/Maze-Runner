import pygame
import sys
import random
import time

pygame.init()

CELL_SIZE = 20
WALL_COLOR = (50, 50, 50)
PATH_COLOR = (255, 255, 255)
PLAYER_COLOR = (255, 100, 100)
START_COLOR = (100, 255, 100)
END_COLOR = (100, 100, 255)     
GAME_OVER_COLOR = (255, 0, 0)
GAME_WIN_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)
PLAYER_RADIUS = 5
PLAYER_SPEED = 1

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)]
        self.generate_maze()
        self.create_entrance_and_exit()
    
    def generate_maze(self):
        start_x, start_y = 0, 0
        
        self.maze[start_y * 2 + 1][start_x * 2 + 1] = 0
        
        stack = [(start_x, start_y)]
        
        while stack:
            current_x, current_y = stack[-1]
            
            neighbors = []
            
            if current_y > 0 and self.maze[(current_y - 1) * 2 + 1][current_x * 2 + 1] == 1:
                neighbors.append((current_x, current_y - 1, "up"))
            if current_x < self.width - 1 and self.maze[current_y * 2 + 1][(current_x + 1) * 2 + 1] == 1:
                neighbors.append((current_x + 1, current_y, "right"))
            if current_y < self.height - 1 and self.maze[(current_y + 1) * 2 + 1][current_x * 2 + 1] == 1:
                neighbors.append((current_x, current_y + 1, "down"))
            if current_x > 0 and self.maze[current_y * 2 + 1][(current_x - 1) * 2 + 1] == 1:
                neighbors.append((current_x - 1, current_y, "left"))

            #DFS
            if neighbors:
                next_x, next_y, direction = random.choice(neighbors)
                
                if direction == "up":
                    self.maze[current_y * 2][current_x * 2 + 1] = 0
                elif direction == "right":
                    self.maze[current_y * 2 + 1][current_x * 2 + 2] = 0
                elif direction == "down":
                    self.maze[current_y * 2 + 2][current_x * 2 + 1] = 0
                elif direction == "left":
                    self.maze[current_y * 2 + 1][current_x * 2] = 0
                
                self.maze[next_y * 2 + 1][next_x * 2 + 1] = 0
                
                stack.append((next_x, next_y))
            else:
                stack.pop()
    
    def create_entrance_and_exit(self):
        self.maze[0][1] = 0
        self.start_pos = (1, 0)
        
        self.maze[self.height * 2][self.width * 2 - 1] = 0
        self.end_pos = (self.width * 2 - 1, self.height * 2)

class Game:
    def __init__(self, maze_width=15, maze_height=10):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.generate_new_maze()
        
        maze_pixel_width = (self.maze.width * 2 + 1) * CELL_SIZE
        maze_pixel_height = (self.maze.height * 2 + 1) * CELL_SIZE
        
        self.screen = pygame.display.set_mode((maze_pixel_width, maze_pixel_height))
        pygame.display.set_caption("Maze Runner")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        
        self.reset_game()
    
    def generate_new_maze(self):
        self.maze = MazeGenerator(self.maze_width, self.maze_height)
        self.start_pixel_pos = (self.maze.start_pos[0] * CELL_SIZE + CELL_SIZE // 2, 
                               self.maze.start_pos[1] * CELL_SIZE + CELL_SIZE // 2)
        self.end_pixel_pos = (self.maze.end_pos[0] * CELL_SIZE + CELL_SIZE // 2, 
                             self.maze.end_pos[1] * CELL_SIZE + CELL_SIZE // 2)
    
    def reset_game(self):
        self.player_pos = list(self.start_pixel_pos)
        self.game_over = False
        self.game_won = False
        self.show_message = False
        self.message_start_time = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.generate_new_maze()
                    self.reset_game()
        
        if not self.game_over and not self.game_won:
            keys = pygame.key.get_pressed()
            
            new_pos = list(self.player_pos)
            
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                new_pos[1] -= PLAYER_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                new_pos[1] += PLAYER_SPEED
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                new_pos[0] -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                new_pos[0] += PLAYER_SPEED
            
            if not self.check_collision(new_pos):
                self.player_pos = new_pos
            
            end_rect = pygame.Rect(
                self.end_pixel_pos[0] - CELL_SIZE//2, 
                self.end_pixel_pos[1] - CELL_SIZE//2,
                CELL_SIZE, CELL_SIZE
            )
            
            if end_rect.collidepoint(self.player_pos[0], self.player_pos[1]):
                self.game_won = True
                self.show_message = True
                self.message_start_time = time.time()
    
    def check_collision(self, pos):
        x, y = pos
        
        grid_x = x // CELL_SIZE
        grid_y = y // CELL_SIZE
        
        if (grid_x < 0 or grid_x >= len(self.maze.maze[0]) or 
            grid_y < 0 or grid_y >= len(self.maze.maze)):
            return True
        
        for dx in [-PLAYER_RADIUS, 0, PLAYER_RADIUS]:
            for dy in [-PLAYER_RADIUS, 0, PLAYER_RADIUS]:
                check_x = (x + dx) // CELL_SIZE
                check_y = (y + dy) // CELL_SIZE
                
                if (0 <= check_x < len(self.maze.maze[0]) and 
                    0 <= check_y < len(self.maze.maze)):
                    if self.maze.maze[check_y][check_x] == 1:
                        if not self.game_over:
                            self.game_over = True
                            self.show_message = True
                            self.message_start_time = time.time()
                        return True
        
        return False
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        for y in range(len(self.maze.maze)):
            for x in range(len(self.maze.maze[0])):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.maze.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                else:
                    pygame.draw.rect(self.screen, PATH_COLOR, rect)
        
        start_rect = pygame.Rect(
            self.start_pixel_pos[0] - CELL_SIZE//2, 
            self.start_pixel_pos[1] - CELL_SIZE//2,
            CELL_SIZE, CELL_SIZE
        )
        end_rect = pygame.Rect(
            self.end_pixel_pos[0] - CELL_SIZE//2, 
            self.end_pixel_pos[1] - CELL_SIZE//2,
            CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(self.screen, START_COLOR, start_rect)
        pygame.draw.rect(self.screen, END_COLOR, end_rect)
        
        pygame.draw.circle(self.screen, PLAYER_COLOR, self.player_pos, PLAYER_RADIUS)
        
        if self.show_message:
            
            self.font = pygame.font.SysFont(None,20)
            
            if self.game_over:
                text = self.font.render("Game Over! Restarting...", True, GAME_OVER_COLOR)
            elif self.game_won:
                text = self.font.render("You Win! New maze loading...", True, GAME_WIN_COLOR)
            
            text_rect = text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()-10))
            self.screen.blit(text, text_rect)
            
            if time.time() - self.message_start_time > 2:
                if self.game_won:
                    self.generate_new_maze()
                self.reset_game()
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game(maze_width=10, maze_height=8)
    game.run()
