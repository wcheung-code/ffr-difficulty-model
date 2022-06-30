# -*- coding: utf-8 -*-
import dotenv
import os

import requests as r
from ChartPreprocessor import ChartPreprocessor
from DataSerializer import DataSerializer

if __name__ == '__main__':

    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)

    api_key = os.getenv("API_KEY")
    raw_data_folder = os.getenv("RAW_DATA_FOLDER")
    os.makedirs(raw_data_folder, exist_ok = True) 
    FFR_API_URL = f'https://www.flashflashrevolution.com/api/api.php?key={api_key}&action={{}}'

    chart_preprocessor = ChartPreprocessor()
    data_serializer = DataSerializer(folder = raw_data_folder)
    song_list = r.get(FFR_API_URL.format('songlist')).json()
    response = {song['id']: dict((k, song[k]) 
        for k in ('name', 'difficulty')) for song in song_list}

    for i, (id, info) in enumerate(response.items()):        
        chart = r.get(FFR_API_URL.format(f'chart&level={id}')).json()
        info['chart'] = chart_preprocessor.preprocess(chart)
        data_serializer.download(info, id)
    
