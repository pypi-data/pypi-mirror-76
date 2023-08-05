'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._973 import DetailedRigidConnectorDesign
    from ._974 import DetailedRigidConnectorHalfDesign
