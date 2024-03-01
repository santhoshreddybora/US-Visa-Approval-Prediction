from US_Visa.logger import logging
from US_Visa.exception import CustomException
import sys 
from US_Visa.pipeline.training_pipeline import TrainPipeline
try :
    pipeline=TrainPipeline()
    pipeline.run_pipeline()
except Exception as e:
    raise CustomException(e,sys)