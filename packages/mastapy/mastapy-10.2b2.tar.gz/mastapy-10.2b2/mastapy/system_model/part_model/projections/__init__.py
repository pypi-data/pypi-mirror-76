'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2045 import SpecifiedConcentricPartGroupDrawingOrder
    from ._2046 import SpecifiedParallelPartGroupDrawingOrder
