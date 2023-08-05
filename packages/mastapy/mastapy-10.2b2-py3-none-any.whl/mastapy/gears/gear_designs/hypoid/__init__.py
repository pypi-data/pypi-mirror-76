'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._751 import HypoidGearDesign
    from ._752 import HypoidGearMeshDesign
    from ._753 import HypoidGearSetDesign
    from ._754 import HypoidMeshedGearDesign
