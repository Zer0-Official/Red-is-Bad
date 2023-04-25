import pygame
from pygame import mixer
from time import sleep

pygame.init()
mixer.init()

width, height = 900, 500
scrn = pygame.display.set_mode((width, height))
pygame.display.set_caption('Red is Bad')
pygame.display.set_icon(pygame.image.load('src/icon.ico'))
clock = pygame.time.Clock()
fps = 60

c_bg = (135, 206, 235)
c_player = (30, 30, 30)
c_red = (214, 34, 21)
c_goal = (64, 184, 13)

title_font = pygame.font.SysFont('arial', 70)
instruct_font = pygame.font.SysFont('arial', 30)
lvl_font = pygame.font.SysFont('arial', 20)

player_w, player_h = 60, 60
player_rect = pygame.Rect(100, 100, player_w, player_h)
velocity = 4
red_vel = 1
goal_rect = pygame.Rect(870, 200, 30, 100)
win_lvl = 6

NEXT_LVL = pygame.USEREVENT + 1
WIN = pygame.USEREVENT + 2
LOSE = pygame.USEREVENT + 3
TRICK = pygame.USEREVENT + 4

lvl_sound = mixer.Sound('src/lvl_done.wav')
win_sound = mixer.Sound('src/win.wav')
lose_sound = mixer.Sound('src/lose.wav')
trick_sound = mixer.Sound('src/trick.wav')


def game():
    global player_rect
    stage = 'title'
    lvl = 0
    reds = []
    tricked = False
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif e.type == pygame.QUIT:
                pygame.quit()

            if stage == 'title':
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        stage = 'game'
                        pygame.event.post(pygame.event.Event(NEXT_LVL))
            elif stage == 'game':
                if e.type == NEXT_LVL:
                    lvl_sound.play()
                    lvl += 1
                    if lvl == 1:
                        player_rect = pygame.Rect(100, 100, player_w, player_h)
                        reds = [(500, 200), (700, 130)]
                    elif lvl == 2:
                        player_rect = pygame.Rect(200, 200, player_w, player_h)
                        reds = [(450, 10), (450, 110), (450, 250), (450, 350), (450, 430)]
                    elif lvl == 3:
                        player_rect = pygame.Rect(300, 240, player_w, player_h)
                        reds = [(260, 170), (370, 220), (260, 310), (200, 170), (130, 230), (170, 360), (170, 430),
                                (830, 120), (830, 320), (770, 197)]
                    elif lvl == 4:
                        player_rect = pygame.Rect(730, 200, player_w, player_h)
                        reds = [(800, 200), (730, 270), (730, 130), (660, 270), (590, 270), (520, 290), (660, 130),
                                (590, 130), (520, 130), (460, 165), (770, 320), (895, 320)]
                    elif lvl == 5:
                        player_rect = pygame.Rect(50, 210, player_w, player_h)
                        reds = [(200, 10), (200, 80), (200, 150), (200, 220), (200, 342), (200, 410), (200, 480),
                                (400, 10), (400, 130), (400, 200), (400, 270), (400, 340), (400, 410), (400, 480),
                                (470, 130), (470, 10), (590, 70)]
                    elif lvl >= win_lvl:
                        pygame.event.post(pygame.event.Event(WIN))
                if e.type == WIN:
                    win_sound.play()
                    stage = 'win'
                if e.type == LOSE:
                    lose_sound.play()
                    stage = 'lose'
                if e.type == TRICK:
                    trick_sound.play()

            elif stage == 'lose':
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        game()

        scrn.fill(c_bg)

        if stage == 'title':
            scrn.blit(title_font.render('Red is Bad', True, (255, 0, 0)), (width / 2 - 150, height / 6))
            scrn.blit(instruct_font.render('(enter to play)', True, (0, 0, 0)), (width / 2 - 90, height / 2 + 50))

        elif stage == 'game':
            keys = pygame.key.get_pressed()

            draw_player(player_rect, keys)

            pygame.draw.rect(scrn, c_goal, goal_rect)
            render_reds(reds)
            scrn.blit(lvl_font.render('Level: ' + str(lvl), True, (0, 0, 0)), (10, 10))

            if lvl == 5 and tricked and player_rect.x > 550:
                scrn.blit(lvl_font.render("I was so close! Let's go back", True, (0, 0, 0)),
                          (player_rect.x - 70, player_rect.y - 30))

            if player_rect.colliderect(goal_rect):
                sleep(0.5)
                if lvl != 5:
                    pygame.event.post(pygame.event.Event(NEXT_LVL))
                else:
                    if tricked is False:
                        goal_rect.x = 0
                        tricked = True
                        pygame.event.post(pygame.event.Event(TRICK))
                    else:
                        pygame.event.post(pygame.event.Event(NEXT_LVL))
            for red in reds:
                if player_rect.colliderect(pygame.Rect(red[0], red[1], 60, 60)):
                    pygame.event.post(pygame.event.Event(LOSE))

        elif stage == 'win':
            scrn.fill((0, 255, 0))
            scrn.blit(title_font.render('All Red is Gone!', True, (0, 0, 255)), (width / 4, height / 4))

        elif stage == 'lose':
            scrn.fill((255, 0, 0))
            scrn.blit(title_font.render('Red has Taken Over!', True, (0, 0, 0)), (width / 5, height / 4))
            scrn.blit(instruct_font.render('Enter to replay.', True, (0, 0, 0)), (width / 2 - 100, height / 2 + 50))

        pygame.display.update()
        clock.tick(fps)


def draw_player(rect, keys):
    if keys[pygame.K_LEFT] and rect.x - velocity > 0:
        rect.x -= velocity
    if keys[pygame.K_RIGHT] and rect.x + velocity + rect.width < width:
        rect.x += velocity
    if keys[pygame.K_UP] and rect.y - velocity > 0:
        rect.y -= velocity
    if keys[pygame.K_DOWN] and rect.y + velocity + rect.height < height:
        rect.y += velocity
    pygame.draw.rect(scrn, c_player, rect)


def render_reds(reds):
    for red in reds:
        pygame.draw.rect(scrn, c_red, pygame.Rect(red[0], red[1], 60, 60))


if __name__ == '__main__':
    game()
