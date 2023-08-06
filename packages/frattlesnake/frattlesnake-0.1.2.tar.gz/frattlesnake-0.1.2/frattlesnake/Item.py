from statistics import mean
from typing import Any, Dict, List, Optional, Union, TypeVar
from functools import cached_property

from .kolmafia import km
from .Range import Range
from .Modifier import Modifier
from .Effect import Effect

T = TypeVar("T")

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

    def __int__(self) -> int:
        return self.id

    def __hash__(self) -> int:
        return hash(self.id)
        
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Item(id={self.id},name={self.name})"

    def __eq__(self, other: Any) -> bool:
        if (isinstance(other, Item)):
            return self.id == other.id

        return self == other

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
    def tradeable(self) -> bool:
        return km.ItemDatabase.isTradeable(self.id)

    @cached_property
    def notes(self) -> str:
        return km.ConsumablesDatabase.getNotes(self.name) or ""

    @cached_property
    def virtual(self) -> bool:
        return km.ItemDatabase.isVirtualItem(self.id)

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

    @cached_property
    def single_equip(self) -> bool:
        return Modifier.SingleEquip in self.modifiers

    @property
    def modifiers(self) -> Dict[Modifier, Any]:
        modifiers = {}
        java_modifiers = km.Modifiers.getItemModifiers(self.id)
        
        if java_modifiers is not None:
            java_modifiers_list = java_modifiers.getString(km.Modifiers.MODIFIERS)
            iterator = km.Modifiers.evaluateModifiers("Item", java_modifiers_list).iterator()

            while iterator.hasNext():
                java_modifier = iterator.next()

                name = java_modifier.getName()

                if name == "none":
                    continue

                m_type = Modifier(name)

                modifiers[m_type] = m_type.parse_value(java_modifier.getValue())

        return modifiers

    @property
    def effect(self) -> Optional[Effect]:
        return self.modifiers.get(Modifier.Effect)

    def modifier(self, key: Modifier, default: T = None) -> T:
        return self.modifiers.get(key, default)

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

    def price(self, historical=False, quantity=1) -> Optional[int]:
        if historical:
            return km.MallPriceDatabase.getPrice(self.id) * quantity

        ar = km.AdventureResult.tallyItem(self.name, quantity, True)
        results = km.StoreManager.searchMall(ar)

        if results.size() == 0:
            return None

        remaining = quantity
        cost = 0

        for i in range(results.size()):
            result = results.get(i)
            available = result.quantity if result.limit == 0 else min(result.quantity, result.limit)

            to_buy = min(available, remaining)
            cost += to_buy * result.price
            remaining -= to_buy

            if remaining <= 0:
                break

        if remaining > 0:
            return None

        return cost