"""THE FUNCTION WILL RETURN DATA SERIES AND CATEGORY DATA FOR LINE GRAPH"""
def LINE_GRAPH(data, column_select, category_col):

    series_list= []
    
    for col in column_select:

        series_list.append({
                             'name': col.replace("_", " "),
                             'data': list(data.values_list(col, flat=True)),
                           })

    category_list = list(data.values_list(category_col, flat=True))

    return series_list, category_list
