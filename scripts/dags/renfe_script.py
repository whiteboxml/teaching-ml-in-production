###############################################################################
# IMPORTS

import argparse
import boto3
from datetime import datetime, timedelta
import joblib
import json
import logging
import pandas as pd
import requests


#########################################################################################
# ARGPARSER


def get_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--origin', type=str, required=True, help='Origin station')
    parser.add_argument('-d', '--destination', type=str, required=True, help='Destination station')
    return parser.parse_args()


###############################################################################
# PARAMETERS

# cli

args = get_cli()

ORIGIN = args.origin
DESTINATION = args.destination

# database

USER = 'workshop'
PASSWORD = 'workshop'
HOST = 'server-davidadrian.asuscomm.com'
PORT = 5433
DATABASE = 'renfe'
CONN_STRING = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

# model

ENCODER_PATH = '/home/david/Nextcloud-gurus/repos/freelance/teaching/ironhack/' \
               'ml-in-production-madrid/output/pickle_data/encoder.joblib'
ENCODER = joblib.load(ENCODER_PATH)
ENCODE_COLS = ['train_type', 'train_class', 'fare', 'origin', 'destination']
FEATURES = [
            'train_type',
            #'train_class',
            #'fare',
            'duration',
            'time_to_departure',
            'hour',
            'weekday'
            ]

ENDPOING_CLUSTERING = 'http://server-davidadrian.asuscomm.com:8926/invocations'

# AWS

ENDPOINT_XGB = 'ml-in-production-madrid-sagemaker-api-endpoint'
ENDPOINT_RF = 'ml-in-prod-mad-mlf-api-ep'
runtime = boto3.client('runtime.sagemaker')


###############################################################################
# FUNCTIONS


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = get_logger()


def mock_alarms():
    logger.info("getting (mocking) user alarms...")
    sql_query = f"""
    select * from trips tablesample system (10)
    where origin = '{ORIGIN}'
    and destination = '{DESTINATION}'
    and start_date > '{(datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")}'
    limit 100
    """

    return pd.read_sql_query(sql=sql_query, con=CONN_STRING)


def add_features(renfe_df):
    logger.info("adding new features...")
    renfe_df['duration'] = (renfe_df['end_date'] - renfe_df['start_date']).dt.seconds / 3600
    renfe_df['time_to_departure'] = (renfe_df['start_date'].dt.tz_localize('Europe/Madrid').dt.tz_convert('UTC') \
                                     - renfe_df['insert_date'].dt.tz_localize('UTC')).dt.days
    renfe_df['hour'] = renfe_df['start_date'].dt.hour
    renfe_df['weekday'] = renfe_df['start_date'].dt.dayofweek


def preprocessing(renfe_df):
    logger.info("preprocessing data...")
    renfe_df.dropna(inplace=True)
    add_features(renfe_df)
    renfe_df.loc[:, ENCODE_COLS] = ENCODER.transform(renfe_df[ENCODE_COLS])


def get_forecast(renfe_df, model):
    logger.info('calling endpoint...')

    if model == 'xgb':
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_XGB,
                                           Body=renfe_df.to_csv(header=False,
                                                                index=False))
        y_pred = list(map(lambda x: float(x), response['Body'].read().decode().split(',')))
        return y_pred

    elif model == 'rf':
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_RF,
                                           ContentType='application/json',
                                           Body=renfe_df.to_json(orient='split'))

        y_pred = json.loads(response['Body'].read().decode())
        return y_pred

    elif model == 'clustering':

        headers = {
            'Content-Type': 'application/json',
        }

        r = requests.post(url=ENDPOING_CLUSTERING,
                          headers=headers,
                          data=renfe_df.to_json(orient='split'))

        y_pred = [int(x) for x in r.text if x.isdigit()]
        return y_pred


###############################################################################
# MAIN

if __name__ == '__main__':
    alarms = mock_alarms()
    preprocessing(alarms)

    for alarm in alarms.itertuples():
        logger.info(f"forecasting price for ticket from {ORIGIN} to {DESTINATION} with "
                    f"alarm price: {alarm.price}...")

        predict_df = pd.DataFrame({
            'train_type': alarm.train_type,
            'duration': alarm.duration,
            'time_to_departure': range(1, alarm.time_to_departure),
            'hour': alarm.hour,
            'weekday': alarm.weekday
        })

        forecast_xgb = get_forecast(predict_df, model='xgb')
        forecast_rf = get_forecast(predict_df, model='rf')

        logger.info('----------------------------------------------------------')
        logger.info(f'current price is: {alarm.price}')
        logger.info('----------------------------------------------------------')
        logger.info(f'max price predicted by xgb model is: {max(forecast_xgb)}')
        logger.info(f'min price predicted by xgb model is: {min(forecast_xgb)}')
        logger.info('----------------------------------------------------------')
        logger.info(f'max price predicted by rf model is: {max(forecast_rf)}')
        logger.info(f'min price predicted by rf model is: {min(forecast_rf)}')
        logger.info('----------------------------------------------------------')
