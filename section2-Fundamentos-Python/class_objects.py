class Person:
    #constructor
    def __init__(self, name, age):
        #atributos de instancia
        self.name=name
        self.age=age
    
    #metodo
    def work(self):
        return f"{self.name} está trabajando duro."
    
    #Instancio la clase o creo un objeto
person1 = Person("Ricardo", 39)
person2 = Person("Juan", 50)

print(person1.name)
print(person2.name)
print(person1.work())