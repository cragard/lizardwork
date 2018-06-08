def gen_liz_num(data, arg1: str = 'species', arg2: str = 'toes', arg3: str = 'sex', svlcol: str = 'svl',
                date: str = 'date', year: str = 'year', lizmarkname: str = 'lizMark'):
    """[Description]"""
    import pandas as pd
    import numpy as np

    # define  unique identifier
    data[lizmarkname] = data[arg1] + data[arg2] + data[arg3]  # Need to rewrite this to handle variable \
    # list length

    # define initial dict of unique lizard numbers and map on lizmarkname to create initial liz num
    lizmarkdict = pd.DataFrame(data[lizmarkname].unique()).reset_index().to_dict()
    data['lizNumber'] = data[lizmarkname].map(lizmarkdict)

    # identify values for first sighting of a lizard
    data['dateMin'] = data.groupby(lizmarkname).date.min()
    data['svlMin'] = data.loc[data[date] == data.dateMin, svlcol]
    data['yearMin'] = data.loc[data[date] == data.dateMin, 'year']

    # determine difference between first values and observation values
    data['yearDiff'] = data[year] - data.yearMin
    data['svlDiff'] = data[svlcol] - data.svlMin

    # Apply criteria to identify misclassified unique individuals
    data.loc[(data.yearDiff > 7) | (data.svlDiff < -2), 'misclassified'] = True

    if len(data.loc[data.misclassified == True]) > 0:
        # Strip lizNumber from misclassified animals
        data.loc[data.misclassified == True, 'lizNumber'] = np.nan

        # define new dict of unique lizard numbers and map on lizmarkname to create new liz num
        lizmarkdict2 = pd.DataFrame(data[data.misclassified == True, lizmarkname].unique()).reset_index().to_dict()
        data['lizNumber'] = data[data.misclassified == True, lizmarkname].map(lizmarkdict2)

        # Apply criteria to identify properly classified unique individuals and remove misclassification label
        data.loc[(data.yearDiff <= 7) | (data.svlDiff >= -2), 'misclassified'] = np.nan

    print('Currently, there are {} misclassified observations'.format(data.loc[data.misclassified == False].shape[0]))

    return data
