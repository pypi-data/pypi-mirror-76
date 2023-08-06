from abc import ABC, abstractstaticmethod


class Backend(ABC):
    @abstractstaticmethod
    def invert(T):
        ...

    @abstractstaticmethod
    def compose(T1, T2):
        ...

    @abstractstaticmethod
    def identity():
        ...
