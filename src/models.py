from typing import (Union, List, Optional, Awaitable, Tuple)
from pydantic import BaseModel
from abc import ABC


class Order(ABC):
    orderHash: str
    makerAsset: str
    takerAsset: str
    exchangeRate: Union[float, str]


class LinchOrder(BaseModel, Order):
    orderHash: str
    makerAsset: str
    takerAsset: str
    makingAmount: int
    takingAmount: int
    exchangeRate: Union[float, str]
