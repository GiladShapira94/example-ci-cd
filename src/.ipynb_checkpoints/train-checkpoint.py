from sklearn import ensemble
import mlrun
from mlrun.frameworks.sklearn import apply_mlrun

@mlrun.handler()
def train(context :mlrun.MLClientCtx,
    train_data: mlrun.DataItem,  # data inputs are of type DataItem (abstract the data source)
    test_data: mlrun.DataItem,  # data inputs are of type DataItem (abstract the data source)
    label_column: str = "label",
    n_estimators: int = 100,
    learning_rate: float = 0.1,
    max_depth: int = 3,
    model_name: str = "model",
):
    # Get the input dataframe (Use DataItem.as_df() to access any data source)
    df_train = train_data.as_df()
    df_test = test_data.as_df()
    
    # Initialize the x train & y train data
    X_train = df_train.drop(label_column, axis=1)
    y_train = df_train[label_column]

    # Initialize the x test & y test data
    X_test = df_test.drop(label_column, axis=1)
    y_test = df_test[label_column]
    
    # Pick an ideal ML model
    model = ensemble.GradientBoostingClassifier(
        n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth
    )

    # -------------------- The only line you need to add for MLOps -------------------------
    # Wraps the model with MLOps (test set is provided for analysis & accuracy measurements)
    apply_mlrun(model=model, model_name=model_name, x_test=X_test, y_test=y_test)
    # --------------------------------------------------------------------------------------
    context.set_label("release","v2")
    # Train the model
    model.fit(X_train, y_train)