try:
    with open('test.txt', mode="w") as my_file:   #EL modo escritura, si el archivo no existe, lo crea.
        text = my_file.write(":)")
    with open('test.txt', mode="r") as my_file:
        print(my_file.readlines())
    with open('test.txt', mode="r+") as my_file:  #lectura y escritura
        print(my_file.readlines())
        text = my_file.write("Hola mundo ")
    with open('test.txt', mode="a") as my_file:   #modo append. Agrega lo que escribamos hasta el final. 
        text = my_file.write("123 ")    
        print(text)
        
except FileNotFoundError:
    print("El archivo no existe")
except Exception as err:
    print(f"Ocurrió un error: {err}")