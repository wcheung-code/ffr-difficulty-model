import dotenv
import os
import pickle

from VerticalDensity import VerticalDensity

if __name__ == '__main__':

    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)

    raw_data_folder = os.getenv("RAW_DATA_FOLDER")

    vertical_density = VerticalDensity(alpha = 4)

    for i, filename in enumerate(os.listdir(raw_data_folder)):
        if i > 1000:
            break
        f = os.path.join(raw_data_folder, filename)
        if os.path.isfile(f) and f.endswith(".chart"):
            raw_data = pickle.load( open( f, "rb" ) )
            chart = raw_data.pop('chart')
            print(vertical_density.compute(chart))
            print(raw_data)