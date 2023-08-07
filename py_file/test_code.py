import mods

# mods.depth.get_depth(3,6)
# mods.move('coba')
# from urllib.request import urlopen

path_file = 'temp_img/coordinates.txt'
f = open(path_file)
coordinates=[]
for i in f.read().split(','):
    coordinates.append(i)
# print(f.read().split(',')[1])
# print(f.read().split(',')[2])
# print(f.read().split(',')[3])

