"""Machine learning functions"""

import logging
import random
import numpy as np 
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    zipcode: int = Field(..., example=99205)
    family_members: int = Field(..., example= 4)
    income: int = Field(..., example= 4000)

    #def to_df(self):
       # """Convert pydantic object to pandas dataframe with 1 row."""
        #return pd.DataFrame([dict(self)])

    #@validator('x1')
    #def x1_must_be_positive(cls, value):
        #"""Validate that x1 is a positive number."""
        #assert value > 0, f'x1 == {value}, must be > 0'
        #return value

@router.post('/predict')
#async def predict(item: Item):
async def determine_eligibility(item: Item):

    zips = pd.read_csv('app/spokane_zipcodes.csv')

    user = zips[zips['zipcode'] == item.zipcode]
    user = user[user['family_members'] == item.family_members]
    user_income = item.income*12
    comp_income = user['annual_income'].astype(np.int32)
        
    if (user_income <= user['annual_income']).all():
        results =  'You Qualify!'
    else:
        results = 'Application Pending - income exceeds limit'

    #X_new = item.to(_df()
    #log.info(X_new)
    #y_pred = random.choice([True, False])
    #y_pred_proba = random.random() / 2 + 0.5
    return {
        #'prediction': y_pred,
        #'probability': y_pred_proba
        'eligibility': results
    }
