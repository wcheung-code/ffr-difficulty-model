import os
import dotenv
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

if __name__ == '__main__':

    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)
    
    raw_data_folder = os.getenv("RAW_DATA_FOLDER")
    processed_data_folder = os.getenv("PROCESSED_DATA_FOLDER")
    models_folder = os.getenv("MODELS_FOLDER")
    output_data_folder = os.getenv("OUTPUT_DATA_FOLDER")

    df = pd.read_csv('/'.join([processed_data_folder, 'dataset.csv']), index_col='id')
    y_true = df.pop('difficulty')
    regr = pickle.load(open( '/'.join([models_folder, 'random_forest_regressor.p']), "rb" ))

    results = pd.DataFrame(index=df.index)
    names = np.array([])

    for i, row in results.iterrows():
        raw_data_path = '/'.join([raw_data_folder, str(i).zfill(4) + '.chart'])
        raw_data = pickle.load(open(raw_data_path, "rb"))
        names = np.append(names, np.array(raw_data['name']))
    
    results['name'] = names
    results['actual_diff'] = y_true
    results['pred_diff'] = regr.predict(df)

    os.makedirs(output_data_folder, exist_ok=True)  
    results.to_csv('/'.join([output_data_folder, 'results.csv']), index=False)