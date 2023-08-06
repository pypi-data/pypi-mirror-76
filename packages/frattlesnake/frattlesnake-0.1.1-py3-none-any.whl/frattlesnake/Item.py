from statistics import mean
from typing import List, Optional, Union
from functools import cached_property

from .kolmafia import km
from .Range import Range
from .Modifier import Modifier, ModifierType
from .Effect import Effect

class Item:
    id: int

    def __init__(self, key: Union[str, int]):
        if isinstance(key, str):
            key = int(km.ItemDatabase.getItemId(key))

        if key == -1 or km.ItemDatabase.getItemDataName(key) is None:
            raise NameError(f"Item {key} not found")

        self.id = key

    @staticmethod
    def all() -> List["Item"]:
        items = []

        for i in range(1, km.ItemDatabase.maxItemId()):
            try:
                item = Item(i)
                items.append(item)
            except NameError: ...

        return items

    @cached_property
    def name(self) -> str:
        return km.ItemDatabase.getDisplayName(self.id)

    @cached_property
    def description(self) -> str:
        return km.ItemDatabase.getDescriptionId(self.id)

    @cached_property
    def image(self) -> str:
        return km.ItemDatabase.getImage(self.id)

    @cached_property
    def inebriety(self) -> Optional[int]:
        return km.ConsumablesDatabase.getRawInebriety(self.name)

    @cached_property
    def fullness(self) -> Optional[int]:
        return km.ConsumablesDatabase.getRawFullness(self.name)

    @cached_property
    def spleen_hit(self) -> Optional[int]:
        return km.ConsumablesDatabase.getRawSpleenHit(self.name)

    @cached_property
    def adventure_range(self) -> Optional[Range]:
        range = km.ConsumablesDatabase.getAdvRangeByName(self.name).strip()

        if range is None or range == "0" or range == "":
            return None

        return Range.from_string(range)

    @cached_property
    def adventures(self) -> Optional[float]:
        if self.adventure_range:
            return mean(self.adventure_range)            

    @property
    def modifiers(self) -> List[Modifier]:
        java_modifiers = km.Modifiers.getItemModifiers(self.id)
        
        if java_modifiers is None:
            return []

        java_modifiers_list = java_modifiers.getString(km.Modifiers.MODIFIERS)
        iterator = km.Modifiers.evaluateModifiers("Item", java_modifiers_list).iterator()

        modifiers = []

        while iterator.hasNext():
            java_modifier = iterator.next()

            name = java_modifier.getName()

            if name == "none":
                continue

            modifier = Modifier(name, java_modifier.getValue())
            modifiers.append(modifier)

        return modifiers

    @property
    def effect(self) -> Optional[Effect]:
        for m in self.modifiers:
            if m.type == ModifierType.Effect:
                return Effect(m.value)

        return None

    def eat(self, quantity=1, silent=False) -> bool:
        command = "eat" + ("silent" if silent else "")
        km.KoLmafiaCLI.DEFAULT_SHELL.executeCommand(command, "{} {}".format(quantity, self.name))
        return km.UseItemRequest.lastUpdate == ""

    def drink(self, quantity=1, silent=False) -> bool:
        command = "drink" + ("silent" if silent else "")
        km.KoLmafiaCLI.DEFAULT_SHELL.executeCommand(command, "{} {}".format(quantity, self.name))
        return km.UseItemRequest.lastUpdate == ""

    def chew(self, quantity=1, silent=False) -> bool:
        command = "chew" + ("silent" if silent else "")
        km.KoLmafiaCLI.DEFAULT_SHELL.executeCommand(command, "{} {}".format(quantity, self.name))
        return km.UseItemRequest.lastUpdate == ""
