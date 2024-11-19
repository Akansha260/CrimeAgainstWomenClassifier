import matplotlib
import numpy as np
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import seaborn as sns

CSV_FILE_PATH = 'data/crime_data.csv'

SAFETY_LABELS = [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 
                 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
LABEL_MAPPING = {0: 'Safe', 1: 'Unsafe'}

def get_safety_mapping():
    try:
        data = pd.read_csv(CSV_FILE_PATH)
        data.columns = data.columns.str.strip()   
        states = sorted(data['STATE/UT'].unique()) 
        safety_mapping = {state: LABEL_MAPPING[label] for state, label in zip(states, SAFETY_LABELS)}
        return safety_mapping
    except Exception as e:
        print(f"Error in generating safety mapping: {e}")
        return {}
    
def get_all_states():
    try:
         
        data = pd.read_csv(CSV_FILE_PATH)
        data.columns = data.columns.str.strip()   

         
        if 'STATE/UT' in data.columns:
            return data['STATE/UT'].drop_duplicates().sort_values().tolist()
        else:
            print("Error: 'STATE/UT' column not found in CSV file.")
            return []
    except Exception as e:
        print(f"Error in retrieving states: {e}")
        return []

def get_crime_data_for_state(state):
    try:
         
        data = pd.read_csv(CSV_FILE_PATH)
        data.columns = data.columns.str.strip()   

         
        state_data = data[data['STATE/UT'] == state]

        if state_data.empty:
            return None, None

         
        crime_counts = state_data[['Rape', 'Kidnapping and Abduction', 'Dowry Deaths', 
                                   'Assault on women with intent to outrage her modesty', 
                                   'Insult to modesty of Women', 
                                   'Cruelty by Husband or his Relatives', 
                                   'Importation of Girls']].sum()

         
        bar_chart_image = create_bar_chart(crime_counts)
        pie_chart_image = create_pie_chart(crime_counts)

         
        crime_data = crime_counts.to_dict()
        graphs = {'bar_chart': bar_chart_image, 'pie_chart': pie_chart_image}

        return crime_data, graphs
    except Exception as e:
        print(f"Error in processing data: {e}")
        return None, None

def create_bar_chart(crime_counts):
    fig, ax = plt.subplots()
    crime_counts.plot(kind='bar', ax=ax)
    ax.set_title('Crime Categories')
    ax.set_ylabel('Crime Count')


    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_b64

def create_multiline_chart(data, category_column, value_column, line_group_column):
    fig, ax = plt.subplots()

    # Pivoting data to have each group as a separate column
    pivot_data = data.pivot(index=category_column, columns=line_group_column, values=value_column)

    # Plot each column as a line
    pivot_data.plot(ax=ax)

    ax.set_title('Multi-Line Chart')
    ax.set_xlabel(category_column)
    ax.set_ylabel(value_column)
    ax.legend(title=line_group_column)

    # Save as base64 encoded image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the figure to free memory
    return img_b64
def create_pie_chart(crime_counts):
    fig, ax = plt.subplots()
    crime_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90)
    ax.set_ylabel('')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_b64 
