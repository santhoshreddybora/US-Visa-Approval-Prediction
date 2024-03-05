import sys

from US_Visa.cloud_storage.aws_storage import SimpleStorageService
from US_Visa.exception import CustomException 
from US_Visa.logger import logging
from US_Visa.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from US_Visa.entity.config_entity import ModelPusherConfig
from US_Visa.entity.s3_estimator import USVisaEstimator


class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact,
                 model_pusher_config:ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = USVisaEstimator(bucket_name=model_pusher_config.bucket_name,
                                model_path=model_pusher_config.s3_model_key_path)
    def initiate_model_pusher(self,)->ModelPusherArtifact:
        """
        Method Name :   initiate_model_pusher
        Description :   This function is used to initiate all steps of the model pusher
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_model_pusher method of Modelpusher class")

        try:
            logging.info("Uploading artifacts folder to s3 bucket")
            self.usvisa_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                                                        s3_model_path=self.model_pusher_config.s3_model_key_path)
            
            logging.info("Uploaded artifacts folder into s3 bucket")
            logging.info("model pusher artifact:{[model_pusher_artifact]}")
            logging.info("Exited initiate_model_pusher  method of modeltrainer class")

            return model_pusher_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
        