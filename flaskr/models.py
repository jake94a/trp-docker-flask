import json
from .config import db

# I tried to do a Django-style "choices" for Pet.species
# It did not work the way I expected, thus I elected to
#   check the species in /submit and /edit
#
# import enum
# from sqlalchemy_utils.types.choice import ChoiceType
# class PetSpecies(enum.Enum):
#     dog = "dog"
#     cat = "cat"


class Pet(db.Model):
    """
    Pet is a SQLAlchemy db object
    ID is auto-generated
    name and species are strings
    TABLED TODO:
        - species should only allow ['dog', 'cat']
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)

    def to_json(self) -> str:
        """
        Encode a Pet object to JSON
        """
        return json.dumps({"id": self.id, "name": self.name, "species": self.species})

    def __repr__(self):
        """
        built-in representation for when a Pet object is printed
        """
        return f"<Pet - ID {self.id}: {self.name}, a {self.species}>"
