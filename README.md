# news_extractor
This program extracts headlines from a specific news url within a given date range. To initialise the class Analysis, create a new instance of the class supplying 4 args namely, **term**, **url to website**, **date of begin**, **date of end**

### example
a = Analysis(term='Donald trump', site='prabhatkhabar.com', b_date='1/1/2020', e_date='1/31/2020')

Once the class has been initialised call the make_data object from the class to download the data and return a dataframe as a csv

### example
a.make_file()

