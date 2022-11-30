from isitgoingtohell.data_management.data_analysis2 import Dated_methods as DM
from isitgoingtohell.data_management.data_analysis2 import Undated_methods as UM
from isitgoingtohell.utils import load_csv
import plotly.express as px
import pandas as pd


class Graph():
    def __init__(self):
        self.dm = DM()
        self.um = UM()
        self.country_codes = load_csv("only_codes.csv")

    def draw_choropleth(self, figure_settings):
        fig = figure_settings
        fig["layout"].pop("updatemenus")
        fig.show()


class Dated_graph(Graph):
    def __init__(self, geography_data, column_names):
        super().__init__()
        # Get data
        self.geography_data = geography_data
        self.column_names = column_names
        self.dataframe = pd.DataFrame(geography_data, columns=column_names).sort_values(by = 'date')

    def set_choropleth_settings(self, df):
        # Set data into settings
        figure_settings = px.choropleth(
            df, 
            locationmode="ISO-3", 
            locations="country_code",
            color="score",
            hover_name="region",
            title = "IS IT GOING TO HELL?", 
            animation_frame= "date",
            range_color=[0.2, 1.2],
            color_continuous_scale=px.colors.diverging.RdYlGn
            )
        
        return figure_settings

    def draw_dated_choropleth(self):
        settings = self.set_choropleth_settings(self.dataframe)
        self.draw_choropleth(settings)


class Undated_graph(Graph):
    def __init__(self, database_object):
        super().__init__()
        self.db = database_object
        region_scores = self.um.calculate_ratio()
        self.populated_regions = self.um.sort_all_regions(region_scores)
        self.figure_settings = px.choropleth(
            self.populated_regions, 
            locationmode='ISO-3', 
            locations='country_code',
            color='score',
            hover_name='region',
            title ='IS IT GOING TO HELL?', 
            range_color=[0.2, 1],
            color_continuous_scale=px.colors.diverging.RdYlGn
            )

    def draw_undated_choropleth(self):
        # Draws map from data in database
        self.draw_choropleth(self.figure_settings)