from news_extractor import Analysis

term = str(input('Enter search term: '))
site = str(input('Specific website to search: '))
b_date = str(input('Enter start date (M/D/YYYY): '))
e_date = str(input('Enter end date (M/D/YYYY): '))

# create class instance
a = Analysis(term=term, site=site, b_date=b_date, e_date=e_date)

# creating data frame
df = a.make_data()

print('Data saved in {}.csv'.format(str.split(site, '.')[0]))

if_print = str(input('Would you like to view the extracted data (Y/N): '))

if str.upper(if_print) == 'Y':
    print(df)