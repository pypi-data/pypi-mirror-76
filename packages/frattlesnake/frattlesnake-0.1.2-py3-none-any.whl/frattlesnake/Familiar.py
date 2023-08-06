from typing import Optional, Union
from functools import cached_property

from .kolmafia import km
from .Item import Item

class Familiar:
    id: int

    def __init__(self, key: Union[str, int]):
        if isinstance(key, str):
            key = int(km.FamiliarDatabase.getFamiliarId(key))

        self.id = key

    @staticmethod
    def mine() -> Optional["Familiar"]:
        return Familiar(km.KoLCharacter.getFamiliar().getId())

    @staticmethod
    def enthroned() -> Optional["Familiar"]:
	    return Familiar(km.KoLCharacter.getEnthroned().getId())

    @staticmethod
    def bjorned() -> Optional["Familiar"]:
	    return Familiar(km.KoLCharacter.getBjorned().getId())

    @cached_property
    def race(self) -> str:
        return km.FamiliarDatabase.getFamiliarName(self.id)

    @cached_property
    def image(self) -> str:
        return km.FamiliarDatabase.getFamiliarImage(self.id)

    @cached_property
    def hatchling(self) -> Item:
        hatchling_id = km.FamiliarDatabase.getFamiliarLarva(self.id)
        hatchling = Item(hatchling_id)

        if hatchling is None:
            raise Exception(f"Hatching {hatchling_id} not recognised")

        return hatchling

    @property
    def nickname(self) -> str:
        fam = km.KoLCharacter.findFamiliar(self.id)
        return fam.getName()

    @property
    def weight(self) -> int:
        fam = km.KoLCharacter.findFamiliar(self.id)
        return fam.getWeight()

    @property
    def experience(self) -> int:
        fam = km.KoLCharacter.findFamiliar(self.id)
        return fam.getTotalExperience()

    def use(self) -> bool:
        km.KoLmafiaCLI.DEFAULT_SHELL.executeCommand("familiar", self.race)
        return True

    def have(self) -> bool:
        return km.KoLCharacter.findFamiliar(self.id) is not None