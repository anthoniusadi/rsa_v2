import os
import shutil


def get_depth(a,b):
    depth = abs(a-b)
    txt = f'depth_1 : {a*100:.3f}cm\ndepth_2 : {b*100:.3f}cm\nfinal_depth {depth*100:.3f}cm'
    with open('temp_img/depth.txt', 'w') as f:
        f.write(txt)
def move(name):
    path_base_result = 'result/'
    isexist = os.path.exists(name)
    if not isexist:
        os.makedirs(name)
    path_temp = 'temp_img/'
    fname = os.listdir(path_temp)
    for fn in fname:
        shutil.move(os.path.join(path_temp,fn),os.path.join(path_base_result,name))
    