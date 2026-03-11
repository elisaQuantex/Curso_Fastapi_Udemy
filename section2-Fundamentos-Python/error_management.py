def divide_numbers():
    try:
        a=int(input("Ingresa el numerador:"))
        b=int(input("Ingresa el denominador:"))
        result=a/b
    except ZeroDivisionError:
        print("No se puede dividir por cero.") #El mensaje ZeroDivisionError lo podemos copiar del mensaje que
                                              #  arroja el codigo cuando tratamos de dividir por cero y 
                                              # solo tenemos puesto el
                                              # except Exception as error:
                                              #     print(type(error))
    except ValueError:                        #El mensaje ValueError lo podemos copiar del mensaje que
         print("Ingresa solo números.")       #  arroja el codigo cuando tratamos de dividir por cero y 
                                              # solo tenemos puesto el
                                              # except Exception as error:
                                              #     print(type(error))
        
    except Exception as error:
        print(type(error))
    else:                                    #Este print y return se puede poner acá o dentro del try, es lo mismo.
        print(result)                        # Lo pusimos acá para ver que siempre que funcione todo ok en el try
        return result                        #luego pasa por el else. Digamos, que si no entró en ningun except, pasa
                                             #por el else. Se puede poner todo en try y acá pass.                       
    
    finally:                                 #Siempre entra en finally. Se puede poner pass. 
        print("Gracias por usar la calculadora.")

divide_numbers()