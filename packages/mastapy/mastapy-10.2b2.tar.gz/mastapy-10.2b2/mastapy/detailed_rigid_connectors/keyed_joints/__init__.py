'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1023 import KeyedJointDesign
    from ._1024 import KeyTypes
    from ._1025 import KeywayJointHalfDesign
    from ._1026 import NumberOfKeys
