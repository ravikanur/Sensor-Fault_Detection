import sys

from sensor.components.data_ingestion import DataIngestion
from sensor.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelEvaluationConfig,
    ModelPusherConfig,
    ModelTrainerConfig,
)
from sensor.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelEvaluationArtifact,
    ModelTrainerArtifact,
)
from sensor.logger import logging
from sensor.exception import SensorException

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

        self.data_validation_config = DataValidationConfig()

        self.data_transformation_config = DataTransformationConfig()

        self.model_trainer_config = ModelTrainerConfig()

        self.model_evaluation_config = ModelEvaluationConfig()

        self.model_pusher_config = ModelPusherConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            """
            """
            logging.info('Entered start_data_ingestion method in train_pipeline class')

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info('got the train test split')

            logging.info('exited the start_data_ingestion method of train pipeline class')

            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)