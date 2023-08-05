'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._739 import KlingelnbergCycloPalloidSpiralBevelGearDesign
    from ._740 import KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
    from ._741 import KlingelnbergCycloPalloidSpiralBevelGearSetDesign
    from ._742 import KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
