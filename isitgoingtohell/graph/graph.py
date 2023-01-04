from isitgoingtohell.label_analysis.label_analysis import Statistics
from isitgoingtohell.utils import load_csv
import plotly.express as px
import pandas as pd
from isitgoingtohell.data_management.db_management import Database as DB
from isitgoingtohell.scrapers.pipelines import REGIONS

TABLENAME = 'geography'

class Graph():
    def __init__(self):
        self.stats = Statistics()
        db = DB()
        self.country_codes = load_csv("only_codes.csv")
        query = f'SELECT * FROM {TABLENAME}'
        db.cur.execute(query)
        self.data = [{'ratio': i[0], 'date': i[1], 'region': i[2]} for i in db.cur.fetchall()]
        db.connection.close()

    def add_country_codes(self, formated_ratios, region):
        # Add country codes for a region.
        ratios_with_country_codes = []

        for country in self.country_codes:
            if country['region'].lower() == region:
                for score in formated_ratios:
                    if score['region'] == region:
                        item = {}
                        item['country_code'] = country['code']
                        item['ratio'] = score['ratio']
                        item['date'] = score['date']
                        item['region'] = score['region']
                        ratios_with_country_codes.append(item)

        return ratios_with_country_codes 

    def add_codes_all_regions(self, data) -> list:
        # Adds country codes for all regions.
        ratios_with_country_codes = []
        for region in REGIONS:
            ratios_with_country_codes.extend(self.add_country_codes(data, region))

        return ratios_with_country_codes

    def set_dataframe(self):
        data_mapped_to_country_code = self.add_codes_all_regions(data=self.data)
        columns = data_mapped_to_country_code[0].keys()
        
        return pd.DataFrame(data_mapped_to_country_code, columns=columns).sort_values(by = 'date')

    def set_choropleth_settings(self, dataframe):
        # Set settings
        figure_settings = px.choropleth(
            dataframe, 
            locationmode="ISO-3", 
            locations="country_code",
            color="ratio",
            hover_name="region",
            title = "IS IT GOING TO HELL?", 
            animation_frame= "date",
            range_color=[0.2, 1.2],
            color_continuous_scale=px.colors.diverging.RdYlGn
            )
            
        return figure_settings

    def draw_choropleth(self):
        df = self.set_dataframe()
        figure_settings = self.set_choropleth_settings(df)
        fig = figure_settings
        fig["layout"].pop("updatemenus")
        fig.show()