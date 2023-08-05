from janis_core import File


class Csv(File):
    def __init__(self, optional=False, extension=".csv"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "csv"

    def doc(self):
        return "A comma separated file"
