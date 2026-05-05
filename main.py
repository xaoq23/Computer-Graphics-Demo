import numpy as np
from IPython.display import clear_output
import time



#定义旋转矩阵

def rotate_z(theta):
    col1 = [np.cos(theta), np.sin(theta), 0]
    col2 = [-np.sin(theta), np.cos(theta), 0]
    col3 = [0, 0, 1]
    return np.array([col1, col2, col3]).transpose()


def rotate_y(phi):
    col1 = [np.cos(phi), 0, -np.sin(phi)]
    col2 = [0, 1, 0]
    col3 = [np.sin(phi), 0, np.cos(phi)]
    return np.array([col1, col2, col3]).transpose()


#定义网格密度
U = np.linspace(0, 2 * np.pi, 100)
V = U

#定义图形半径
r = 0.3
R = 1

#定义图形坐标
donut = np.array([[np.cos(u) * (R + r * np.cos(v)), np.sin(u) * (R + r * np.cos(v)), r * np.sin(v)] for u in U for v in V]).transpose()

#定义旋转角度
phi = 1
theta = 2
transform = rotate_z(theta) @ rotate_y(phi)
donut_r = transform @ donut


#求面上的法向量
big_ring = R*np.array([[np.cos(u), (np.sin(u)), 0] for u in U for v in V]).transpose()
normal = donut - big_ring
normal = normal/r

#求所有法向量的范数
np.linalg.norm(normal, axis=0)

#构造打印显示矩阵
radius = 1.3 * (R + r)
res_x = 36
res_y = 18

x_line = np.linspace(-radius, radius, res_x)
y_line = np.linspace(-radius, radius, res_y)
pixils = np.stack(np.meshgrid(x_line, y_line), axis=2)

pixil_len_x = x_line[1] - x_line[0] 
pixil_len_y = y_line[1] - y_line[0]

def calculate_brightness_pixil(transform):
    screen = np.zeros([res_y, res_x])
    _donut = transform @ donut
    _normal = transform @ normal
    brightness_3d = _normal[2, :] + 1
    
    def in_pixil_window(points, pixil)->bool:
        x,y = pixil
        return(x-pixil_len_x < points[1, :]) & (points[1, :] < x+pixil_len_x) & (y-pixil_len_y < points[2, :]) & (points[2, :] < y+pixil_len_y)
    
    
    for i in range(res_y):
        for j in range(res_x):    
            mask = in_pixil_window(_donut , pixils[i][j]) 
            x_vals = _donut[0, :][mask]
            screen[i][j] = brightness_3d[mask][np.argmax(x_vals)] if x_vals.size > 0 else 0
    return screen

ASCII_BRIGHTNESS=".,-~:;=!*$$##%@"

def show_donut(transform):
    screen = calculate_brightness_pixil(transform)
    scaled = np.zeros_like(screen)
    visible = screen > 0 
    if np.any(visible):
        lo = screen[visible].min()
        hi = screen[visible].max()
        scaled[visible] = (screen[visible] - lo) / (hi - lo)
    rows = []
    for row in scaled[::-1]:
        chars = []
        for value in row:
            if value <= 0:
                chars.append(" ")
            else:
                idx = min(len(ASCII_BRIGHTNESS)-1 , int(value * (len(ASCII_BRIGHTNESS)-1)))
                chars.append(ASCII_BRIGHTNESS[idx])
        rows.append("".join(chars))
    donut_frame = "\n".join(rows)
    return donut_frame


angle = 0.0
while True:
    clear_output(wait=True)
    print(show_donut(rotate_z(angle) @ rotate_y(angle / 2)))
    angle += 0.1
    time.sleep(0.05)