import os
from posixpath import dirname
from typing import List

import pandas as pd
import numpy as np

from data_model.model import Model
from reader import Reader


class Loader:
    def __init__(self, dirpath_df) -> None:
        self.loading_fnames: List[str] = [
            "U", "p", "p_rgh", "T", "alpha.poly"
        ]
        self.loading_fnames_initial: List[str] = [
            "alphat", "k", "muTilda", "nut", "P", "T", "U"
        ]
        self.dirpath_df: pd.DataFrame = dirpath_df

    # each file
    def _load2model(
        self,
        file_index: int, fpath: str, is_initial, has_coordinate
    ) -> Model:
        model = Model()
        reader = Reader()
        reader.read2linelist(path=fpath)
        reader.set_meta(model=model)
        del reader
        return model

    def load_all_species(self, file_index, dir_path, is_initial, has_coordinate) -> List[Model]:
        models: List[Model] = []
        if is_initial:
            fnames = self.loading_fnames_initial
        else:
            fnames = self.loading_fnames

        for species in fnames:
            fpath = os.path.join(dir_path, species)
            print(fpath)
            model = self._load2model(file_index=file_index, fpath=fpath, is_initial=is_initial, has_coordinate=has_coordinate)
            models.append(model)
        return models
    
    def load_all_dirs(self, dirnames_df: pd.DataFrame) -> List[List[Model]]:
        alltime_models: List[List[Model]] = []
        for i in range(len(dirnames_df)):
            file_index = dirnames_df.loc[i, "fileIndex"]
            dir_path = dirnames_df.loc[i, "dirpath"]
            is_initial = dirnames_df.loc[i, "isInitial"]
            has_coordinate = dirnames_df.loc[i, "hasCoordinate"]
            if is_initial:
                continue
            models: List[Model] = self.load_all_species(file_index=file_index, dir_path=dir_path, is_initial=is_initial, has_coordinate=has_coordinate)
            alltime_models.append(models)
        return alltime_models


if __name__ == "__main__":
    loader = Loader("hoge")
    dirnames_df = pd.read_csv("dirnames_df.csv")
    alltime_models = loader.load_all_dirs(dirnames_df=dirnames_df)


