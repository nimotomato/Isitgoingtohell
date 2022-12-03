# Isitgoingtohell
News sentiment analysis.

bbc_scraper:
This module scrapes BBC news site.
Returns headline, date (if headline has no date tag, it uses todays date), and region. Writes data to a json file locally. Do not know how to change this. The resulting data can be uploaded from upload_scraped_data in the run-module. It uploads to the 'data'-table. Two columns are null, label and score, to keep track of what data has gone through sentiment analysis.


data_management:
This module interacts with the database. It has 4 main features:
Manage connection:
set up and close connection.

Retrieve data:
Get data in various ways.

Upload data:
upload data in various ways. 

Modify data:
Reoders data, changes it into strings to be uploaded or checks database for duplicates (local, db)


sentiment_analysis:
This module runs sentiment analysis on headlines, either from database or the file produced by bbc_scraper. The main function, analyse_data, returns a list of dicts. When analysing data, get data from table 'data' that has not yet been analysed, i.e. where label and score are null. The resulting data can be uploaded from upload_analysed_data in the run-module via the data_management module, which happens by uploading the correct item in the database. Items are kept track of using the headline text as it is unique. 

label_analysis:
This module has two children and two grandchildren.
Load data: Gets data needed from database and loads a csv.-file of region codes needed to map the graph.

General method: parent of undated and dated methods.

Undated_methods: Using sentiment analysed data from table 'data', calculates ratio of positive and negative sentiments grouped by region.
Mainly consists of sorting as we are dealing with different datastructures(list of tuples, list of dicts, and pseudo-ordered list of dicts). It also maps all countries to their respective regions, which is needed to display them in the graph. The ratio should be calculated using the previously calculated ratios. To do this, metadata is added before uploading it. Metada contains number of labels used to calculate mean and calculation date. A new mean can be calculated by multiplying the previous mean by previous labels used, adding the previous total to new total, adding previous labels to new labels, and calculating a new mean.

Dated_methods: Does the same thing as undated_methods, but grouped by regions AND dates. Does not calculate ratio using the old calculations in the same way, but does it freshly which is bad. This uploads duplicates, dunno how to fix.


graph:
This module has two children, dated and undated. 
The dated class paints a picture consisting of data sorted by date, while the undated uses all data to paint a picture. 
The classes needs data from the database. When loading data for the undated one, ironcally you have to specify the calculation date you want to map. 


