def big_function(*arg, **kargs):
    print(arg)
    print(kargs)
    return 4*arg[0]+3*arg[1]

big_function(1,2,3, hola=5, chau=6)
print(big_function(1,2,3, hola=5, chau=6))