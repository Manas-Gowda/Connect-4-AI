
import pygame, math, random
import numpy as np


ROW_COUNT = 6
COLUMN_COUNT = 7

boxsize = 70
radius = 25
width = COLUMN_COUNT * 70 + 20
height = (ROW_COUNT + 1) * 70 + 60
p1 = 1
p2 = 2
ai = 2
turn = random.randint(0, 1)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 240, 0)
green = (0, 200, 0)
light_green = (0, 255, 0)
pista = (205, 255, 220)
cream = (255, 253, 208)
orange = (255, 150, 0)
gold = (255, 200, 15)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('4 in a row')
icon = pygame.image.load('icon1.png')
pygame.display.set_icon(icon)

welcomeimg = pygame.image.load('welcome1.jpg')
# get a rectangle around the image {.get_rect()} and place the center  
# of the rectangle at x = centre of screen, y = image height / 2
position = welcomeimg.get_rect(center=(width // 2, (welcomeimg.get_height() // 2)))
# (or) position = welcomeimg.get_rect()
#      position.center = (width//2,95)
infoimg = pygame.image.load('discription.JPG')
img = pygame.image.load('desc.jpg')

board = np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        y = np.equal(0, board[r][col])
        if (y) == True :
            return r


def winning_move(board, piece):
    start = (0, 0)
    end = (0, 0)

    # check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and board[r][c + 1] == piece
                    and board[r][c + 2] == piece and board[r][c + 3] == piece):
                start = (c * 70 + 10 + 35, height - (r * 70 + 45))
                end = ((c + 3) * 70 + 10 + 35, height - (r * 70 + 45))
                return True, start, end

    # check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece
                    and board[r + 2][c] == piece and board[r + 3][c] == piece):
                start = (c * 70 + 10 + 35, height - (r * 70 + 45))
                end = (c * 70 + 10 + 35, height - ((r + 3) * 70 + 45))
                return True, start, end

    # check +ve sloped diagonals /
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece
                    and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
                start = (c * 70 + 10 + 35, height - (r * 70 + 45))
                end = ((c + 3) * 70 + 10 + 35, height - ((r + 3) * 70 + 45))
                return True, start, end

    # check -ve sloped diagonals \
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece
                    and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece):
                start = (c * 70 + 10 + 35, height - (r * 70 + 45))
                end = ((c + 3) * 70 + 10 + 35, height - ((r - 3) * 70 + 45))
                return True, start, end

    return False, start, end


def tie_move(board):
    empty_cells = 42
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] != 0:
                empty_cells -= 1
                if empty_cells == 0:
                    return True
    return False


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, blue, (c * 70 + 10, r * 70 + 70 + 50, 70, 70))
            pygame.draw.circle(screen, white, (c * 70 + 35 + 10, r * 70 + 70 + 35 + 50), radius)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == p1:  # it should fill from bottom row
                pygame.draw.circle(screen, red, (c * 70 + 35 + 10, height - (r * 70 + 45)), radius)
            elif board[r][c] == p2:
                pygame.draw.circle(screen, yellow, (c * 70 + 35 + 10, height - (r * 70 + 45)), radius)


def display_text(text, colour, size, x, y):
    font = pygame.font.SysFont('comicsansms', size)
    textsurf = font.render(text, True, colour)
    textpos = textsurf.get_rect(center=(x, y))
    screen.blit(textsurf, textpos)


