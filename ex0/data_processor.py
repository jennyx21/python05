from typing import Any
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
    def output(self) -> tuple[int, str]:
        ... 

class NumericProcessor(DataProcessor):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.data:list[str] = []
    def validate(self, data: Any):
        if isinstance(data, (int, float)):
            return True
        elif isinstance (data, list)and all(isinstance(x, (int, float)) for x in data):
            return True
        else: 
            return False
        
    def ingest(self, data: int | float | list[int| float]):
        if isinstance(data, list):
            self.data += [str(x) for x in data]
        else:
            self.data.append(str(data))

class TextProcessor(DataProcessor):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.data: str = ""
    def validate(self, data: Any):
        if isinstance(data, str):
            return True
        else: 
            return False
        
    def ingest(self, data: str):
        if isinstance(data, str):
            self.data = data 

class LogProcessor(DataProcessor):
    def __init__(self,name) -> None:
        super().__init__(name)
        self.data: dict  = {}
    def validate(self, data: Any):
        if isinstance(data, dict):
            return True
        else: 
            return False
        
    def ingest(self, data: dict):
        if isinstance(data, dict):
            self.data = data 