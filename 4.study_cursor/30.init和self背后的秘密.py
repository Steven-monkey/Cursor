class Dog:
    species = '犬科动物'

    def __init__(self, name, age):
        self.species = "狗子"
        self.name = name
        self.age = age


dog1 = Dog('旺财', 5)
# print(dog1.name, dog1.age)
print(Dog.species)