def button(text, x, y, width, height, inactive_colour, active_colour, command=None):
    pygame.draw.rect(screen, inactive_colour, (x, y, width, height))

    pos = pygame.mouse.get_pos()#print(pos)
    click = pygame.mouse.get_pressed()#print(click)
    
    if x + width > pos[0] > x and y + height > pos[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, width, height))
        if click[0] == 1:
            pygame.mixer.music.load('options .mp3')
            pygame.mixer.music.play()
            pygame.time.wait(300)

            if command == '1player':
                one_player()    
            elif command == '2player':
                two_players()          
            elif command == 'quit':
                running = False
                pygame.quit()
                quit()
                
            elif command == 'again':
                two_players()
            elif command == 'main':
                game_intro()
            elif command == 'again_ai':
                one_player()
            elif command == 'main_ai':
                game_intro()

    display_text(text, black, 25, x + width // 2, y + height // 2)


def score_position(window, piece):
    score = 0
    opp_piece = p1
    if piece == p1:
        opp_piece = ai

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(piece) == 1:
        score += 10
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def score_board(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, 3])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])] # contains a list of all pieces in a preticular row
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+4] # list of all consecutive 4 pieces in that row_array
            score += score_position(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+4]
            score += score_position(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)] # list of consecutive 4 pieces of a diagonal
            score += score_position(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += score_position(window, piece)

    return score


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_columns = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_columns)
    for col in valid_columns:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score1 = score_board(temp_board, piece)
        if score1 > best_score:
            best_score = score1
            best_col = col

    return best_col

def is_terminal_node(board):
    win_ai,start,end = winning_move(board,ai)
    win_p1,start,end = winning_move(board,p1)
    tie = tie_move(board)
    return win_ai or win_p1 or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    #print('v  ',valid_locations)
    is_terminal = is_terminal_node(board)
    #print('s_terminal ',is_terminal)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, ai):
                return (None, 100000000000000)
            elif winning_move(board, p1):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            #print('score_board   ',score_board(board, ai))
            return (None, score_board(board, ai))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, ai)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, p1)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


    
def player(board, piece):
    global turn
    pos = pygame.mouse.get_pos()
    if 500 > pos[0] > 10:
        posx = pos[0]
        col = math.floor((posx - 10) / boxsize)
        if is_valid_location(board, col):
            pygame.mixer.music.load('drop2.mp3')
            pygame.mixer.music.play()
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)
            turn += 1
            turn = turn % 2


