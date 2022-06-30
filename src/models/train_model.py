import os
import dotenv
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

if __name__ == '__main__':

    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)

    processed_data_folder = os.getenv("PROCESSED_DATA_FOLDER")
    models_folder = os.getenv("MODELS_FOLDER")

    df = pd.read_csv('/'.join([processed_data_folder, 'dataset.csv']), index_col='id')
    df = df[df.difficulty != 0]
    y_true = df.pop('difficulty')

    X_train, X_test, y_train, y_test = train_test_split(df, y_true, random_state=0)
    regr = RandomForestRegressor(random_state=0)
    regr.fit(X_train, y_train)
    print(f"Random Forest Regressor Score: {regr.score(X_test, y_test)}")
    
    pickle.dump(regr, open( '/'.join([models_folder, 'random_forest_regressor.p']), "wb" ) )