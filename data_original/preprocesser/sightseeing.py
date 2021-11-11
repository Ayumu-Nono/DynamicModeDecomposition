import os
from glob import glob
from typing import List

import pandas as pd


class Sightseeing:
    def __init__(self, root_path) -> None:
        self.root_path = root_path
        self.dirs: list = []
        self.fnames: list = []
        self.dataframes: List[pd.DataFrame] = []

    def see_indir(self, dir1="case2_par4") -> bool:
        self.dirs = sorted(os.listdir(os.path.join(self.root_path, dir1)))
        for dir in self.dirs:
            _path = os.path.join(self.root_path, dir1, dir, "*")
            _fnames = [fname.split("/")[-1] for fname in glob(_path)]
            self.fnames.append(_fnames)
        return True

    def read_csvs(self, outdir="flist") -> bool:
        for i, dir in enumerate(self.dirs):
            df = pd.DataFrame(self.fnames[i], columns=["fname"])
            df.to_csv(os.path.join(outdir, dir))
        return True

    # def outputter(self, dir="tree") -> bool:
        
        

if __name__ == "__main__":
    ss = Sightseeing("../data/")
    ss.see_indir()
    ss.read_csvs()
        

