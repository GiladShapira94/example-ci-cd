from kfp import dsl
import mlrun

@dsl.pipeline(
    name="CI/CD tutorial",
    description="Workflow Example as part of iguazio CI/CD tutorial"
)
def pipeline():
    
    # Ingest the data set
    data_fetch = mlrun.run_function(
        'data-fetch',returns=['train-dataset','test-dataset'],
        outputs=['train-dataset','test-dataset']
    )
    
    # Train a model   
    train = mlrun.run_function(
        "train",
        inputs={'train_data':data_fetch.outputs['train-dataset'],'test_data':data_fetch.outputs['test-dataset']},
        outputs=['model']
    )
    
    # Deploy the model as a serverless function
    deploy = mlrun.deploy_function(
        "serving",
        models=[{'key':'model','model_path':train.outputs["model"], 'class_name':'mlrun.frameworks.sklearn.SklearnModelServer'},tag="v2"]
    )