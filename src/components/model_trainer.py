import os
import sys
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object , evaluate_model

from sklearn.linear_model import LinearRegression , Lasso , Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor
)
from catboost import CatBoostRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts" , "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self , train_array , test_array):
        try:
            logging.info("Splitting Training and test input data")
            X_train ,y_train , X_test, y_test = (
                train_array[:,:-1,],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "linear model" : LinearRegression(),
                "lasso" : Lasso(),
                "ridge" : Ridge(),
                "KNN" : KNeighborsRegressor(),
                "Decision Tree" : DecisionTreeRegressor(),
                "AdaBoost Regressor" : AdaBoostRegressor(),
                "Random Forest Regressor" : RandomForestRegressor(),
                "Gradient Boosting Regressor" : GradientBoostingRegressor(),
                "Cat Boost Regressor" : CatBoostRegressor(),
                "XGB Regresoor" : XGBRegressor()
            }

            model_report:dict = evaluate_model(
                X_train = X_train,
                y_train = y_train,
                X_test = X_test,
                y_test = y_test,
                models = models
                )
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6 :
                raise CustomException("No Best Model Found.")
            
            logging.info(f"Best Model Found on Training and Test DataSet:")
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                object=best_model
            )

            predicted = best_model.predict(X_test)
            r2score = r2_score(y_test , predicted)
            return r2score


        except Exception as e:
            raise CustomException(e , sys)