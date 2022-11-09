import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from sensor.constants.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from sensor.data_access.sensor_data import SensorData
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.entity.config_entity import DataIngestionConfig
from sensor.utils.main_utils import read_yaml_file
from sensor.exception import SensorException
from sensor.logger import logging

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise SensorException(e,sys)

    def export_data_into_feature_store(self) -> DataFrame:
        try:
            logging.info('Starting export of data from mongo db to csv')

            sensor_data = SensorData()

            sensor_df = sensor_data.export_collection_as_dataframe(
                collection_name = self.data_ingestion_config.collection_name)

            logging.info(f'shape of dataframe is {sensor_data.shape}')

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f'saving the dataframe in path {feature_store_file_path}')

            sensor_df.to_csv(feature_store_file_path, index=False, header=True)

            return sensor_df

        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test_split(self, dataframe: DataFrame) -> None:
        try:
            """
            Method Name :   split_data_as_train_test
            Description :   This method splits the dataframe into train set and test set based on split ratio 
            
            Output      :   Folder is created in s3 bucket
            On Failure  :   Write an exception log and then raise an exception
            
            Version     :   1.2
            Revisions   :   moved setup to cloud
            """

            logging.info('entered split_data_as_train_test_split method')
            train_set, test_set  = train_test_split(dataframe, 
                                    test_size=self.data_ingestion_config.train_test_split_ratio)
            
            train_file_path = self.data_ingestion_config.training_file_path

            test_file_path = self.data_ingestion_config.testing_file_path

            dir_path = os.path.dirname(train_file_path)

            os.makedirs(dir_path)
            
            train_set.to_csv(train_file_path, index=False, header=True)

            test_set.to_csv(test_file_path, index=False, header=True)

            logging.info(f'splitting of data into train test split is done and path is {train_file_path} and {test_file_path}')

        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """

        try:
            logging.info('entered initiate_data_ingestion_method')
            
            dataframe = self.export_data_into_feature_store()

            _schema_config = read_yaml_file(SCHEMA_FILE_PATH)

            dataframe = dataframe.drop(columns=_schema_config[SCHEMA_DROP_COLS], axis=1)

            logging.info("Got the data from mongodb")

            self.split_data_as_train_test_split(dataframe=dataframe)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)

        