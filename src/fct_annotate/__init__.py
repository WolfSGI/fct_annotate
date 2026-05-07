import typing as t
from dataclasses import dataclass
from inspect import unwrap, getmembers, isroutine
from dataclasses import asdict


@dataclass
class Annotation:
    __key__: t.ClassVar[str] = '__annotations__'

    @staticmethod
    def discriminator(component) -> Exception | None:
        if not isroutine(component):
            return TypeError(f"{component!r} is not a routine.")
        if component.__name__.startswith("_"):
            return NameError(f"{component!r} has a private name.")
        return None

    def dump(self, component):
        return asdict(self)

    @classmethod
    def predicate(cls, component):
        if cls.discriminator(component) is not None:
            return False
        return True

    def __call__(self, func):
        canonical = unwrap(func)
        if error := self.discriminator(canonical):
            raise error
        setattr(canonical, self.__key__, self.dump(func))
        return func

    @classmethod
    def find(cls, obj_or_module):
        members = getmembers(obj_or_module, predicate=cls.predicate)
        for name, func in members:
            canonical = unwrap(func)
            if (val := getattr(canonical, cls.__key__, False)) is not False:
                yield val, func


def annotation(key: str):
    def annotation_decorator(cls):
        dc = dataclass(kw_only=True)(cls)
        return type(
            f"Annotation{cls.__name__.title()}",
            (dc, Annotation),
            {"__key__": f"__annotation_{key}__"}
        )
    return annotation_decorator
