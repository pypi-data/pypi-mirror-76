## Django Highcharts series

This will create a series for line/column graph just by passing in the data and
the name of the column/columns as a list.

## Installation
Run the following to install:

''' python 
pip install django-highcharts-series
'''

## Usuage

''' python
from django_highcharts_series import LINE_GRAPH

series, category = LINE_GRAPH(data, [column_name], category_column)

'''