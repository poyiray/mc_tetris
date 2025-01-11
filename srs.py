from shape import pos
from copy import deepcopy
from basic import bottom, width, m

L_t = [[(0,0),(-1,0),(-1,-1),(0,2),(-1,2)],
       [(0,0),(1,0),(1,1),(0,-2),(1,-2)],
       [(0,0),(1,0),(1,-1),(0,2),(1,2)],
       [(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)]]

T_t = [[(0,0),(-1,0),(-1,-1),(-1,2)],
       [(0,0),(1,0),(1,1),(0,-2),(1,-2)],
       [(0,0),(1,0),(0,2),(1,2)],
       [(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)]]

S_t = [[(0,0),(-1,0),(-1,-1),(0,2),(-1,2)],
       [(0,0),(1,0),(1,1),(0,-2),(1,-2)],
       [(0,0),(1,0),(1,-1),(0,2),(1,2)],
       [(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)]]

I_r_t = [[(0,0),(-2,0),(1,0),(-2,1),(1,-2)],
         [(0,0),(-1,0),(2,0),(-1,-2),(2,1)],
         [(0,0),(2,0),(-1,0),(2,-1),(-1,2)],
         [(0,0),(1,0),(-2,0),(1,2),(-2,-1)]]

I_l_t= [[(0,0),(-1,0),(2,0),(-1,-2),(2,1)],
        [(0,0),(2,0),(-1,0),(2,-1),(-1,2)],
        [(0,0),(1,0),(-2,0),(1,2),(-2,-1)],
        [(0,0),(-2,0),(1,0),(-2,1),(1,-2)]]

def collision(x, y):
        for i in range(len(x)):
            if x[i] < 0 or x[i] >= width or y[i] >= bottom or m[y[i]][x[i]]: 
                return True
        return False

def collision_SRS(tetro, d):
    state = tetro.state
    name = tetro.name

    if name != 'I':
         state_t = (state - (d == -1) * 2) % 4
         if name == 'L' or name == 'J': a_t = L_t
         elif name == 'S' or name == 'Z': a_t = S_t
         elif name == 'T':
              a_t = T_t
              d = 1
    else:
         if d == 1: a_t = I_r_t
         else: a_t = I_l_t
         d = 1
         state_t = state

    state = (state + d) % 4

    for i in range(len(a_t[state_t])):
        x_t = []
        y_t = []
        pos_x = tetro.pos_x + a_t[state_t][i][0] * d
        pos_y = tetro.pos_y + a_t[state_t][i][1]
        for j in range(len(tetro.x)):
            x_t.append(pos_x + pos[name][state][j][0])
            y_t.append(pos_y + pos[name][state][j][1])
        if not collision(x_t, y_t):
             tetro.x = x_t
             tetro.y = y_t
             tetro.state = state
             tetro.pos_x = pos_x
             tetro.pos_y = pos_y
             return

    
