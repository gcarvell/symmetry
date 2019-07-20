gridsize = 4
a = gridsize
for b in range(1, gridsize**2+1):
    if b%gridsize == 0:
        x = gridsize-1
    else:
        x = b%gridsize-1
    print("sq number: {}, column = {}".format(b,x))