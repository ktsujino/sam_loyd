import sys
from collections import deque

kWall = 0
kSpace = 1
kWhite = 2
kBlack = 3

kConst2Char = {
    kWall:'X',
    kSpace:' ',
    kWhite:'W',
    kBlack:'K'
}

# 0: wall, 1: space, 2:white, 3:black
kStartState = [
    kWhite, kWhite, kWhite,  kWall,  kWall,
    kWhite, kWhite, kWhite,  kWall,  kWall,
    kWhite, kWhite, kSpace,  kBlack, kBlack,
    kWall,  kWall,  kBlack,  kBlack, kBlack,
    kWall,  kWall,  kBlack,  kBlack, kBlack,
]

kGoalState = [
    kBlack, kBlack, kBlack,  kWall,  kWall,
    kBlack, kBlack, kBlack,  kWall,  kWall,
    kBlack, kBlack, kSpace,  kWhite, kWhite,
    kWall,  kWall,  kWhite,  kWhite, kWhite,
    kWall,  kWall,  kWhite,  kWhite, kWhite,
]

def visualize_key(key):
    row = ''
    for i in range(25):
        row += kConst2Char[key%4]
        key //= 4
        if i % 5 == 4:
            print(row)
            row = ''

def state_to_key(state):
    key = 0
    for i in state:
        key *= 4
        key += i
    return key

def is_valid_pos(state, pos):
    if pos >= 0 and pos < 25 and state[pos] != kWall:
        return True
    else:
        return False

def is_in_same_row(pos1, pos2):
    if pos1//5 == pos2//5:
        return True
    else:
        return False

def gen_moves(state):
    space_pos = state.index(kSpace)
    new_pos_list = []
    # horizontal move
    for offset in [-2, -1, 1, 2]:
        new_pos = space_pos + offset
        if is_valid_pos(state, new_pos) and is_in_same_row(space_pos, new_pos):
            new_pos_list.append(new_pos)
    for offset in [-10, -5, 5, 10]:
        new_pos = space_pos + offset
        if is_valid_pos(state, new_pos):
            new_pos_list.append(new_pos)
    moves = []
    for new_pos in new_pos_list:
        new_state = list(state)
        new_state[space_pos], new_state[new_pos] = new_state[new_pos], new_state[space_pos]
        moves.append(new_state)
    return moves
        
kStartKey = state_to_key(kStartState)
kGoalKey = state_to_key(kGoalState)

q = deque()
q.append((kStartState, None, 0))
key2prev_key = {}

while q:
    state, prev_key, dist = q.popleft()
    key = state_to_key(state)
    if key in key2prev_key:
        continue
    key2prev_key[key] = prev_key
    if key == kGoalKey:
        print(dist)
        break
    for new_state in gen_moves(state):
        new_key = state_to_key(new_state)
        if new_key not in key2prev_key:
            q.append((new_state, key, dist+1))
        
# visualize states
keys = [kGoalKey]
key = kGoalKey
while key != kStartKey:
    key = key2prev_key[key]
    keys.append(key)

for key in keys[::-1]:
    print()
    visualize_key(key)

