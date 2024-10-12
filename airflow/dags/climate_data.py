from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.macros import ds_add #função que soma dias a uma data e retorna a data final
import pendulum #biblioteca para definir data específica
from os.path import join
import pandas as pd


def extrai_dados(data_interval_end):
    city = 'Boston'
    key = 'FDGPVVLMK7JLZHUTCG4P7NUJ9'
    file_path = f'/home/platero/climate_report_airflow/data/week_{data_interval_end}/'
    try:
        url = join(
            'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
            f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv'
        )
        data = pd.read_csv(url)
        data.to_csv(file_path + 'row_data.csv')
        data[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperatures.csv')
        data[['datetime', 'description', 'icon']].to_csv(file_path + 'weather.csv')
    except:
        pass


with DAG(
    'climate_data',
    start_date=pendulum.datetime(2024, 9, 30, tz='UTC'),
    schedule_interval='0 0 * * 1'
) as dag:
    task_1 = BashOperator(
        task_id = 'mkdir',
        bash_command = 'mkdir -p "/home/platero/climate_report_airflow/data/week_{{data_interval_end.strftime("%Y-%m-%d")}}"'
    )
    task_2 = PythonOperator(
        task_id = 'data_extraction',
        python_callable = extrai_dados,
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'} 
    )
    task_3 = BashOperator(
        task_id='git_update',
        bash_command=
        '''
            cd /home/platero/climate_report_airflow
            git add .
            git commit -m "Inserting data through Airflow"
            git push origin main
        '''
    )
    task_1 >> task_2 >> task_3