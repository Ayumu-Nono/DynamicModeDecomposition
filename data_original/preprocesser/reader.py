import os
import re

import numpy as np

from data_model.model import Model


L_dimensions: int = 18 - 1
L_dtype: int = 20 - 1
L_dnum: int = 21 - 1
L_values_start: int = 23 - 1


class Reader:
    """1ファイルに対して動作"""
    def __init__(self) -> None:
        self.contents: list = []
        self.path = ""
        
    def read2linelist(self, path: str):
        self.path = path
        with open(path) as f:
            self.contents = f.readlines()

    def _get_dimentions(self) -> list:
        dimentions = self.contents[L_dimensions]
        dimentions = re.search(re.escape("[") + '(.*)' + re.escape("]"), dimentions)
        dimentions = dimentions.group()[1:-1]
        dimentions = [int(d) for d in dimentions.split()]
        return dimentions

    def _get_dtype(self) -> str:
        dtype = self.contents[L_dtype]
        dtype = re.search(re.escape("<") + '(.*)' + re.escape(">"), dtype)
        dtype = dtype.group()[1:-1]
        return dtype

    def _get_dnum(self) -> int:
        dnum = self.contents[L_dnum]
        dnum = int(dnum)
        return dnum

    def _get_values(self, dnum: int, dtype: str) -> np.ndarray:
        var = self.contents[
            L_values_start:L_values_start + dnum
        ]
        if dtype == "scalar":
            var = [float(value.rstrip("\n")) for value in var]
            values = np.array(var)
            assert(len(values) == dnum)
        elif dtype == "vector" or dtype == "symmTensor":
            var = [
                re.search(
                    re.escape("(") + '(.*)' + re.escape(")"),
                    value.rstrip("\n")
                ).group()[1:-1].split(" ")
                for value in var
            ]
            var = [
                [float(v) for v in value]
                for value in var
            ]
            values = np.array(var)
            assert(len(values) == dnum)
        else:
            raise KeyError("Invalid Key in dtype", dtype)
        return values

    def _get_species(self) -> str:
        return self.path.split("/")[-1]

    def _get_dirname(self) -> str:
        return self.path.split("/")[-2]

    def set_meta(self, model: Model, is_initial=False, has_coordinate=False) -> None:
        model.dimensions = self._get_dimentions()
        model.dtype = self._get_dtype()
        model.dnum = self._get_dnum()
        model.values = self._get_values(dnum=model.dnum, dtype=model.dtype)
        model.species = self._get_species()
        model.dirname = self._get_dirname()
        if is_initial:
            model.is_initial = True
        if has_coordinate:
            model.has_coordinate = True


if __name__ == "__main__":
    r = Reader()
    model = Model()
    r.read2linelist(path="../dogbone_dumbbell_A12/dogbone_dumbbell_A12/0.01/alpha.poly")
    r.set_meta(model=model)
    model.print()