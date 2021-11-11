import numpy as np


class Model:
    def __init__(self) -> None:
        self.dimensions: list = []
        self.dtype: str = ""
        self.dnum: int = 0
        self.values: np.ndarray = None
        self.is_initial: bool = False
        self.has_coordinate: bool = False
        self.species: str = ""
        self.dirname: str = ""
        
    def print(self) -> None:
        print("**************")
        contents = "model: {0}\n"\
            "dimensions: {1}\n"\
            "dtype: {2}\n"\
            "dnum: {3}\n"\
            "values: {4}\n"\
            "species: {5}\n"\
            "dirname: {6}"\
            .format(
                self,
                self.dimensions,
                self.dtype,
                self.dnum,
                self.values,
                self.species,
                self.dirname
            )
        print(contents)
        print("**************")