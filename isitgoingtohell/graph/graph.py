from isitgoingtohell.data_management.db_management import DB 
from isitgoingtohell.data_management.data_analysis import Dated_methods as DM
from isitgoingtohell.data_management.data_analysis import Undated_methods as UM
from isitgoingtohell.utils import load_csv
import plotly.express as px
import pandas as pd

class Graph():
    def __init__(self):
        self.dm = DM()
        self.um = UM()
        self.db = DB()
        self.country_codes = load_csv("only_codes.csv")

    def draw_choropleth(self, figure_settings):
        fig = figure_settings
        fig["layout"].pop("updatemenus")
        fig.show()

class Dated_graph(Graph):
    def __init__(self):
        super().__init__()
        # Get data
        data = self.db.get_geography_data()
        columns = self.db.get_col_names_not_id('geography', len(data[0].keys())).split(",")
        
        # Sort data
        df = pd.DataFrame(data, columns=columns).sort_values(by = 'date')

        # Set data into settings
        self.figure_settings = px.choropleth(
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


    def draw_dated_choropleth(self):
        self.draw_choropleth(self.figure_settings)

class Undated_graph(Graph):
    def __init__(self):
        super().__init__()
        region_scores = self.um.calculate_ratio_total()
        self.populated_regions = self.um.populate_regions(region_scores)
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
        self.draw_choropleth(self.figure_settings)