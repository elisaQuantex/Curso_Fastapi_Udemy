class Person:
    #atributo de clase (general)
    specie = "humano"
    #constructor
    def __init__(self, name, age):
        #atributos de instancia
        self.name=name
        self.age=age
        #atributo protegido. Se puede ver,
        #pero es una forma de mostrar que se debe proteger o tener cuidado.
        # La idea es que se llame a traves de un metodo y no directamente.
        #Puede ser un método protegido tambien
        self._energy = 100
        #atributo privado
        self.__password = "1234"
    
    #metodo
    def work(self):
        return f"{self.name} está trabajando duro."
    
    #metodo protegido
    def _waste_energy(self, quantity):
        self._energy -= quantity 
        return self._energy
    
    #método privado
    def __generate_password(self):
        return f"$${self.name}{self.age}$$"    
    
#Instancio la clase o creo un objeto
person1 = Person("Ricardo", 39)
person2 = Person("Juan", 50)

print(person1.specie)
print(person1.name)
print(person2._energy)
print(person1.work())
print(person1._waste_energy(10))
#Esta es la forma de acceder al atributo privado:
print(person2._Person__password)
#De la forma habitual da error para "Protegerlo"
# y que el programador se de cuenta de que no es 
#recomendado tocarla.
#print(person2.__password)
print(person1._Person__generate_password())