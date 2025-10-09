from typing import Tuple

import pandas as pd

from lib.AbstractDataRetriever import AbstractDataRetriever


class ComposedDataRetriever(AbstractDataRetriever):

    def __init__(self, data_name, description, unit, retriever_1: AbstractDataRetriever,
                 retriever_2: AbstractDataRetriever, function,
                 is_rate=False, round=1, show_final=True):
        super().__init__(
            min_year_range=[max(retriever_1.min_year_range[0], retriever_2.min_year_range[0]),
                            min(retriever_1.min_year_range[1], retriever_2.min_year_range[1])],
            keep_unit=is_rate,
            max_year_range=[max(retriever_1.max_year_range[0], retriever_2.max_year_range[0]),
                            min(retriever_1.max_year_range[1], retriever_2.max_year_range[1])],
            round=round,
            description=description,
            show_final=show_final,
            unit=unit,
            data_name=data_name,
            source=f'{retriever_1.source}\n{retriever_2.source}'
        )
        self.retriever_1 = retriever_1
        self.retriever_2 = retriever_2
        self.function = function

    def retrieve(self, region) -> Tuple[pd.DataFrame, str]:
        data1, data_label_1 = self.retriever_1.retrieve(region)
        data2, data_label_2 = self.retriever_2.retrieve(region)
        data = pd.merge(data1, data2, on=["iso_a3", "year"])
        data["composed"] = [self.function(v1, v2) for v1, v2 in
                            zip(data[data_label_1].to_numpy(), data[data_label_2].to_numpy())]
        return data, "composed"
