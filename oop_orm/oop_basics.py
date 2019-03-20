class Animal:
    num_animals = 0
    def __init__(self, num_legs, type_of_animal, speed, name):
        self.health = 100
        self.stamina = 10
        self.agility = 5
        self.num_legs = num_legs
        self.type = type_of_animal
        self.speed = speed
        self.name = name
        Animal.num_animals += 1

    def work_out(self, health):
        self.health += health
        return self

    def display(self):
        print(f"Hi my name is {self.name} and I have {self.health} health.")
        return self

gary = Animal(0, "snail", 5, "Gary")
shelly = Animal(4, "dog", 60, "Shelly")
print("this is the print", gary.work_out(50))
gary.work_out(50).display().work_out(10).display()

gary.favorite_food = "Sushi"
print(gary.favorite_food)
print(Animal.num_animals)
