from dataflows import Flow, load, dump_to_path, printer

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
CONFIRMED_US = 'time_series_covid19_confirmed_US.csv'
DEATH_US = 'time_series_covid19_deaths_US.csv'

# Flow(
#       load(f'{BASE_URL}{CONFIRMED}'),
#       load(f'{BASE_URL}{RECOVERED}'),
#       load(f'{BASE_URL}{DEATHS}'),
#       dump_to_path('csse_covid_19_data')
# ).results()[0]

extra_value = {'yesterday': '', 'today': ''}

def print_days(package):
    elems = package.pkg.descriptor['resources'][0]['schema']['fields'][-2:]
    extra_value.yesterday = elems[0]['name']
    extra_value.today = elems[1]['name']
    
def add_dates_column_to_schema(package):
    # Add a new field to the first resource
    elems = package.pkg.descriptor['resources'][0]['schema']['fields'][-2:]
    yesterday = elems[0]['name']
    today = elems[1]['name']

    package.pkg.descriptor['resources'][0]['schema']['fields'].append(dict(
        name='yesterday',
        type='number'
    ))
    package.pkg.descriptor['resources'][0]['schema']['fields'].append(dict(
        name='today',
        type='number'
    ))
    # Must yield the modified datapackage
    yield package.pkg
    # And its resources
    yield from package

def add_dates_column(row):
    row['yesterday'] = row['3/31/20']
    row['today'] = row['4/1/20']




# Flow(
#     load(f'csse_covid_19_data/confirmed_us/{CONFIRMED_US}'),
#     # dump_to_path('confirmed_today.csv')
  
# # ).process()[1]
# ).results()[0]


Flow(
    load(f'csse_covid_19_data/confirmed_us/{CONFIRMED_US}'),
    add_dates_column_to_schema,
    add_dates_column,
    dump_to_path('confirmed_today.csv'),
    # printer(num_rows=1, tablefmt='html')
).process()[1]

