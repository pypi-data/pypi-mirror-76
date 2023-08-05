'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2047 import ConcentricOrParallelPartGroup
    from ._2048 import ConcentricPartGroup
    from ._2049 import ConcentricPartGroupParallelToThis
    from ._2050 import DesignMeasurements
    from ._2051 import ParallelPartGroup
    from ._2052 import PartGroup
