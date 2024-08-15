import abc
import weakref
import datetime
from typing import Iterable, Iterator, TypedDict, NamedTuple
import math
from pathlib import Path
import csv
import enum
import random
from dataclasses import dataclass


class BadSampleRow(ValueError):
    "Raise excepition for unvalid row."


class Sample(NamedTuple):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class Purporse(enum.IntEnum):
    Classification = 0
    Testing = 1
    Training = 2


class KnowSample(NamedTuple):
    sample: Sample
    species: str


class TestingKnowSample:
    def __init__(
            self, sample: KnowSample, classification: str | None = None
    ) -> None:
        self.sample = sample
        self.classification = classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(sample={self.sample!r},"
            f"classification={self.classification!r})"
        )


class TrainingKnowSample(NamedTuple):
    sample: KnowSample


class SampleReader:
    """
    See iris.names for attribute ordering in bezdekIris.data file
    """

    target_class = Sample
    header = [
        "sepal_length", "sepal_width",
        "petal_length", "petal_width", "class"
    ]

    def __init__(self, source: Path) -> None:
        self.source = source

    def sample_iter(self) -> Iterator[Sample]:
        target_class = self.target_class
        with self.source.open() as source_file:
            reader = csv.DictReader(source_file, self.header)
            for row in reader:
                try:
                    sample = target_class(
                        sepal_length=float(row["sepal_length"]),
                        sepal_width=float(row["sepal_width"]),
                        petal_length=float(row["petal_length"]),
                        petal_width=float(row["petal_width"]),
                    )
                except ValueError as ex:
                    raise BadSampleRow(f"Invalid {row!r}") from ex
                yield sample


class SampleDict(TypedDict):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str


class SamplePartion(list[SampleDict], abc.ABC):
    @overload
    def __init__(self, *, training_subset: float = 0.80) -> None:
        ...
    
    @overload
    def __init__(
        self,
        iterable: Iterable[SampleDict] | None = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        self.training_subset = training_subset
        if iterable:
            super().__init__(iterable)
        else:
            super().__init__

    @abc.abstractproperty
    @property
    def testing(self) -> list[TrainingKnowSample]:
        ...

    @abc.abstractproperty
    @property
    def training(self) -> list[TrainingKnowSample]:
        ...


class ShufflingSamplePartition(SamplePartion):
    def __init__(
            self,
            iterable: Iterable[SampleDict] | None = None,
            *,
            training_subset: float = 0.80,
    ) -> None:
        super().__init__(iterable, training_subset=training_subset)
        self.split: int | None = None

    def shuffle(self) -> None:
        if not self.split:
            random.shuffle(self)
            self.split = int(len(self) * self.training_subset)

    @property
    def training(self) -> list[TrainingKnowSample]:
        self.shuffle()
        return [TrainingKnowSample(**sd) for sd in self[: self.split]]
    
    @property
    def testing(self) -> list[TestingKnowSample]:
        self.shuffle
        return [TestingKnowSample(**sd) for sd in self[self.split :]]


class Distance:
    """Get distance."""

    def distance(self, s1: Sample, s2: Sample) -> float:
        pass


class MD(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        )


class SD(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        ) / sum(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        )


class CD(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return sum(
            [
                abs(s1.sepal_length - s2.sepal_length),
                abs(s1.sepal_width - s2.sepal_width),
                abs(s1.petal_length - s2.petal_length),
                abs(s1.petal_width - s2.petal_width),
            ]
        )


class ED(Distance):
    def distance(self, s1: Sample, s2: Sample) -> float:
        return math.hypot(
            s1.sepal_length - s2.sepal_length,
            s1.sepal_width - s2.sepal_width,
            s1.petal_length - s2.petal_length,
            s1.petal_width - s2.petal_width,
        )


class Hyperparameter:
    """Конкретный набор параметров настройки с k и алгоритмом расстояния"""

    k: int
    algorithm: Distance
    data: weakref.ReferenceType["TrainingData"]

    def classify(self, sample: Sample) -> str:
        """Алгоритм k-NN"""
        ...


class TrainingData:
    """A set of training data and testing data with methods to loas and test
the samples."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: list[Sample] = []
        self.testing: list[Sample] = []
        self.tuning: list[Hyperparameter] = []

    def load(
            self,
            raw_data_source: Iterable[dict[str, str]]
    ) -> None:
        """Load and partition the raw data."""
        self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)