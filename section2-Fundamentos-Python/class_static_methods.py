class Person:
    #atributo de clase (general)
    specie = "humano"
    #constructor
    def __init__(self, name, age):
        #atributos de instancia
        self.name=name
        self.age=age  
        
    #método para cambiar la especie a nivel instancia
    def change_species(self, new_specie):
        self.specie = new_specie
    
    #método para cambiar la especie a nivel clase, osea, todos las instancias que cree
    #despues de ejecutar el metodo
    @classmethod
    def change_species_class(cls, new_specie):
        cls.specie = new_specie  
    
    #método al que puedes acceder a nivel de clase o de instancia    
    @staticmethod
    def is_older(age):
        return age >=18
        
person1 = Person("Ricardo", 39)
person2 = Person("Juan", 50)
print(person1.specie)
print(person2.specie)

'''
#Cambio la especie a nivel instancia
person1.change_species("Reptiliano")
print(person1.specie)
print(person2.specie)
'''
#cambio specie a nivel clase:
Person.change_species_class("Humanoide")
print(person1.specie)
print(person2.specie)

print(Person.is_older(29))
print(person1.is_older(30))
print(Person.is_older(person1.age))
print(person1.is_older(person1.age))