import pygame
import sys 
import random 
from collections import deque

def new_food(snake, surface):
  newfood = (random.randint(0, 80)*10, random.randint(0, 60)*10)
  
  while newfood in snake or newfood[1] >= 550:
    newfood = (random.randint(0, 80)*10, random.randint(0, 60)*10)
  screen.fill(0xff0000, pygame.Rect(newfood[0], newfood[1], 10, 10))
  return newfood

def next_pos(pos, delta):
  return ((pos[0] + delta[0]*10 + 800)%800, (pos[1] + delta[1]*10 + 600)%600)

def helper(_snake, _food, delt, color):
  for t in xrange(0, 80):
    (tx, ty) = ((_snake[-1][0] + dx*t*10 + 1600)%800,
                (_snake[-1][1] + dy*t*10 + 1200)%600)
    if not ((tx, ty) in _snake or (tx, ty) == _food):
      screen.fill(color, pygame.Rect(tx, ty, 10, 10))

screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

tick = 0
direction = zip([pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN],
                [(-1,0), (0,-1), (1,0), (0,1)])
dx, dy = 1, 0

snake = deque([(random.randint(0, 80)*10, random.randint(0, 60)*10)])
food = new_food(snake, screen)

score = 0
ended = False

pygame.font.init()
font48 = pygame.font.Font(None, 48)
font27 = pygame.font.Font(None, 27)
GGtext = font48.render("GAME OVER", True, (0xff, 0, 0), (0x30, 0x30, 0x30))

while True:
  tick = tick + 1
  clock.tick(18)
  if [e for e in pygame.event.get() if e.type==pygame.QUIT]:
    print "bye!"
    pygame.quit()
    sys.exit()
  if ended:
    continue

  helper(snake, food, (dx, dy), 0)

  key = pygame.key.get_pressed()
  delts = [(k_dx, k_dy) for (which, (k_dx, k_dy)) in direction if key[which]]
  if len(delts)==1 and next_pos(snake[-1], delts[0]) not in snake:
    dx, dy = delts[0]

  if tick%2 != 0:
    continue
  (x, y) = next_pos(snake[-1], (dx, dy))

  print x, y, "::", snake, "...",  delts

  if (x,y) in snake:
    screen.blit(GGtext, ((800 - GGtext.get_width())/2, (600 - GGtext.get_height())/2))
    pygame.display.flip()
    ended = True
    continue

  snake.append((x,y))

  if (x, y) == food:
    snake.appendleft((-514, -514))
    snake.appendleft((-514, -514))
    score = score + 10
    food = new_food(snake, screen)
    print "new food:", food, "score: ", score

  screen.fill(0x000000, pygame.Rect(snake[0][0], snake[0][1], 10, 10))
  screen.fill(0xffffff, pygame.Rect(snake[-1][0], snake[-1][1], 10, 10))
  snake.popleft()
  helper(snake, food, (dx, dy), 0x101010)

  scoretext = font27.render(str(score), True, (0xaa, 0xaa, 0), (0, 0, 0))
  screen.blit(scoretext, (800 - scoretext.get_width() - 5, 600 - scoretext.get_height() - 5))
  pygame.display.flip()
