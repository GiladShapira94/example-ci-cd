
from sklearn.datasets import make_classification
import pandas as pd
from sklearn.model_selection import train_test_split

def data_fetch(context):
    # creating data
    x,y = make_classification()
    
    # spliting the data to train and test data sets
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,train_size=0.8)
    
    #creating train dataframe
    x_train_df = pd.DataFrame(x_train)
    y_train_df = pd.DataFrame(y_train,columns=['label'])
    df_train = pd.concat([x_train_df,y_train_df],axis=1)
    
    #creating train dataframe
    x_test_df = pd.DataFrame(x_test)
    y_test_df = pd.DataFrame(y_test,columns=['label'])
    df_test = pd.concat([x_test_df,y_test_df],axis=1)
    context.set_label("release","v2")
    return df_train,df_test
