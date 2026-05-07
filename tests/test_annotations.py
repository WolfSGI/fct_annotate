import pytest
from fct_annotate import annotation


@annotation("example")
class example:
    name: str
    title: str


def test_empty_annotation():

    class Empty:
        ...


    found = list(example.find(Empty))
    assert found == []


def test_simple_cls_annotation():

    class Simple:

        @example(name='name', title='title')
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

        @example(name='name', title='title')
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

        @example(name='name', title='title')
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

        @example(name='name', title='title')
        def whatever(self):
            ...


    class NotSoSimple(Simple):

        @example(name='other name', title='other title')
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

            @example(name='name', title='title')
            def __test__(self):
                ...


def test_class_annotation():

    with pytest.raises(TypeError):
        @example(name='name', title='title')
        class Simple:
            ...


def test_decorated_annotation():

    class Simple:

        @example(name='name', title='title')
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


def test_barren_annotation():

    @annotation("useless")
    class barren:
        pass

    class Simple:

        @barren()
        def whatever(self):
            ...

        @barren()
        def something_else(self):
            ...

    obj = Simple()
    found = list(barren.find(obj))
    assert found == [
        (
            {},
            obj.something_else,
        ),
        (
            {},
            obj.whatever,
        ),
    ]


def test_annotation_dump():

    @annotation("useless")
    class barren:

        def dump(self, component):
            return {'overridden': True}


    class Simple:

        @barren()
        def whatever(self):
            ...

        @barren()
        def something_else(self):
            ...

    obj = Simple()
    found = list(barren.find(obj))
    assert found == [
        (
            {'overridden': True},
            obj.something_else,
        ),
        (
            {'overridden': True},
            obj.whatever,
        ),
    ]
