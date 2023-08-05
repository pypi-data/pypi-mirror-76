from janis_core import File


class Tsv(File):
    def __init__(self, optional=False, extension=".tsv"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "tsv"

    def doc(self):
        return "A tab separated file"
