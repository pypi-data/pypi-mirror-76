
import platform


class IdentifyCodeList(object):
    def __init__(self):
        pass

    def operating_system(self):
        plat_form = platform.platform()
        return plat_form[0:2]

    def version(self):
        version = platform.version()
        return version[0:3]

    def architecture(self):
        architecture = platform.architecture()
        return architecture[0:3]

    def machine(self):
        machine = platform.machine()
        return machine[0:2]

    def node(self):
        node = platform.node()
        return node[0:3]

    def processor(self):
        processor = platform.processor()
        return processor[0:3]

    def all(self):
        all = self.operating_system() + self.version() + "".join(self.architecture()) + self.machine() + self.node() + self.processor()
        all = all.replace(" ", "")
        return all



