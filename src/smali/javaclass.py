import smali.source
import smali.parser


class JavaClass(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.source = smali.source.get_source_from_file(filepath)

    @property
    def methods(self):
        return smali.parser.extract_methods(self.source)

    @property
    def fields(self):
        return smali.parser.extract_attribute_names(self.source)


