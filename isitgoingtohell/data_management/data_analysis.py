import pandas as pd
from isitgoingtohell.data_management.db_management import DB


class Data_Analysis:
    def __init__(self):
        db = DB()
        data = db.get_all_data(tablename="data")
        self.df = pd.DataFrame(data, columns=["id", "headline","date","region","label","confidence_score", "iso_code"])

    def calculate_ratio(self, groupings: list):
        # Calculates ratio sorted by selected columns in the list.
        ratio = (
            self.df.replace('POSITIVE', 1).replace('NEGATIVE', 0).groupby(groupings, as_index=False)
                .agg(
                    positives_count=('label', 'sum'),
                    sentiment_count=('label', 'count'),
                    sentiment_ratio=('label', 'mean'))
        )

        return ratio

class Calculate_ratio_dated(Data_Analysis):      
    def __init__(self):
        super().__init__()

    def calculate_ratio_dated(self):
        groupings=['iso_code','date']
        return self.calculate_ratio(groupings)

class Calculate_ratio_total(Data_Analysis):
    def __init__(self):
        super().__init__()

    def calculate_ratio_total(self):
        groupings=['iso_code']
        return self.calculate_ratio(groupings)