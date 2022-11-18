
from isitgoingtohell.data_management.data_analysis import Dated_methods as DM
from isitgoingtohell.data_management.data_analysis import Undated_methods as UM
from isitgoingtohell.utils import load_csv
import plotly.express as px


class Graph():
    def __init__(self):
        self.dm = DM()
        self.um = UM()
        self.country_codes = load_csv("only_codes.csv")

class Dated_graph(Graph):
    def __init__(self):
        super().__init__()
        date_score_region = self.dm.to_dict(self.dm.calculate_ratio_dated(), not_null=True)
        self.populated_regions = self.dm.populate_regions(self.country_codes, date_score_region)

    def draw_choropleth(self):
        fig = px.choropleth(
            self.populated_regions, 
            locationmode="ISO-3", 
            locations="country_code",
            color="dated_region_score",
            hover_name="region",
            title = "News sentiments ratios", 
            animation_frame= "date",
            range_color=[0.2, 1.2],
            color_continuous_scale=px.colors.diverging.RdYlGn
            )

        fig["layout"].pop("updatemenus")
        fig.show()

class Undated_graph(Graph):
    def __init__(self):
        super().__init__()
        region_scores = self.um.to_dict(self.um.calculate_ratio_total(), not_null=True)
        self.populated_regions = self.um.populate_regions(self.country_codes, region_scores)

    def draw_choropleth(self):
        fig = px.choropleth(
            self.populated_regions, 
            locationmode="ISO-3", 
            locations="country_code",
            color="region_score",
            hover_name="region",
            title = "News sentiments ratios", 
            range_color=[0.2, 1],
            color_continuous_scale=px.colors.diverging.RdYlGn
            )

        fig["layout"].pop("updatemenus")
        fig.show()