from typing import Any
from abc import ABC, abstractmethod

list_test = ['Hello world', [3.14, -1, 2.71],
             [{'log_level': 'WARNING', 'log_message':
               'Telnet access! Use ssh instead'},
              {'log_level': 'INFO', 'log_message':
               'User wil isconnected'}], 42, ['Hi', 'five']]


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.data: list[Any] = []
        self.rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.data:
            raise IndexError
        else:
            self.rank += 1
            return (self.rank - 1, self.data.pop(0))


class NumericProcessor(DataProcessor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.data: list[str] = []

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, list) and all(isinstance(x, (int, float))
                                            for x in data):
            return True
        else:
            return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric value")
        if isinstance(data, list):
            self.data += [str(x) for x in data]
        else:
            self.data.append(str(data))


class TextProcessor(DataProcessor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.data: list[str] = []

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return True
        else:
            return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Improper str data")
        if isinstance(data, list):
            self.data += [str(x) for x in data]
        if isinstance(data, str):
            self.data.append(data)


class LogProcessor(DataProcessor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.data: list[str] = []

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return True
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            return True
        else:
            return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Improper dict data")
        if isinstance(data, dict):
            self.data.append(f"{data['log_level']}: {data['log_message']}")
        if isinstance(data, list):
            for x in data:
                self.data.append(f"{x['log_level']}: {x['log_message']}")


def test_numeric() -> None:
    print("Testing Numeric Proccessor...")
    list1: list[int] = [1, 2, 3, 4, 5]
    num: int = 42
    text: str = "hello"
    text2: str = "foo"
    processor = NumericProcessor("processor")
    i: int = 0
    print(f"Trying to validate input '{num}': ", end="")
    print(processor.validate(num))
    print(f"Trying to validate input '{text}': ", end="")
    print(processor.validate(text))
    try:
        print(f"Test invalid ingestion of string '{text2}'"
              f" without prior validation:")
        processor.ingest(text2)
    except Exception as e:
        print(f"Got exeption: {e}")
    print(f"processing data: {list1}")
    processor.ingest(list1)
    print("Extracting 3 values...")
    while i < 3:
        out: tuple[int, str] = processor.output()
        rank, value = out
        print(f"Numeric value {rank}: {value}")
        i += 1


def test_text() -> None:
    print("\nTesting Text Processor")
    list1 = ["hello", "my", "name", "is", "jenny"]
    num: int = 42
    text: str = "hello"
    processor = TextProcessor("processor")
    i: int = 0
    print(f"Trying to validate input '{num}': ", end="")
    print(processor.validate(num))
    print(f"Trying to validate input '{text}': ", end="")
    print(processor.validate(text))
    try:
        print(f"Test invalid ingestion of number '{num}'"
              f" without prior validation:")
        processor.ingest(num)
    except Exception as e:
        print(f"Got exeption: {e}")
    print(f"processing data: {list1}")
    processor.ingest(list1)
    print("Extracting 1 value...")
    while i < 1:
        out: tuple[int, str] = processor.output()
        rank, value = out
        print(f"Text value {rank}: {value}")
        i += 1


def test_log() -> None:
    print("\nTesting Log Processor")
    list1 = [{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
             {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
    text: str = "hello"
    processor = LogProcessor("processor")
    i: int = 0
    print(f"Trying to validate input '{text}': ", end="")
    print(processor.validate(text))
    print(f"processing data: {list1}")
    processor.ingest(list1)
    print("Extracting 2 value...")
    while i < 2:
        out: tuple[int, str] = processor.output()
        rank, value = out
        # log_level, log_message = value
        # log_level = value[log_level]
        # log_message = value[log_message]
        print(f"Text value {rank}: {value}")
        i += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    test_numeric()
    test_text()
    test_log()


if __name__ == "__main__":
    main()
