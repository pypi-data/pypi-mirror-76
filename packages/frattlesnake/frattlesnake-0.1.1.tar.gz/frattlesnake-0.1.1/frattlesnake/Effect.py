from functools import cached_property
from typing import List, Union
from enum import Enum

from .kolmafia import km
from .Modifier import Modifier

class Quality(Enum):
    Good = 0
    Neutral = 1
    Bad = 2


class Effect:
    id: int

    def __init__(self, key: Union[str, int]):
        if isinstance(key, str):
            key = int(km.EffectDatabase.getEffectId(key))

        self.id = key

    @cached_property
    def name(self) -> str:
        return km.EffectDatabase.getEffectName(self.id)

    @cached_property
    def image(self) -> str:
        return km.EffectDatabase.getImageName(self.id)

    @cached_property
    def description(self) -> str:
        return km.EffectDatabase.getDescriptionId(self.id)

    @cached_property
    def quality(self) -> Quality:
        quality = km.EffectDatabase.getQuality(self.id)
        return Quality(quality)

    @property
    def modifiers(self) -> List[Modifier]:
        java_modifiers = km.Modifiers.getEffectModifiers(self.id)
        
        if java_modifiers is None:
            return []

        java_modifiers_list = java_modifiers.getString(km.Modifiers.MODIFIERS)
        iterator = km.Modifiers.evaluateModifiers("Effect", java_modifiers_list).iterator()

        modifiers = []

        while iterator.hasNext():
            java_modifier = iterator.next()

            name = java_modifier.getName()

            if name == "none" or name == "":
                continue

            modifier = Modifier(name, java_modifier.getValue())
            modifiers.append(modifier)

        return modifiers

