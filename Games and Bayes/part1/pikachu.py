#
# pikachu.py : Play the game of Pikachu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, March 2021
#
import sys
import time
import copy
import math

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

# all possible moves of white pichu along with the attacking moves
def pichu_move_w(board,N):
    fringe = []
    for i in range(N,N*(N-1)):
        # white pichu moving forward
        if board[i] == 'w' and board[i+N] == '.':
            boardc = list(copy.deepcopy(board))
            # white pichu becomes pikachu if it jumps to last row
            if i+N in [j for j in range(N*(N-1),N*N)]:
                boardc[i+N] = 'W'
            else:
                boardc[i+N] = 'w'
            boardc[i] ='.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # white pichu moving left
        if board[i] == 'w' and board[i-1] == '.' and i not in [j for j in range(0,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i-1] = 'w'
            boardc[i] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # white pichu moving right
        if board[i] == 'w' and board[i+1] == '.' and i not in [j for j in range(N-1,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i+1] = 'w'
            boardc[i] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # white pichu moving two steps forward by killing the black
        if i not in [j for j in range(N*(N-2),N*N)]:
            if board[i] == 'w' and (board[i+N] == 'b' or board[i+N] == 'B')  and board[i + 2*N] == '.':
                boardc = list(copy.deepcopy(board))
                # white pichu becomes pikachu if it jumps to last row
                if i+2*N in [j for j in range(N*(N-1), N*N)]:
                    boardc[i+2*N] = 'W'
                else:
                    boardc[i+2*N] = 'w'
                boardc[i] = '.'
                boardc[i+N] = '.'
                boardc = "".join(boardc)
                fringe.append(boardc)
        # white pichu moving two steps left by killing the black
        if board[i] == 'w' and (board[i-1] == 'b' or board[i-1] == 'B')  and board[i-2] == '.' and i not in [j for j in range(0,N*N,N)] and i not in [k for k in range(1,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i-2] = 'w'
            boardc[i] = '.'
            boardc[i-1] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # white pichu moving two steps right by killing the black
        if board[i] == 'w' and (board[i+1] == 'b' or board[i+1]=='B') and board[i+2] == '.' and i not in [j for j in range(N-1,N*N,N)] and i not in [k for k in range(N-2,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i+2] = 'w'
            boardc[i] = '.'
            boardc[i+1] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
    return fringe

# all possible moves of black pichu along with the attacking moves
def pichu_move_b(board,N):
    fringe = []
    for i in range(N*(N-1)-1,N-1,-1):
        # black pichu moving forward
        if board[i] == 'b' and board[i-N] == '.':
            boardc = list(copy.deepcopy(board))
            # black pichu becomes pikachu if it jumps to first row
            if i-N in [j for j in range(0,N)]:
                boardc[i-N] = 'B'
            else:
                boardc[i-N] = 'b'
            boardc[i] ='.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # black pichu moving left
        if board[i] == 'b' and board[i-1] == '.' and i not in [j for j in range(0,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i-1] = 'b'
            boardc[i] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # black pichu moving right
        if board[i] == 'b' and board[i+1] == '.' and i not in [j for j in range(N-1,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i+1] = 'b'
            boardc[i] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # black pichu moving two steps forward by killing the white
        if i not in [j for j in range(0,2*N)]:
            if board[i] == 'b' and (board[i-N] == 'w' or board[i-N] == 'W')and board[i-2*N] == '.':
                boardc = list(copy.deepcopy(board))
                # black pichu becomes pikachu if it jumps to first row
                if i-2*N in [j for j in range(0, N)]:
                    boardc[i-2*N] = 'B'
                else:
                    boardc[i-2*N] = 'b'
                boardc[i] = '.'
                boardc[i-N] = '.'
                boardc = "".join(boardc)
                fringe.append(boardc)
        # black pichu moving two steps left by killing the white
        if board[i] == 'b' and (board[i-1] == 'w' or board[i-1] == 'W') and board[i-2] == '.' and i not in [j for j in range(0,N*N,N)] and i not in [k for k in range(1,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i-2] = 'b'
            boardc[i] = '.'
            boardc[i-1] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
        # black pichu moving two steps right by killing the white
        if board[i] == 'b' and (board[i+1] == 'w' or board[i+1] == 'W') and board[i+2] == '.' and i not in [j for j in range(N-1,N*N,N)] and i not in [k for k in range(N-2,N*N,N)]:
            boardc = list(copy.deepcopy(board))
            boardc[i+2] = 'b'
            boardc[i] = '.'
            boardc[i+1] = '.'
            boardc = "".join(boardc)
            fringe.append(boardc)
    return fringe

# all possible moves of white pikachu along with the attacking moves
def pikachu_move_w(board,N):
    fringe = []
    for i in range(0,N*N):
        # white pikachu moving forwards
        if i not in [j for j in range(N*(N-1),N*N)] and board[i]=='W':
            for k in range(i+N,N*N,N):
                if board[k] !='.': break
                if board[k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[k] = 'W'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # white pikachu moving backwards
        if i not in [j for j in range(0,N)] and board[i]=='W':
            for k in range(i-N,-1,-N):
                if board[k] != '.': break
                if board[k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[k] = 'W'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # white pikachu moving left
        if i not in [j for j in range(0,N*N,N)] and board[i]=='W':
            m = min(j for j in range(i,0,-N)if j > 0)
            for k in range(1,m+1):
                if board[i-k] != '.': break
                if board[i-k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[i-k] = 'W'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # white pikachu moving right
        if i not in [j for j in range(N-1,N*N,N)] and board[i]=='W':
            m= max(j-i for j in range(N-1,N*N,N)if j-i<N)
            for k in range(1,m+1):
                if board[i+k] != '.': break
                if board[i+k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[i+k] = 'W'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # white pikachu moving forwards and jumping above black by killing it
        if i not in [j for j in range(N*(N-2),N*N)] and board[i]=='W':
            for k in range(i+N,N*N,N):
                if board[k] == 'w' or board[k] == 'W': break
                elif board[k]  =='.': continue
                elif board[k] =='b' or board[k] == 'B':
                    for m in range(k+N,N*N,N):
                         if board[m] != '.': break
                         elif board[m] == '.':
                            boardc = list(copy.deepcopy(board))
                            boardc[m] = 'W'
                            boardc[i] ='.'
                            boardc[k] ='.'
                            boardc = "".join(boardc)
                            fringe.append(boardc)
                    break
        # white pikachu moving backwards and jumping above black by killing it
        if i not in [j for j in range(0,2*N)] and board[i]=='W':
            for k in range(i-N,-1,-N):
                if board[k] == 'w' or board[k] == 'W': break
                elif board[k]  =='.': continue
                elif board[k] =='b' or board[k] == 'B':
                    for m in range(k-N,-1,-N):
                         if board[m] != '.': break
                         if board[m] == '.':
                            boardc = list(copy.deepcopy(board))
                            boardc[m] = 'W'
                            boardc[i] ='.'
                            boardc[k] ='.'
                            boardc = "".join(boardc)
                            fringe.append(boardc)
                    break
        # white pikachu moving left and jumping above black by killing it
        if i not in [j for j in range(0,N*N,N)] and i not in [j for j in range(1,N*N,N)] and board[i]=='W':
                m = min(j for j in range(i, 0, -N) if j > 0)
                for k in range(1, m + 1):
                    if board[i - k] == 'w' or board[i - k] == 'W':break
                    elif board[i - k] == '.':continue
                    elif board[i - k] == 'b' or board[i - k] == 'B':
                        for l in range(k + 1, m + 1):
                            if board[i - l] != '.': break
                            if board[i - l] == '.':
                                boardc = list(copy.deepcopy(board))
                                boardc[i - l] = 'W'
                                boardc[i] = '.'
                                boardc[i - k] = '.'
                                boardc = "".join(boardc)
                                fringe.append(boardc)
                        break
        # white pikachu moving right and jumping above black by killing it
        if i not in [j for j in range(N-1,N*N,N)] and i not in [j for j in range(N-2,N*N,N)] and board[i]=='W':
                m= max(j-i for j in range(N-1,N*N,N)if j-i<N)
                for k in range(1,m+1):
                    if board[i+k] == 'w' or board[i+k] == 'W':break
                    elif board[i+k] == '.':continue
                    elif board[i+k] == 'b' or board[i+k] == 'B':
                        for l in range(k+1, m+1):
                            if board[i+l] != '.': break
                            if board[i+l] == '.':
                                boardc = list(copy.deepcopy(board))
                                boardc[i+l] = 'W'
                                boardc[i] = '.'
                                boardc[i+k] = '.'
                                boardc = "".join(boardc)
                                fringe.append(boardc)
                        break

    return fringe

# all possible moves of black pikachu along with the attacking moves
def pikachu_move_b(board,N):
    fringe = []
    for i in range(0,N*N):
        # black pikachu moving backward
        if i not in [j for j in range(N*(N-1),N*N)] and board[i]=='B':
            for k in range(i+N,N*N,N):
                if board[k] !='.': break
                if board[k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[k] = 'B'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # black pikachu moving forward
        if i not in [j for j in range(0,N)] and board[i]=='B':
            for k in range(i-N,-1,-N):
                if board[k] != '.': break
                if board[k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[k] = 'B'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # black pikachu moving left
        if i not in [j for j in range(0,N*N,N)] and board[i]=='B':
            m = min(j for j in range(i,0,-N)if j > 0)
            for k in range(1,m+1):
                if board[i-k] != '.': break
                if board[i-k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[i-k] = 'B'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # black pikachu moving right
        if i not in [j for j in range(N-1,N*N,N)] and board[i]=='B':
            m= max(j-i for j in range(N-1,N*N,N)if j-i<N)
            for k in range(1,m+1):
                if board[i+k] != '.': break
                if board[i+k] == '.':
                    boardc = list(copy.deepcopy(board))
                    boardc[i+k] = 'B'
                    boardc[i] ='.'
                    boardc = "".join(boardc)
                    fringe.append(boardc)
        # black pikachu moving backward and jumping above white by killing it
        if i not in [j for j in range(N*(N-2),N*N)] and board[i]=='B':
            for k in range(i+N,N*N,N):
                if board[k] == 'b' or board[k] == 'B': break
                elif board[k]  =='.': continue
                elif board[k] =='w' or board[k] == 'W':
                    for m in range(k+N,N*N,N):
                         if board[m] != '.': break
                         elif board[m] == '.':
                            boardc = list(copy.deepcopy(board))
                            boardc[m] = 'B'
                            boardc[i] ='.'
                            boardc[k] ='.'
                            boardc = "".join(boardc)
                            fringe.append(boardc)
                    break
        # black pikachu moving forward and jumping above white by killing it
        if i not in [j for j in range(0,2*N)] and board[i]=='B':
            for k in range(i-N,-1,-N):
                if board[k] == 'b' or board[k] == 'B': break
                elif board[k]  =='.': continue
                elif board[k] =='w' or board[k] == 'W':
                    for m in range(k-N,-1,-N):
                         if board[m] != '.': break
                         if board[m] == '.':
                            boardc = list(copy.deepcopy(board))
                            boardc[m] = 'B'
                            boardc[i] ='.'
                            boardc[k] ='.'
                            boardc = "".join(boardc)
                            fringe.append(boardc)
                    break
        # black pikachu moving left and jumping above white by killing it
        if i not in [j for j in range(0,N*N,N)] and i not in [j for j in range(1,N*N,N)] and board[i]=='B':
                m = min(j for j in range(i, 0, -N) if j > 0)
                for k in range(1, m+1):
                    if board[i-k] == 'b' or board[i-k] == 'B':break
                    elif board[i - k] == '.':continue
                    elif board[i - k] == 'w' or board[i - k] == 'W':
                        for l in range(k + 1, m + 1):
                            if board[i - l] != '.': break
                            if board[i - l] == '.':
                                boardc = list(copy.deepcopy(board))
                                boardc[i - l] = 'B'
                                boardc[i] = '.'
                                boardc[i - k] = '.'
                                boardc = "".join(boardc)
                                fringe.append(boardc)
                        break
        # black pikachu moving right and jumping above white by killing it
        if i not in [j for j in range(N-1,N*N,N)] and i not in [j for j in range(N-2,N*N,N)] and board[i]=='B':
                m= max(j-i for j in range(N-1,N*N,N)if j-i<N)
                for k in range(1,m+1):
                    if board[i+k] == 'b' or board[i+k] == 'B':break
                    elif board[i+k] == '.':continue
                    elif board[i+k] == 'w' or board[i+k] == 'W':
                        for l in range(k+1, m+1):
                            if board[i+l] != '.': break
                            if board[i+l] == '.':
                                boardc = list(copy.deepcopy(board))
                                boardc[i+l] = 'B'
                                boardc[i] = '.'
                                boardc[i+k] = '.'
                                boardc = "".join(boardc)
                                fringe.append(boardc)
                        break

    return fringe

# evaluation function for a calculating the utility of a particlar board configuration
def evaluation_function(board,max_player):
    num_pichu_w=0
    num_pichu_b=0
    num_pikachu_w=0
    num_pikachu_b=0
    num_pichu_b_adv=0
    num_pichu_w_adv =0
    N = int(math.sqrt(len(board)))

    # for calculating the number of white and black pichus and pikachus on the board
    for i in board:
        if i == 'w':
            num_pichu_w += 1
        elif i== 'b':
            num_pichu_b += 1
        elif i == 'W':
            num_pikachu_w += 1
        elif i == 'B':
            num_pikachu_b += 1
    # for calculating the number of white and black pieces of pichu on the opponents half i.e white on N-1 and N-2 row and black on 1 and 2 row
    for j in board[N:3*N]:
        if j == 'b':
            num_pichu_b_adv += 1
    for j in board[N*(N-3):N*(N-1)]:
        if j == 'w':
            num_pichu_w_adv += 1
    # calculating the mobility of white and black pieces
    num_mob_w = len(pichu_move_w(board,N))+len(pikachu_move_w(board,N))
    num_mob_b = len(pichu_move_b(board,N))+len(pikachu_move_b(board,N))

    if max_player == 'w':
        return 5*(num_pichu_w-num_pichu_b)+25*(num_pikachu_w-num_pikachu_b)+10*(num_pichu_w_adv-num_pichu_b_adv)+0.5*(num_mob_w-num_mob_b)
    elif max_player == 'b':
        return 5*(num_pichu_b-num_pichu_w)+25*(num_pikachu_b-num_pikachu_w)+10*(num_pichu_b_adv-num_pichu_w_adv)+0.5*(num_mob_b-num_mob_w)

def terminal_state(board,max_player):
    num_pichu_w=0
    num_pichu_b=0
    num_pikachu_w=0
    num_pikachu_b=0

    # for calculating the number of white and black pichus and pikachus on the board
    for i in board:
        if i == 'w':
            num_pichu_w += 1
        elif i== 'b':
            num_pichu_b += 1
        elif i == 'W':
            num_pikachu_w += 1
        elif i == 'B':
            num_pikachu_b += 1
    if (num_pichu_b+num_pikachu_b) == 0 and max_player == 'w':
        return True
    elif (num_pichu_w+num_pikachu_w) == 0 and max_player == 'b':
        return True
    else:
        return False

def successors(board, player):
    N=int(math.sqrt(len(board)))
    if player == 'w':
        return pichu_move_w(board,N)+pikachu_move_w(board,N)
    elif player == 'b':
        return pichu_move_b(board,N)+pikachu_move_b(board,N)

def min_method(board, max_player, min_player, alpha, beta, depth):
    best_move = None
    min_val = float('inf')

    if depth == 0 or terminal_state(board, max_player):
        return board, evaluation_function(board, max_player)

    else:
        for s in successors(board, min_player):
            v = max_method(s, max_player, min_player, alpha, beta, depth - 1)[1]

            v = min(v,min_val)

            if v <= alpha:
                return (board, v)
            beta = min(beta,v)
            new_board =s
    return (new_board,v)

def max_method(board, max_player, min_player, alpha, beta, depth):
    best_move = None
    max_val = float('-inf')

    if depth == 0 or terminal_state(board, max_player):
        return (board, evaluation_function(board, min_player))

    else:
        for s in successors(board, max_player):
            v = min_method(s, max_player, min_player, alpha, beta, depth - 1)[1]

            v = max(v,max_val)

            if v >= beta:
                return (board,v)

            alpha = max(alpha,v)
            newboard = s
        return (newboard,v)



    return (best_move, max_val)


def alpha_beta_result(board, max_player, min_player, depth):
    alpha = float('-inf')
    beta = float('inf')
    max_val = float('-inf')
    best_move = None

    moves = []

    for s in successors(board, max_player):
        v = min_method(s, max_player, min_player, alpha, beta, depth)[1]
        if v > max_val:
            max_val = v
            best_move = s

    return best_move

def find_best_move(board,player, timelimit,depth):
    if player == "b":
        max_player = "b"
        min_player = "w"
    else:
        max_player = "w"
        min_player = "b"

    best_config = alpha_beta_result(board, max_player, min_player, depth)
    return best_config



if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: pikachu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")
    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for i in range(2,11):
        depth = i
        new_board = find_best_move(board,player,timelimit,depth)
        print("Best move for "+player+" till depth: "+str(i))
        print(new_board)
