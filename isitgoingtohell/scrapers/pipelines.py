# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

import numpy as np
import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from transformers import pipeline

from isitgoingtohell.data_management.db_management import Database as DB
from isitgoingtohell.utils import load_toml

REGIONS = ["africa", "asia", "europe", "oceania", "north america", "south america"]

filename = "items"


class RegionPipeline:
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if item["region"] == "us_and_canada":
            item["region"] = "north america"
        elif item["region"] == "middle_east":
            item["region"] = "asia"
        elif item["region"] == "australia":
            item["region"] = "oceania"
        elif item["region"] == "latin_america":
            item["region"] = "south america"
        elif item["region"] == "bolivia":
            item["region"] = "south america"
        elif item["region"] == "brazil":
            item["region"] = "south america"
        elif item["region"] == "colombia":
            item["region"] = "south america"
        elif item["region"] == "china":
            item["region"] = "asia"
        elif item["region"] == "asia pacific":
            item["region"] = "asia"
        elif item["region"] == "united kingdom":
            item["region"] = "europe"
        elif item["region"] == "united states":
            item["region"] = "north america"
        elif item["region"] == "middle east":
            item["region"] = "asia"
        elif item["region"] == "afghanistan":
            item["region"] = "asia"
        elif item["region"] == "sudan":
            item["region"] = "africa"
        elif item["region"] == "israel":
            item["region"] = "asia"

        return item


class RemoveUncategorized:
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if item["region"] in REGIONS:
            return item
        else:
            item["region"] = None

            return item


class CsvWriterPipeline(object):
    def open_spider(self, spider):

        if not os.path.exists(spider.settings["OUTPUT_CSV"]):
            with open(spider.settings["OUTPUT_CSV"], "w") as f:
                f.write("headline\tdate\tregion\n")

        self.file = open(spider.settings["OUTPUT_CSV"], "a")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # line = json.dumps(dict(item), default=str) + ",\n"
        self.file.write(f'{item["headline"]}\t{item["date"]}\t{item["region"]}\n')
        return item
