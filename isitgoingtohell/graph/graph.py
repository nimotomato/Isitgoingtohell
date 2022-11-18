
from isitgoingtohell.data_management.data_analysis import Dated_methods as DM
from isitgoingtohell.utils import load_csv
import plotly.express as px


class Graph():
    def __init__(self):
        dm = DM()
        country_codes = load_csv("only_codes.csv")
        date_score_region = dm.to_dict(dm.calculate_ratio_dated(), not_null=True)
        self.populated_regions = dm.populate_regions(country_codes, date_score_region)


    def draw_choropleth(self):
        fig = px.choropleth(
            self.populated_regions, 
            locationmode="ISO-3", 
            locations="country_code",
            color="dated_region_score",
            hover_name="region",
            title = "News sentiments ratios", 
            animation_frame= "date",
            color_continuous_scale=px.colors.diverging.RdYlGn
            )

        fig["layout"].pop("updatemenus")
        fig.show()