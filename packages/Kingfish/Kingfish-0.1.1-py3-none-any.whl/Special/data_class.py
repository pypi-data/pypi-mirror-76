from dataclasses import dataclass

@dataclass
class Contact:
    name: str
    email: str
    phone: str

@dataclass
class Car:
    manufacturer: str
    model: str
    year: int
    color: str

"""Example:"""
"""contact = Contact("test","test@test.com","00 00 00 00")"""