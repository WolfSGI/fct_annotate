import pytest
from fct_annotate import annotation


class example(annotation):
    name = "__example__"

    def __init__(self, name: str, title: str):
        super().__init__(name=name, title=title)


def test_empty_annotation():

    class Empty:
        ...


    found = list(example.find(Empty))
    assert found == []


def test_simple_cls_annotation():

    class Simple:

        @example('name', 'title')
        def whatever(self):
            ...


    found = list(example.find(Simple))
    assert found == [
        (
            {
                'name': 'name',
                'title': 'title',
            },
            Simple.whatever,
        )
    ]


def test_simple_obj_annotation():

    class Simple:

        @example('name', 'title')
        def whatever(self):
            ...


    obj = Simple()
    found = list(example.find(obj))
    assert found == [
        (
            {
                'name': 'name',
                'title': 'title',
            },
            obj.whatever,
        )
    ]


def test_inheritence_annotation():

    class Simple:

        @example('name', 'title')
        def whatever(self):
            ...


    class NotSoSimple(Simple):
        ...


    obj = NotSoSimple()
    found = list(example.find(obj))
    assert found == [
        (
            {
                'name': 'name',
                'title': 'title',
            },
            obj.whatever,
        )
    ]


def test_override_annotation():

    class Simple:

        @example('name', 'title')
        def whatever(self):
            ...


    class NotSoSimple(Simple):

        @example('other name', 'other title')
        def whatever(self):
            ...


    obj = NotSoSimple()
    found = list(example.find(obj))
    assert found == [
        (
            {
                'name': 'other name',
                'title': 'other title',
            },
            obj.whatever,
        )
    ]


def test_private_annotation():

    with pytest.raises(NameError):
        class Simple:

            @example('name', 'title')
            def __test__(self):
                ...


def test_class_annotation():

    with pytest.raises(TypeError):
        @example('name', 'title')
        class Simple:
            ...


def test_decorated_annotation():

    class Simple:

        @example('name', 'title')
        @classmethod
        def whatever(self):
            ...


    obj = Simple()
    found = list(example.find(obj))
    assert found == [
        (
            {
                'name': 'name',
                'title': 'title',
            },
            obj.whatever,
        )
    ]
