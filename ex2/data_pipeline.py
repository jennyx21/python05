import typing
from typing import Any, Protocol
from abc import ABC, abstractmethod


list1 = ['Hello world', [3.14, -1, 2.71],
         [{'log_level': 'WARNING', 'log_message':
           'Telnet access! Use ssh instead'},
          {'log_level': 'INFO', 'log_message':
           'User wil isconnected'}], 42, ['Hi', 'five']]

list2 = [21, ['I love AI', 'LLMs are wonderful',
              'Stay healthy'], [{'log_level': 'ERROR', 'log_message':
                                 '500 server crash'},
                                {'log_level': 'NOTICE', 'log_message':
                                 'Certificateexpires in 10 days'}],
             [32, 42, 64, 84, 128, 168], 'World hello']


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
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
            self.total_processed += len(data)
        else:
            self.data.append(str(data))
            self.total_processed += 1


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
            self.total_processed += len(data)
        if isinstance(data, str):
            self.data.append(data)
            self.total_processed += 1


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
            self.total_processed += 1
            self.data.append(f"{data['log_level']}: {data['log_message']}")
        if isinstance(data, list):
            self.total_processed += len(data)
            for x in data:
                self.data.append(f"{x['log_level']}: {x['log_message']}")


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CSVExport:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if data:
            dictionary = ",".join(i for _, i in data)
            print(f"CSV Output:\n{dictionary}")


class JSONExport:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if data:
            dictionary = ', '.join(f'"item_{i}": "{d}"' for i, d in data)
            print(f"JSON Output:\n{{{dictionary}}}")


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
                    handled = True
                    break
            if not handled:
                print(f"DataStrem error - Can't process element in "
                      f"stream: {items}")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for process in self.processor:
            got_list: list[tuple[int, str]] = []
            for _ in range(nb):
                if len(process.data) == 0:
                    break
                got_list.append(process.output())
            if len(got_list) > 0:
                plugin.process_output(got_list)

    def print_process_stats(self) -> None:
        print("\n=== DataStream statistics ===")
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


def demonstrate_datapipeline() -> None:
    process1 = NumericProcessor("process1")
    process2 = TextProcessor("process2")
    process3 = LogProcessor("process3")
    ds = DataStream()
    plugin1 = CSVExport()
    plugin2 = JSONExport()
    ds.print_process_stats()
    print("\nRegistering Processors\n")
    print(f"Send first batch of data on stream: {list1}")
    ds.register_processor(process1)
    ds.register_processor(process2)
    ds.register_processor(process3)
    ds.process_stream(list1)
    ds.print_process_stats()
    print("Send 3 Processed data from each processor to CSV plugin:")
    ds.output_pipeline(3, plugin1)
    ds.print_process_stats()
    print(f"\nSend another batch of data on stream: {list1}")
    ds.process_stream(list2)
    ds.print_process_stats()
    print("Send 5 Processed data from each processor to JSON plugin:")
    ds.output_pipeline(5, plugin2)
    ds.print_process_stats()


def main() -> None:
    print("=== Code Nexus - Stream ===\n")
    print("initialize Data Stream....")
    demonstrate_datapipeline()


if __name__ == "__main__":
    main()
