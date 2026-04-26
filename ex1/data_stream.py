import typing
from typing import Any
from abc import ABC, abstractmethod


list1 = ['Hello world', [3.14, -1, 2.71],
         [{'log_level': 'WARNING', 'log_message':
           'Telnet access! Use ssh instead'},
          {'log_level': 'INFO', 'log_message':
           'User wil isconnected'}], 42, ['Hi', 'five']]


class DataProcessor(ABC):
    def __init__(self, name) -> None:
        self.name = name
        self.data: list[Any] = []
        self.rank: int = 0
        self.total_processed: int = 0

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
    def __init__(self, name) -> None:
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
            self.total_processed += len(data)
        else:
            self.data.append(str(data))
            self.total_processed += 1


class TextProcessor(DataProcessor):
    def __init__(self, name) -> None:
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
            self.total_processed += len(data)
        if isinstance(data, str):
            self.data.append(data)
            self.total_processed += 1


class LogProcessor(DataProcessor):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.data: list[str] = []

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return True
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            return True
        else:
            return False

    def ingest(self, data: dict | list[dict]) -> None:
        if not self.validate(data):
            raise TypeError("Improper dict data")
        if isinstance(data, dict):
            self.data.append(data)
            self.total_processed += 1
        if isinstance(data, list):
            self.data += data
            self.total_processed += len(data)


class DataStream:
    def __init__(self) -> None:
        self.processor: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processor.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for items in stream:
            handled = False
            for process in self.processor:
                if process.validate(items):
                    process.ingest(items)
                    # if isinstance(items, list):
                    #     self.total_process += len(items)
                    # else:
                    #     self.total_process += 1
                    handled = True
                    break
            if not handled:
                print(f"DataStrem error - Can't process element in "
                      f"stream: {items}")

    def print_process_stats(self) -> None:
        print("=== DataStream statistics ===")
        if not self.processor:
            print("No processor found, no data")
            return
        for process in self.processor:
            if isinstance(process, NumericProcessor):
                print(f"Numeric Processor: total {process.total_processed} "
                      f"items Processed, remaining {len(process.data)} "
                      f"on Processor")
            if isinstance(process, TextProcessor):
                print(f"Text Processor: total {process.total_processed} "
                      f"items Processed, remaining {len(process.data)} "
                      f"on Processor")
            if isinstance(process, LogProcessor):
                print(f"Log Processor: total {process.total_processed} "
                      f"items Processed, remaining {len(process.data)} "
                      f"on Processor")


def demonstrate_datastream() -> None:
    process1 = NumericProcessor("process1")
    process2 = TextProcessor("process2")
    process3 = LogProcessor("process3")
    ds = DataStream()
    i: int = 0
    ds.print_process_stats()
    print("\nRegistering Numeric Processor\n")
    print(f"Send first batch of data on stream: {list1}")
    ds.register_processor(process1)
    ds.process_stream(list1)
    ds.print_process_stats()
    print("\nRegistering other data processors\n")
    print("send batch again")
    ds.register_processor(process2)
    ds.register_processor(process3)
    ds.process_stream(list1)
    ds.print_process_stats()
    print("\nConsume some elements from the data processorts:"
          " Numeric 3, text 2, log 1")
    while i < 3:
        process1.output()
        i += 1
    i = 0
    while i < 2:
        process2.output()
        i += 1
    i = 0
    while i < 1:
        process3.output()
        i += 1
    ds.print_process_stats()


def main():
    print("=== Code Nexus - Stream ===\n")
    print("initialize Data Stream....")
    demonstrate_datastream()


if __name__ == "__main__":
    main()
