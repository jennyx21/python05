import typing
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self, name) -> None:
        self.name = name
    
    @abstractmethod
    def validate(self, data: Any)-> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    @classmethod
    def output(input) -> tuple[int, str]:
        ... 

class NumericProcessor(DataProcessor):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.data:list[str] = []
    def validate(self, data: Any):
        if isinstance(data, (int, float)):
            return True
        elif isinstance (data, list[int, float]):
            return True
        else: 
            return False
        
    def ingest(self, data: int | float | list[int| float]):
        if isinstance(data, list):
            self.data += [str(x) for x in data]
        else:
            self.data.append(str(data))

class TextProcessor(DataProcessor):
    def __init__(self) -> None:


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
