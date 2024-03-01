import sys
import os
from US_Visa.exception import CustomException
from US_Visa.logger import logging
from US_Visa.components.data_ingestion import DataIngestion
from US_Visa.entity.config_entity import DataIngestionConfig
from US_Visa.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
    def start_data_ingestion(self)->DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component

        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def run_pipeline(self,)->None:
        """This method of TrainPipeline class is responsible for running complete pipeline"""
        try:
            data_ingestion_artifact=self.start_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys)
        
    


