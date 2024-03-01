# US-Visa-Approval-Prediction


## End to End Workflow

* 1) Template - Creating a template where the project structure is created 
* 2) Setup and Requirements installation
* 3) Logging and Exception and utility files - Log the error or any other info and raise custom expection and also utility files where common used operations where kept that
* 4) EDA and Feature Engineering - Creating a ipynb to get insights from it
* 5) 
    * i) Constants folder - Where we can assign required constants variables a value which we want to use in 
        furture
    * ii)Configuration(mongo_db_conenction.py) and Data access(usvisa_data.py) - Where we can establish a    mongo db connection and access data from the database and export collection as data frame 
    set mongo db url with your url with fllowing command in git bash. 
    
    export MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.ecs8wjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    * iii)Entity Config_entity and artifact entity - Where we create a path structure where we need to store data artifacts according to timestamp (raw ,train,test data)
    * iv)data_ingestion - Where we can initate data ingestion.Export data from mongo db to feature store path and splitting data and store in artifact ingested path 
    * v) training pipeline - Where initiation of data ingestion is started and run pipeline is created to run complete pipeline





