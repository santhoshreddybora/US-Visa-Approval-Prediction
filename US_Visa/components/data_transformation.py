import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer

from US_Visa.constants import TARGET_COLUMN,SCHEMA_FILE_PATH,CURRENT_YEAR
from US_Visa.entity.config_entity import DataTransformationConfig
from US_Visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from US_Visa.exception import CustomException
from US_Visa.logger import logging
from US_Visa.utils.main_utils import save_object, save_numpy_array_data, read_yaml, drop_columns
from US_Visa.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
            self._schema_config=read_yaml(filepath=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Exception(e,sys)
    
    def get_data_transformer_object(self)->Pipeline:
        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object for the data
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )
        try:
            logging.info("Got Numerical columns from schema config")
            numeric_transformer=StandardScaler()
            oh_transformer=OneHotEncoder()
            or_transformer=OrdinalEncoder()
            logging.info("Initialize StandardScaler, onehot encoder,ordinal encoder")

            oh_columns=self._schema_config['oh_columns']
            or_columns=self._schema_config['or_columns']
            transform_columns=self._schema_config['transform_columns']
            num_features=self._schema_config['num_features']

            logging.info("Initialize Power Transformer")

            Transform_pipe=Pipeline([
                ('Power Transformer',PowerTransformer(method='yeo-johnson'))
                                     ])

            preprocessor=ColumnTransformer([
                ('OnehotEncoder',oh_transformer,oh_columns),
                ('OrdinalEncoder',or_transformer,or_columns),
                ('PowerTransformer',Transform_pipe,transform_columns),
                ('StandardScaler',numeric_transformer,num_features)
            ])

            logging.info(f"Created Preprocessor object from columntransformer")

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation component for the pipeline 
        
        Output      :   data transformer steps are performed and preprocessor object is created  
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info(f"Starting data transformation")
                preprocessor=self.get_data_transformer_object()
                logging.info(f"Got preprocessor object")

                train_df=DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df=DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

                input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_train_df=train_df[TARGET_COLUMN]

                logging.info("Got train features of Training dataset")

                input_feature_train_df['company_age'] = CURRENT_YEAR-input_feature_train_df['yr_of_estab']

                logging.info("Added company_age column to the Training dataset")

                drop_cols = self._schema_config['drop_columns']

                logging.info("drop the columns in drop_cols of Training dataset")

                input_feature_train_df = drop_columns(df=input_feature_train_df, cols = drop_cols)
                
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )

                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                logging.info("Got test features of Testing dataset")

                input_feature_test_df['company_age'] = CURRENT_YEAR-input_feature_test_df['yr_of_estab']

                logging.info("Added company_age column to the Test dataset")

                drop_cols = self._schema_config['drop_columns']

                logging.info("drop the columns in drop_cols of Test dataset")

                input_feature_test_df = drop_columns(df=input_feature_test_df, cols = drop_cols)
                
                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )
                logging.info("Got train features and test features of Testing dataset")

                logging.info(
                    "Applying preprocessing object on training dataframe and testing dataframe"
                )

                input_feature_train_arr=preprocessor.fit_transform(input_feature_train_df)
                logging.info(
                    "Used the preprocessor object to fit transform the train features"
                )

                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info("Used the preprocessor object to transform the test features")

                logging.info(f"Applying SMOTEENN on Training dataset")
                smt=SMOTEENN(sampling_strategy='minority')

                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )

                logging.info("Applied SMOTEENN on training dataset")

                input_feature_test_final,target_feature_test_final=smt.fit_resample(
                    input_feature_test_arr,target_feature_test_df)
                logging.info("Applied SMOTEENN on Test dataset")
                logging.info("Created train array and test array")
                train_arr=np.c_[input_feature_train_final,np.array(target_feature_train_final)]
                test_arr=np.c_[input_feature_test_final,np.array(target_feature_test_final)]

                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info("Saved the preprocessor object")

                logging.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                )

                data_transformation_artifact=DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )

                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)
        except Exception as e:
            raise CustomException(e,sys)


                
