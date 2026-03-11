# La programacióon OO tiene 4 pilares:
#1- Encapsulación
#2- Abstracción
#3- Herencia
#4- Polimorfismo

class BankAccount:
    def __init__(self, owner, initial_balance):
        self.owner = owner
        self.__balance = initial_balance #Encapsulación (atributo privado)
        
    def deposit(self, amount):
        if amount > 0:
            self.__balance +=amount  # dentro de la clase puedo acceder a los atributos privados.
    
    def withdraw(self, amount):
        if 0 < amount < self.__balance:
            self.__balance -= amount
        else:
            print("Saldo insuficiente o monto inválido.")
            
    def check_balance(self):
        return f"Saldo actual: ${self.__balance}"
    
account = BankAccount("Ricardo", 1000) #ABstracción: De forma interna no sabe como funciona. EL usuario
                                       #no sabe como se maneja su saldo. Todo es abstracto, solo se crean
                                       # metodos publicos para que el usuario pueda acceder a cierto tipo de
                                       #información.
account.deposit(500)
account.withdraw(700)
print(account.check_balance())
            
        