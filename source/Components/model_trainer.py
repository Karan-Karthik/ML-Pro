import os
import sys
from source.exception import CustomException
from source.logger import logging
from dataclasses import dataclass
from source.utils import save_object, evaluate_models

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ( AdaBoostRegressor,
                              GradientBoostingRegressor,
                              RandomForestRegressor)


@dataclass
class ModelTrainerConfig:
    trained_model_file_path= os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig

    def initiate_model_trainer(self, train_array, test_array):
        try:
            X_train, y_train, X_test, y_test= (train_array[:,:-1], train_array[:,-1], test_array[:,:-1], test_array[:,-1])
            logging.info("Split data")

            models= {"Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "AdaBoost Regressor": AdaBoostRegressor()}
            
            

            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }
            model_results:dict= evaluate_models(X_train= X_train,y_train= y_train , X_test=X_test, y_test=y_test, models=models, params=params)

            #Best Model Score
            best_model_score=max(sorted(model_results.values()))
            # Best Model name
            best_model_name= list(model_results.keys())[
                list(model_results.values()).index(best_model_score)
            ]
            best_model= models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No good model found")
            
            logging.info("Best model found on training and testing data")


            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj= best_model
            )


        except Exception as e:
            raise CustomException(e, sys)