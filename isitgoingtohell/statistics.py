import pandas as pd

COLUMNS = ['region','label']

class Statistics():
    # Get data
    def __init__(self, data):
        self.dataframe = pd.DataFrame(data, columns=COLUMNS)

    # Calculate data
    def calculate_neg_freq(self):
        filtered_df = self.dataframe[self.dataframe['label'].isin(['NEU', 'POS'])]
        pos_count = filtered_df['region'].value_counts()

        filtered_df = self.dataframe[self.dataframe['label'].isin(['NEG'])]
        neg_count = filtered_df['region'].value_counts()

        ratios = neg_count.divide(pos_count)

        return ratios

    def calculate_pos_freq(self):
        filtered_df = self.dataframe[self.dataframe['label'].isin(['NEU', 'NEG'])]
        neg_count = filtered_df['region'].value_counts()

        filtered_df = self.dataframe[self.dataframe['label'].isin(['POS'])]
        pos_count = filtered_df['region'].value_counts()

        ratios = pos_count.divide(neg_count)

        return ratios

    def calculate_ratio_ignore_neutral(self):
        filtered_df = self.dataframe[self.dataframe['label'].isin(['NEG'])]
        neg_count = filtered_df['region'].value_counts()

        filtered_df = self.dataframe[self.dataframe['label'].isin(['POS'])]
        pos_count = filtered_df['region'].value_counts()

        ratios = pos_count.divide(neg_count)

        return ratios