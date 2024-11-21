from __future__ import annotations

from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name: str) -> None:
        self.protected_name = '_' + name

    def __get__(self, obj, objtype) -> int | str:
        value = getattr(obj, self.protected_name)
        return value

    def __set__(self, obj, value) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if value not in range(self.min_value, self.max_value + 1):
            raise ValueError(f"Quantity should not be less than {self.min_value} and greater than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: list) -> None:
        self.options = options

    def validate(self, value: any) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    def __init__(self,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 buns: int,
                 sauce: str) -> None:

        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.buns = buns
        self.sauce = sauce

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0,2)
    sauce = OneOf(["ketchup", "mayo", "burger"])
