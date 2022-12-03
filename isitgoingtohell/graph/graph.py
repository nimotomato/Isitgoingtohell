from isitgoingtohell.label_analysis.label_analysis import Dated_methods as DM
from isitgoingtohell.label_analysis.label_analysis import Undated_methods as UM
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
        self.geography_data = self.dm.map_all_regions_dated(geography_data)
        self.column_names = geography_data[0].keys()
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
    def __init__(self, geography_data_undated):
        super().__init__()
        self.geography_data = self.um.map_all_regions_undated(geography_data_undated)

    def set_choropleth_settings(self, mapped_geography_data):
        figure_settings = px.choropleth(
            mapped_geography_data, 
            locationmode='ISO-3', 
            locations='country_code',
            color='score',
            hover_name='region',
            title ='IS IT GOING TO HELL?', 
            range_color=[0.2, 1],
            color_continuous_scale=px.colors.diverging.RdYlGn
            )
        return figure_settings
        
    def draw_undated_choropleth(self):
        # Draws map from data in database
        settings = self.set_choropleth_settings(self.geography_data)
        self.draw_choropleth(settings)