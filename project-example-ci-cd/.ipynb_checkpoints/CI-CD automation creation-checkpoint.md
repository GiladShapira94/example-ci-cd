# CI/CD Automation Using - Git, Zip, Tar source 

MLRun provides you three option to create or loading a project:

1. [get_or_create_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=get_or_create_project#mlrun.projects.get_or_create_project) - this method allows you to load a project from MLRun DB or optionally load it from a yaml/zip/tar/git template, or create/import if doesnt exist
2. [new_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=new_project#mlrun.projects.new_project) - Create a new MLRun project, optionally load it from a yaml/zip/tar/git template.
3. [load_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=load_project#mlrun.projects.load_project) - Load an MLRun project from yaml/zip/tar/git/dir or from MLRun db

### Project YAML
Project YAML allows users to define thier project metadata for loading a project and deploy and run a functions.

In the Project YAML you can define:
* Functions 
* Workflow
* Artifacts
* Source 
On project creation MLRun create a light project YAML, for example: 
````
kind: project
metadata:
  name: default
  created: '2022-06-30T09:41:05.612000'
spec:
  functions: []
  workflows: []
  artifacts: []
  desired_state: online
status:
  state: online
````
For update project YAML use projec.save()

On this section we will cover how to define each topic from the list above and provide an end to end example.

### Functions
For functions definations use the [set_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=set_function#mlrun.projects.MlrunProject.set_function) method.

The **set_function** method allow you to set the functions attributes in the project YAML, for example: 
function source (YAML, py, ipynb, function object) , name of the fucntion, function handler, function image and function kind.

````
project.set_function(
    name="training", handler="training.model_training",
    image="mlrun/mlrun", kind="job", with_repo=True,
)
````
> Set the with_repo=True to add the entire repo code into the destination container during build or run time. 

> When using with_repo=True the functions need to be deployed (function.deploy()) to build a container, unless you set project.spec.load_source_on_run=True which instructs MLRun to load the git/archive repo into the function container at run time and do not require a build (this is simpler when developing, for production it’s preferred to build the image with the code)

**Important Note -** Remote functions as Serving need a function YAML as a source or function object
Before you creating fucntion YAML you need to the create a fucntion object you can do it with [code_to_function()](https://docs.mlrun.org/en/latest/api/mlrun.html?highlight=code_to_function#mlrun.code_to_function), [new_function()](https://docs.mlrun.org/en/latest/api/mlrun.run.html?highlight=new_function#mlrun.run.new_function).

After you creating a function object you can use the [export()](https://docs.mlrun.org/en/latest/api/mlrun.runtimes.html?highlight=export#mlrun.runtimes.BaseRuntime.export) method, For Example:
````
<function object>.export('./model_training.yaml')
````

````
project.set_function(
    func="training.yaml",name='training',with_repo=True,kind='serving')
````

### Artifacts
For Artifacts Defenition use [set_artifact()](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=set_artifact#mlrun.projects.MlrunProject.set_artifact) method.

The set_artifact() method allow you to add artifacts to the project spec that will be registered on load.

**Important Note -** The artifacts need to be store in a remote storage. 

````
# register a simple file artifact
project.set_artifact('data', target_path=data_url)
````
There are 3 objects for register artifacts - 
* Model - ModelArtifact
* Dataset - DatasetArtifact
* Simple Artifact - Artifact

````
# register a model artifact
project.set_artifact('model', ModelArtifact(model_file="model.pkl"), target_path=model_dir_url)

# register a path to artifact package (will be imported on project load)
project.set_artifact('model', 'https://mystuff.com/models/mymodel.zip')
````
You can use the export() method to save the artifact object into a yaml/json file or zip archive
````
<artifcat object>.export('./model.yaml')

````
### Workflow
For workflow defenition use [set_workflow()](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=set_workflow#mlrun.projects.MlrunProject.set_workflow) method.

The set_workflow() method alows user to add or update a workflow into the project spec , specify a name and the code path.

````
project.set_workflow('main', 'workflow.py', embed=True)
````
**Remember -** After you complete to update/edit the project YAML, run `project.save()` 

For example how to create a new project and build an project YAML you can see  - create_project example
