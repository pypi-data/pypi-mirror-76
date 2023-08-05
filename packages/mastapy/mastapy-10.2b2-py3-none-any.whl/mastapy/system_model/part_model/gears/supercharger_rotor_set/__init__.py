'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2115 import BoostPressureInputOptions
    from ._2116 import InputPowerInputOptions
    from ._2117 import PressureRatioInputOptions
    from ._2118 import RotorSetDataInputFileOptions
    from ._2119 import RotorSetMeasuredPoint
    from ._2120 import RotorSpeedInputOptions
    from ._2121 import SuperchargerMap
    from ._2122 import SuperchargerMaps
    from ._2123 import SuperchargerRotorSet
    from ._2124 import SuperchargerRotorSetDatabase
    from ._2125 import YVariableForImportedData
