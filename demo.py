from US_Visa.logger import logging
from US_Visa.exception import CustomException
import sys 

try :
    s=1/'0'
    logging.info('Exception testing')
except Exception as e:
    logging.info(e)
    raise CustomException(e,sys)  