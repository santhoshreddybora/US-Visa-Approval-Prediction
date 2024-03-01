import numpy as np
import pandas as pd
import sys 
from US_Visa.logger import logging
from US_Visa.utils import *
from US_Visa.exception import CustomException
from US_Visa.entity.config_entity import DataIngestionConfig
from US_Visa.entity.artifact_entity import DataIngestionArtifact
from US_Visa.data_access.usvisa_data import USVisaData
import os
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        param for data ingestion config
        """
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
    def export_data_into_featurestore(self)->pd.DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info(f"Exporting data from mongo db")
            usvisa_data=USVisaData()
            dataframe=usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"data frame is strored in dataframe varaible and shape of data frame is{dataframe.shape}")
            feature_store_file_path=self.data_ingestion_config.feature_store_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info(f"Saved Exported data frame into feature store path {feature_store_file_path}")
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
    def split_data_as_train_test(self,dataframe:pd.DataFrame)->None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            
            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class")
            
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"exporting train and test files to path ")
            
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            
            logging.info(f"Exported train and test file to path ")
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_ingestion(self,)->DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try:
            dataframe=self.export_data_into_featurestore()
            logging.info("Got the data from Mongodb")
            self.split_data_as_train_test(dataframe)
            logging.info("Performed train test split on dataset")
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.test_file_path)
            logging.info(f"Data Ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        



    
        
