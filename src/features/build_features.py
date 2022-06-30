import dotenv
import os
import pickle
import csv

from HorizontalDensity import HorizontalDensity
from VerticalDensity import VerticalDensity

if __name__ == '__main__':

    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)
    raw_data_folder = os.getenv("RAW_DATA_FOLDER")
    processed_data_folder = os.getenv("PROCESSED_DATA_FOLDER")
    os.makedirs(processed_data_folder, exist_ok = True) 

    vertical_density = VerticalDensity(alpha = 3)
    horizontal_density = HorizontalDensity(alpha = 3)

    fields = [ 'id', 'difficulty', 'nps', 'length',
          'L', 'D', 'U', 'R', 'left', 'right', 'all']

    with open('/'.join([processed_data_folder, 'dataset.csv']), 'w') as f:
        w = csv.DictWriter( f, fields )
        w.writeheader()
        for filename in os.listdir(raw_data_folder):
            f = os.path.join(raw_data_folder, filename)
            if os.path.isfile(f) and f.endswith(".chart"):
                raw_data = pickle.load( open( f, "rb" ) )
                chart = raw_data.pop('chart')
                raw_data['vertical'] = vertical_density.compute(chart)
                raw_data['horizontal'] = horizontal_density.compute(chart)

            row = {'id': int(filename.split('.')[0])}
            for feature, val in sorted(raw_data.items()):
                if isinstance(val, dict):
                    row.update(val)
                elif feature != 'name':
                    row[feature] = val
                else:
                    pass
            w.writerow(row)
