from flask import Flask, render_template, url_for, request
import pandas as pd
import random
from scipy.spatial import distance

app = Flask(__name__) 


def format_value(value):
    """ This function convert value to actual number

    Args:
        value (string):  string value 

    Returns:
        [string]: return formatted value
    """
    if 'M' in value:
        value = float(value.replace('M', ''))
        value = value * 1000000
    elif 'K' in value:
        value = float(value.replace('K', ''))
        value = value * 1000
    return value


def format_wage(wage):
    """ This function convert wage to actual number

    Args:
        wage (string): wage string value

    Returns:
        [string]: return formatted wage
    """
    wage = wage.replace('€', '')
    if 'K' in wage:
        wage = float(wage.replace('K', ''))
        wage = wage * 1000
    return wage


def cleanup_data(input_data):
    """ This is a copied new data frame based on existing one, update column types and format values  

    Args:
        input_data (dataframe): orginal data frame created from csv file

    Returns:
        [dataframe]: formatted data frame based on orginal
    """
    raw_data = input_data[['Age','Overall', 'Potential', 'Value', 'Wage']].copy()
    raw_data['Value'] = raw_data['Value'].str.replace('€', '')
    raw_data['Value'] = raw_data['Value'].apply(format_value)
    raw_data['Value'] = raw_data['Value'].astype('float')
    raw_data['Wage'] = raw_data['Wage'].apply(format_wage)
    raw_data['Wage'] = raw_data['Wage'].astype('float')
    raw_data['Age'] = raw_data['Age'].astype('int')
    raw_data['Overall'] = raw_data['Overall'].astype('int')
    raw_data['Potential'] = raw_data['Potential'].astype('int')
    return raw_data


def get_five_similar(source_data,selected_id):
    """ This will get filve similar ids from clean data frame

    Args:
        source_data (dataframe): passing original data frame 
        selected_id (string): [description]

    Returns:
        [list]: return formatted id list
    """
    formatted_data = cleanup_data(source_data)
    selected = formatted_data.loc[selected_id].tolist()
    scores = []
    for i in range(formatted_data.shape[0]):
        lst = formatted_data.loc[i, ['Age','Overall', 'Potential', 'Value', 'Wage']].tolist()
        scores.append(distance.cosine(selected, lst))
    formatted_data['relation'] = pd.Series(scores)
    formatted_data = formatted_data.sort_values('relation', ascending=True).reset_index().loc[1:5]
    return formatted_data['index'].tolist()


def get_compare_ids(input_data):
    """ generate random ids from data set

    Args:
        input_data (dataframe): dataframe read from csv file

    Returns:
        [list]: return 5 similar id + 1 random pick id
    """

    df = input_data[input_data['Potential']>85].reset_index(drop=True)
    selected_player_index = random.randint(0,df.shape[0]-1) # find selected player
    five_ids = get_five_similar(input_data,selected_player_index)
    all_ids = five_ids + [selected_player_index]
    return all_ids


@app.route("/")
def first_index():
	return render_template('index.html')


@app.route("/game.html")
def game():
    """ This is game page for guess footballers

    Returns:
        render game page: pass data dictionary
    """
    source_data = pd.read_csv('./data_prep/data.csv')
    id_lst = get_compare_ids(source_data) 
    #ids = [0,1,2,3,4,5]
    selected_id = id_lst[-1]
    source_data = source_data.loc[id_lst]
    #ids = random.sample(ids, len(ids))

    # return display dictionary object to game page
    dict_data = {}
    dict_data['ids'] = id_lst # all picked player id
    dict_data['selected_id'] = id_lst[-1] # selected id would be last in id list
    dict_data['player_info'] = dict(source_data)
    return render_template('game.html', dict=dict_data)