#dataset got from : https://www.kaggle.com/c/home-data-for-ml-course/data

import  pandas as pd
from sklearn.ensemble import  RandomForestRegressor
from sklearn.metrics import mean_absolute_error

df=pd.read_csv('Input/train.csv' , index_col='Id')
df_test = pd.read_csv('Input/test.csv' , index_col='Id')

X=df.drop('SalePrice',axis=1)
y=df['SalePrice']


#for simplicity we just keep numerical vals
X=X.select_dtypes(exclude='object')



#for simplicity we just keep numerical vals
X_test=df_test.select_dtypes(exclude='object')

from sklearn.model_selection import train_test_split

X_train,X_valid,y_train,y_valid =train_test_split(X,y,train_size=0.8 ,random_state=0)


missing_values_counts=X_train.isnull().sum()
print(missing_values_counts[missing_values_counts > 0])


def score_dataset(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=10, random_state=0)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)


#approach 1:delete cols with missing vals
cols_with_missing_valuse = [col for col in X_train.columns if X_train[col].isnull().any() ]


reduced_X_train = X_train.drop(cols_with_missing_valuse,axis=1)
reduced_X_valid = X_valid.drop(cols_with_missing_valuse ,axis=1)


reduced_MAE=score_dataset(reduced_X_train,reduced_X_valid,y_train,y_valid )

print('MAE for reduced approach is:{}'.format(reduced_MAE))


#approach 2 : imputation

from sklearn.impute import SimpleImputer

my_imputer = SimpleImputer()

imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
imputed_X_valid = pd.DataFrame(my_imputer.fit_transform(X_valid))

#rename the columns
imputed_X_train.columns = X_train.columns
imputed_X_valid.columns = X_valid.columns

imputed_MAE = score_dataset(imputed_X_train,imputed_X_valid,y_train,y_valid)

print('MAE imputed approach is : {}'.format(imputed_MAE))

#select approach:
# it seems first approach is better so chose it for final prediction


X_final_train = reduced_X_train
X_final_valid = reduced_X_valid

model = RandomForestRegressor()
model.fit(X_final_train ,y_train)

pred_valid = model.predict(X_final_valid)

MAE_valid =score_dataset(X_final_train,X_final_valid,y_train,y_valid)
print('model prediction on valid set: {}'.format(MAE_valid))
#
#
# #predict on test dataset
#
# pred_test=model.predict(X_test)



