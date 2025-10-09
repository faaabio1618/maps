import abc
import os
from abc import ABC
from typing import Tuple

import kagglehub
import pandas as pd
from kagglehub import KaggleDatasetAdapter

from lib.AbstractDataRetriever import AbstractDataRetriever


class KaggleRetriever(AbstractDataRetriever, ABC):

    def __init__(self, *,
                 data_name,
                 description,
                 unit,
                 source,
                 min_year_range,
                 max_year_range,
                 round,
                 show_final,
                 keep_unit,
                 kaggle_handle,
                 file_names

                 ):
        super().__init__(
            data_name=data_name,
            source=source,
            keep_unit=keep_unit,
            min_year_range=min_year_range,
            max_year_range=max_year_range,
            show_final=show_final,
            unit=unit,
            description=description,
            round=round,
        )
        self.kaggle_handle = kaggle_handle
        self.file_names = file_names

    @abc.abstractmethod
    def retrieve(self, region) -> Tuple[pd.DataFrame, str]:
        pass

    def _retrieve_kaggle(self, region):
        datas = {}
        for file_name in self.file_names:
            cache_file = f"data/cache/kaggle/{self.kaggle_handle}/{self.data_name}.csv"
            if os.path.exists(cache_file):
                data = pd.read_csv(cache_file)
            else:
                path = kagglehub.dataset_download(handle=self.kaggle_handle, path=file_name, force_download=True)
                try:
                    data = pd.read_csv(path, encoding="utf-8")
                except:
                    data = pd.read_csv(path, encoding="ISO-8859-1")
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                data.to_csv(cache_file)
            datas[file_name] = data
        return datas
