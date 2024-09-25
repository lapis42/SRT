import abc
from typing import List, Dict
from .constants import WINDOW_SEAT


class Passenger(metaclass=abc.ABCMeta):
    """Passenger class. Highly inspired by `srt.py`
    <https://github.com/dotaitch/SRTpy/blob/master/SRTpy/srt.py>`
    by `dotaitch`
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    def __init_internal__(self, name: str, type_code: str, count: int):
        self.name = name
        self.type_code = type_code
        self.count = count

    def __repr__(self) -> str:
        return f"{self.name} {self.count}명"

    def __add__(self, other: "Passenger") -> "Passenger":
        if not isinstance(other, self.__class__):
            raise TypeError("Passenger types must be the same")
        if self.type_code == other.type_code:
            return self.__class__(count=self.count + other.count)
        raise ValueError("Passenger types must be the same")

    @classmethod
    def combine(cls, passengers: List["Passenger"]) -> List["Passenger"]:
        if not all(isinstance(p, Passenger) for p in passengers):
            raise TypeError("All passengers must be based on Passenger")

        passenger_dict = {}
        for passenger in passengers:
            key = passenger.__class__
            if key in passenger_dict:
                passenger_dict[key] += passenger
            else:
                passenger_dict[key] = passenger

        return [p for p in passenger_dict.values() if p.count > 0]

    @staticmethod
    def total_count(passengers: List["Passenger"]) -> str:
        if not all(isinstance(p, Passenger) for p in passengers):
            raise TypeError("All passengers must be based on Passenger")
        return str(sum(p.count for p in passengers))

    @staticmethod
    def get_passenger_dict(
        passengers: List["Passenger"],
        special_seat: bool = False,
        window_seat: str = None
    ) -> Dict[str, str]:
        if not all(isinstance(p, Passenger) for p in passengers):
            raise TypeError("All passengers must be instances of Passenger")

        combined_passengers = Passenger.combine(passengers)
        data = {
            "totPrnb": Passenger.total_count(combined_passengers),
            "psgGridcnt": str(len(combined_passengers)),
        }

        for i, passenger in enumerate(combined_passengers, start=1):
            data[f"psgTpCd{i}"] = passenger.type_code
            data[f"psgInfoPerPrnb{i}"] = str(passenger.count)

        data.update({
            "locSeatAttCd1": WINDOW_SEAT.get(window_seat, "000"),
            "rqSeatAttCd1": "015",
            "dirSeatAttCd1": "009",
            "smkSeatAttCd1": "000",
            "etcSeatAttCd1": "000",
            "psrmClCd1": "2" if special_seat else "1"
        })

        return data


class Adult(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("어른/청소년", "1", count)


class Child(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("어린이", "5", count)


class Senior(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("경로", "4", count)


class Disability1To3(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("장애 1~3급", "2", count)


class Disability4To6(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("장애 4~6급", "3", count)
