import logging

from androguard.core.bytecodes.dvm import DalvikVMFormat
import lief

from .base import IDetector
from ml_analyzer.mlfw import MLFrameworkType

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO: write a test for this detector
class TFLiteDetector(IDetector):
    def fw_type(self) -> MLFrameworkType:
        return MLFrameworkType.TF_LITE

    def detect_dot_so_file(self, elf: lief.ELF.Binary) -> bool:
        # TODO: tyr to use symbols specificed here https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/def_file_filter/def_file_filter.py.tpl
        return super().detect_dot_so_file_by_symbol(
            elf, ['TfLite.*', 'Java_org_tensorflow_lite_.*']) or super().detect_dot_so_file_by_dot_rodata(
            elf, [b'TfLiteTensor', b'kTfLiteUInt8'])

    def detect_dex(self, dex: DalvikVMFormat) -> bool:
        return super().detect_dex_by_class_name(dex, ['Lorg/tensorflow/lite/.*'])