def one_player():
    global turn ,start, end
    start,end = (0,0),(0,0)
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype='int32')
    GameOver = False
    GameExit = False
    while not GameExit:
        screen.fill(white)
        screen.blit(img,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameExit = True
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                if turn == 0:
                    posx = event.pos[0]
                    pygame.draw.circle(screen, red, (posx, 50 + boxsize // 2 + 5), radius)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
                if turn == 0:  # ask player 1's input
                    player(board,p1)
                    win, start, end = winning_move(board, p1)
                    if win == True:
                        pygame.mixer.music.load('win.mp3')
                        pygame.mixer.music.play()
                        display_text('You Win!', red, 55, width // 2, 50 + 30)
                        time = pygame.time.get_ticks()
                        GameOver = True

                    if tie_move(board):
                        pygame.mixer.music.load('draw.mp3')
                        pygame.mixer.music.play()
                        display_text('Game Draw', light_green, 55, width // 2, 50 + 30)
                        time = pygame.time.get_ticks()
                        GameOver = True
                    draw_board(board)

            if turn == 1 and GameOver == False:
                #col = random.randint(0,6)
                #col = pick_best_move(board,ai)
                col, minimax_score = minimax(board, 2, -math.inf, math.inf, True)
                #print('mini   ',minimax_score)
                x = is_valid_location(board,col)
                if x == True:
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,ai)
                    pygame.mixer.music.load('drop_piece .mp3')
                    pygame.mixer.music.play(start = 0.288) # start playing sound at 0.288 sec
                    
                win,start,end = winning_move(board,ai)
                if win:
                    pygame.mixer.music.load('lose123.mp3')
                    pygame.mixer.music.play()
                    display_text('You Lose!',red,55,width//2,50+30)
                    time = pygame.time.get_ticks()
                    GameOver = True
                    
                if tie_move(board):
                    pygame.mixer.music.load('draw.mp3')
                    pygame.mixer.music.play()
                    display_text('Game Draw', light_green, 55, width // 2, 50 + 30)
                    time = pygame.time.get_ticks()
                    GameOver = True
            turn = 0
            #turn =turn%2

            #print(np.flip(board, 0))
            draw_board(board)
            pygame.draw.line(screen, pista, start, end, 3)
            pygame.display.update()

        while GameOver == True:
            #pygame.time.wait(2000)

            if pygame.time.get_ticks() - time >= 1500:
                pygame.draw.rect(screen, cream, (150, 130, 210, 270))
                button('Play Again', 170, 190, 170, 50, orange, gold, command='again_ai')
                button('Main Menu', 170, 290, 170, 50, orange, gold, command='main_ai')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameExit = True
                    GameOver = False
                    pygame.quit()
                    quit()
            pygame.display.update()


def two_players():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype='int32')
    GameOver = False
    GameExit = False
    while not GameExit:
        
        screen.fill(white)
        screen.blit(infoimg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameExit = True
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, red, (posx, 50 + boxsize // 2 + 5), radius)
                else:
                    pygame.draw.circle(screen, yellow, (posx, 50 + boxsize // 2), radius)
                draw_board(board)
                rect = pygame.Rect((0,50,width,70))
                pygame.display.update(rect)

            #click = pygame.mouse.get_pressed()
            #if click[0] == 1 :
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if turn == 0:  # ask player 1's input
                    player(board, p1)
                    win, start, end = winning_move(board, p1)
                    if win == True:
                        pygame.mixer.music.load('win.mp3')
                        pygame.mixer.music.play()
                        display_text('Player 1 wins !', red, 55, width // 2, 50 + 30)
                        time = pygame.time.get_ticks()
                        GameOver = True

                    if tie_move(board):
                        pygame.mixer.music.load('draw.mp3')
                        pygame.mixer.music.play()
                        display_text('Game Draw', light_green, 55, width // 2, 50 + 30)
                        time = pygame.time.get_ticks()
                        GameOver = True

                else:  # ask player 2's input
                    player(board, p2)
                    win, start, end = winning_move(board, p2)
                    if win == True:
                        pygame.mixer.music.load('win.mp3')
                        pygame.mixer.music.play()
                        display_text('Player 2 wins !', (255, 200, 15), 55, width // 2, 50 + 30)
                        time = pygame.time.get_ticks()
                        GameOver = True

                    if tie_move(board):
                        pygame.mixer.music.load('draw.mp3')
                        pygame.mixer.music.play()
                        display_text('Game Draw', light_green, 55, width // 2, 50 + 30)
                        time = pygame.time.get_ticks()
                        GameOver = True

                # print(np.flip(board, 0))
                draw_board(board)
                pygame.draw.line(screen, pista, start, end, 3)
                pygame.display.update()

        while GameOver == True:
            #pygame.time.wait(2000)
            
            if pygame.time.get_ticks() - time >= 1500:
                pygame.draw.rect(screen, cream, (150, 130, 210, 270))
                button('Play Again', 170, 190, 170, 50, orange, gold, command='again')
                button('Main Menu', 170, 290, 170, 50, orange, gold, command='main')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameExit = True
                    GameOver == False
                    pygame.quit()
                    quit()
                '''
                    if event.key == pygame.K_UP:
                        pygame.draw.rect(screen, black, (170, 190, 170, 50),3,border_radius=2)
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                two_players()
                    if event.key == pygame.K_DOWN:
                        pygame.draw.rect(screen, black, (170, 290, 170, 50),3)
                        if event.key == pygame.K_RETURN:
                            game_intro()
                            
                '''
            pygame.display.update()


def game_intro():

##    import os
##    filepath = os.path.abspath(__file__)
##    filedir = os.path.dirname(filepath)
##    musicpath = os.path.join(filedir, "bgm.mp3")
##    pygame.mixer.music.load(musicpath)
    
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        screen.fill(cream)
        screen.blit(welcomeimg, position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        button('One Player', 160, 240, 170, 50, green, light_green, command='1player')
        button('Two Players', 160, 320, 170, 50, green, light_green, command='2player')
        button('Exit', 160, 400, 170, 50, red, (200, 0, 0), command='quit')

        pygame.display.update()


game_intro()


