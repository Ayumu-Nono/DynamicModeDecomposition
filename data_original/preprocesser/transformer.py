import pandas as pd
import numpy as np

from data_model.model import Model 
from loader import Loader


class TransFormer:
    """変形：座標とその位置でのスカラー量というデータ"""
    def __init__(self, df_coordinates: pd.DataFrame) -> None:
        self.df_coordinates = df_coordinates
        self.df: pd.DataFrame = None
        self.dnum = 0

    def set_void_df(self, dnum: int) -> None:
        self.dnum = dnum
        dummy_column = [i for i in range(dnum)]
        self.df = pd.DataFrame(dummy_column, columns=["index"])

    def add_coordinates(self) -> None:
        self.df["x"] = self.df_coordinates["x"]
        self.df["y"] = self.df_coordinates["y"]
        self.df["z"] = self.df_coordinates["z"]

    def add_column(self, model: Model) -> None:
        if model.dtype == "scalar":
            assert model.dnum == self.dnum
            self.df[model.species] = model.values
        elif model.dtype == "vector":
            model.values = model.values.T
            assert len(model.values) == 3, model.values.shape
            assert len(model.values[0]) == self.dnum, model.species
            v_list = [model.values[i] for i in range(3)]
            coordinate_names = ["x", "y", "z"]
            for i in range(3):
                column_name = model.species + coordinate_names[i]
                assert len(v_list[i]) == self.dnum, model.species
                self.df[column_name] = v_list[i]
        else:
            raise KeyError(model.dtype)

    def _make_path(self, it: int) -> str:
        return "datasets/{0}.csv".format(it)
    
    def make_datasets(self, it: int) -> None:
        path = self._make_path(it)
        self.df.to_csv(path)



if __name__ == "__main__":
    loader = Loader("hoge")
    dirnames_df = pd.read_csv("dirnames_df.csv")
    all_time_models = loader.load_all_dirs(dirnames_df=dirnames_df)

    df_coordinates = pd.read_csv("coordinates.csv")
    transformer = TransFormer(df_coordinates=df_coordinates)
    for i, models in enumerate(all_time_models):
        transformer.set_void_df(dnum=60400)
        transformer.add_coordinates()
        for model in models:
            if model.species == "phi_0" or model.species == "phi":
                continue
            if model.dtype != "scalar" and model.dtype != "vector":
                continue
            transformer.add_column(model=model)
        transformer.make_datasets(it=i)
            

