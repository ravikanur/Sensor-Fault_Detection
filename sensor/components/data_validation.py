import os, sys

import pandas as pd
from scipy.stats import ks_2samp

from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file, write_yaml_file

from sensor.logger import logging
from sensor.exception import SensorException

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            num_data_columns = len(dataframe.columns)
            num_req_columns = len(self._schema_config['columns'])
            logging.info(f'required number of columns {num_req_columns}')
            logging.info(f'number of data columns {num_data_columns}')
            if num_req_columns==num_data_columns:
                return True
            return False

        except Exception as e:
            raise SensorException(e,sys)

    def is_numerical_columns(self, dataframe: pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            dataframe_columns = dataframe.columns
            status = True

            missing_columns = []
            for column in dataframe_columns:
                if column not in numerical_columns:
                    status = False
                    missing_columns.append(column)

            logging.info(f'missing numericals are {missing_columns}')
            return status

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_csv(file_path: str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.5)->bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                drift = ks_2samp(d1,d2)
                if drift.pvalue >= threshold:
                    is_found = False

                else:
                    is_found = True
                    status = False
                report.update({column: {
                    'drift status':is_found,
                    'pvalue':float(drift.pvalue)
                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            dir_path = os.path.dirname(drift_report_file_path)

            write_yaml_file(report, dir_path)

            logging.info(f'saved drift report in path {dir_path}')

            return status

        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            error_message = ""

            train_df = DataValidation.read_csv(train_file_path)
            test_df = DataValidation.read_csv(test_file_path)

            status = self.validate_number_of_columns(train_df)

            if not status:
                error_message = f"{error_message}Train Dataframe does not contain all columns.\n"

            status = self.validate_number_of_columns(test_df)

            if not status:
                error_message = f"{error_message}Test Dataframe does not contain all columns.\n"

            status = self.is_numerical_columns(train_df)

            if not status:
                error_message = f"{error_message}Train Dataframe does not contain all numerical columns.\n"

            status = self.is_numerical_columns(test_df)

            if not status:
                error_message = f"{error_message}Test Dataframe does not contain all numerical columns.\n"

            if len(error_message)>0:
                raise Exception(error_message)

            status = self.detect_dataset_drift(train_df, test_df)

            data_validation_artifact = DataValidationArtifact(
                status, train_file_path, test_file_path,
                None, None, self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data Validation artifact: {data_validation_artifact}")

            return data_validation_artifact



        except Exception as e:
            raise SensorException(e, sys)

