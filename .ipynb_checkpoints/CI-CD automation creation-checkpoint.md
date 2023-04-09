
# Create CI/CD Automation Using - Git source example

This example shows how to create a project in MLRun for CI/CD Automation
based on a remote source e.g git - this process is equivalent for using
tar.gz, zip archive files.

After this example you will learn how to:

-   Create a new MLRun project
-   Set a project remote or archive source
-   Run and set MLRun functions using git source code
-   Run and set MLRun workflow
-   Set and register MLRun artifacts
-   Create and save project YAML
-   Push and Manage your git repo or archive file

Install mlrun - if mlrun does not installed use
`pip install mlrun==<mlrun server version>` or `sh align_mlrun.sh` (our
default mlrun installer - automatically install the server version)

``` python
import mlrun
```

MLRun provides you three option to create or loading a project:

1.  [get_or_create_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=get_or_create_project#mlrun.projects.get_or_create_project) -
    this method allows you to load a project from MLRun DB or optionally
    load it from a yaml/zip/tar/git template, and create a new project
    if doesnt exist
2.  [new_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=new_project#mlrun.projects.new_project) -
    Create a new MLRun project, optionally load it from a
    yaml/zip/tar/git template.
3.  [load_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=load_project#mlrun.projects.load_project) -
    Load an MLRun project from yaml/zip/tar/git/dir or from MLRun db

**Note -** for loading a project you must have a project.yaml file that
may include all the relevant metadata such as funciton, workflows and
artifacts in your repo/archive file or to have the project stored in
MLRun DB.

### Creating a project


This example demostrate how to create a project for CI/CD when:

1.  you need to test you code in local mode - clone the files before
    running this notebook
2.  you have python code files that are ready to run in your remote or
    archive source
3.  you do not have project yaml file in your remote or archive source -
    a new project is created

``` python
#creating a new project or load it from DB
project = mlrun.get_or_create_project(name='new-git-proj',context='./',init_git=True)
```


**name -** project name


**context -** project local directory path (default value = \"./\")


**init git -** if True, will git init the context dir


When you create a new project MLRun create a light project YAML, for
example:

    kind: project
    metadata:
      name: new-git-proj
      created: '2022-06-30T09:41:05.612000'
    spec:
      functions: []
      workflows: []
      artifacts: []
      desired_state: online
    status:
      state: online

For update project YAML use **projec.save()**


**Secrets -** for working with private repo you need to provide a Git
token as a secrets using mlrun or mlrun UI, for example:

    #while loading from private repo
    project = mlrun.get_or_create_project(name='new-git-proj',context='./',init_git=True,secrest={"GIT_TOKEN":<github-token>})
    #while running functions in a project from a private repo
    project.set_secrets({"GIT_TOKEN":<github-token>}


### Set a project remote or archive source


To point the project to a specific source you need to set a project
source using
[project.set_source](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=set_source#mlrun.projects.MlrunProject.set_source)
method in addition you can set the pull_at_runtime (e.g
load_source_on_run) flag value and the project working dir.

This method will add the source,pull_at_runtime and the project working
dir to the project.yaml and will copy to the functions spec when setting
with_repo=True in the set_function method (will explain better in
details).


**Note -** Please add git branch or refs to the source e.g.:
\'<git://>`<url>`{=html}/org/repo.git#\<branch-name or refs/heads/..\>\'


``` python
source = 'git://github.com/GiladShapira94/example-ci-cd.git#master'
```

``` python
project.set_source(source=source,pull_at_runtime=True)
```


**pull_at_runtime -** flag will determine if the code is loaded in
runtime to the k8s pod or added to the image during build or function
deployment. the first (at runtime) option is better for debugging while
the secound is better for production. Note that if you choose the 2nd
option you\'ll need to build the function before run using the
[build_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=build_function#mlrun.projects.build_function)
method, This method allows you to build a new image based on your job
requirements or custom attributes - this method.


### Run and set MLRun functions using git source code


For the first time you are working with a remote or an archive source
code e.g git or zip file with MLRun, the first thing you want to do is
to clone or extract your files to the project context to start
developing and run your function in MLRun (for running function in local
your files must be stored in the project context folder e.g
./project-context or set the absulte file path).

If you have files that are allready competibile to run with MLRun in
remote you do not need to clone or extarct the files.


#### Set MLRun functions to the project


For functions definations use the
[project.set_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=set_function#mlrun.projects.MlrunProject.set_function)
method.

The **set_function** method allow you to set the functions attributes in
the project YAML, for example: function source (YAML, py, ipynb,
function object) , name of the fucntion, function handler, function
image,function kind and function requirmnets.

**Note -** Most of the time we will store the code source file under a
folder named src in the project context e.g
./project-context/src/data_fetch.py


#### First examle - Not using GitHub source


Most of the scenirios the first time a user will work with MLRun he will
need to test his code MLRun for this scenirio see the below example:

1.  Clone and extract the code files to the project context and use
    those files to run the function in local and remote (the function
    will not use the source),do not set with_repo=True in the
    set_function method


```
    project.set_function(func='function.py
        name="training", handler="model_training",
        image="mlrun/mlrun", kind="job"
    )
```

**Note -** in this example becuase you are not working with the project
source you do won\'t needed to push or create a new archive file after
every code change.


#### Second examle - using GitHub source

This example is shows and exmaple of the first option - clone and run in
local and from remote


After your first development you would want use your project source to
run your function in remote (when running from remote the function will
run the files that stored in your repo or archive files), can see below
example:

1.  Clone and extract the code files and use the local files to run in
    local and the remote source for running in remote (those function
    will use the project source for running in remote), to do this add
    with_repo=True in the set_function method.

```
    project.set_function(func='function.py
        name="training", handler="model_training",
        image="mlrun/mlrun", kind="job",with_repo=True
    )
```

1.  Run function from remote source and not in local, to do this add
    with_repo=True and you can use the relative handler
    (folder_name.file_name.function_handler) and then you do need to
    point the a python code file.

```
    project.set_function(name="training", 
        handler="function.model_training",
        image="mlrun/mlrun", kind="job",with_repo=True
    )
```

**Note -** in those examples you will need to push or create a new
archive file after every code change for those changes to take affect
when running function in remote.


> Set the with_repo=True to add the entire repo code into the
> destination container during build or run time.

> When using with_repo=True the functions need to be deployed
> (function.deploy()) to build a container, unless you set
> project.set_source(source=source,pull_at_runtime=True) which instructs
> MLRun to load the git/archive repo into the function container at run
> time and do not require a build (this is simpler when developing, for
> production it's preferred to build the image with the code)


**Fetch Data function**


``` python
# Set data_fetch function to the project.yaml file
project.set_function(func='./src/data_fetch.py',name='data-fetch',handler='data_fetch',kind='job',image='mlrun/mlrun',with_repo=True)
```


**Run Fucntion**

-   For getting a function after you set a function in the project, you
    can use
    [get_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=get_function#mlrun.projects.MlrunProject.get_function)
    method.

**Note -** The get_function allows the user to get function object and
change the funciton spec for example function resources and saved those
change in the project object cashe, then when the user will run the
function it will include those changes

    data_fetch_func = mlrun.get_function('data-fetch')
    data_fetch_func.with_requests(mem='1G',cpu=3)
    data_fetch_run = project.run_function('data-fetch')

-   For running functions in a project you can use the
    [run_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=run_function#mlrun.projects.run_function)
    method, This method allows you to run a MLRun jobs locally and
    remotely as long as there is no requirments ( if there is any
    requirments you will need to build a new image before you run a
    function) It is equivalent to func.run method.

-   For building function image you can use the
    [build_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=build_function#mlrun.projects.build_function)
    method, This method allows you to build a new image based on your
    job requirements or custom attributes - this method it only for non
    remote function for example MLRun jobs. It is equivalent to
    func.deploy() method.

```
    project.build_function('<function name>')
```

-   For deploy remote function e.g serving and nuclio kinds you can use
    [deploy_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=deploy_function#mlrun.projects.deploy_function)
    method.


**Run in local - use the code files from the local folder**


``` python
data_fetch_run = project.run_function(function='data-fetch',returns=['train-dataset','test-dataset'],local=True)
```

**Run in Remote - use the code files from the remote source**


``` python
data_fetch_run = project.run_function(function='data-fetch',returns=['train-dataset','test-dataset'],local=False)
```

**Train function**


``` python
project.set_function(func='./src/train.py',name='train',handler='train',kind='job',image='mlrun/mlrun',with_repo=True)
```

``` python
train_run = project.run_function(function='train',inputs={'train_data':data_fetch_run.outputs['train-dataset'],'test_data':data_fetch_run.outputs['test-dataset']})
```

**Serving Function**

``` python
# Create a serving function object
serving = mlrun.new_function(name="serving", kind="serving", image="mlrun/mlrun")

# Add a model to the model serving function object
serving.add_model(key='model',model_path=train_run.outputs["model"], class_name='mlrun.frameworks.sklearn.SklearnModelServer')
```




``` python
# save the function definition into a .yaml file and register it in the project
serving.export(target=f"./{project.context}/src/serving.yaml")
project.set_function(func="./src/serving.yaml", name="serving")
```

#### Speciel Cases



When creating a project for CI/CD there are speciel cases you need to
take in consider, see the list below:

1.  When creating a serving function the function spec contain metadata
    of the function steps or the function models, becuase of it you need
    to create a function.yaml file by using the
    - [export()](https://docs.mlrun.org/en/latest/api/mlrun.runtimes.html?highlight=export#mlrun.runtimes.BaseRuntime.export)
    method after you are creating the function object and then set the
    function with this yaml file, with this approach all the function
    spec will be saved for future deployments.

For Example:

    <function object>.export('./model_training.yaml')

    project.set_function(
        func="training.yaml",name='training',with_repo=True,kind='serving')

1.  In addition to the first point if you want to change the defualt
    funciton spec values e.g resources, node-selector and more, and make
    this change constant you will need to create a yaml function and
    point use the yaml function in the set_fucntion method.
2.  When set a nuclio function the function handler is a combination of
    the file_name::function_handler, for example:

```
    project.set_function(name='nuclio',handler='multi:multi_3',kind='nuclio',image='mlrun/mlrun',with_repo=True)


``` python
serving_func = project.deploy_function(function='serving',models=[{'key':'model','model_path':train_run.outputs["model"], 'class_name':'mlrun.frameworks.sklearn.SklearnModelServer'}])
```
### Run and set MLRun workflow

After you develop your functions in our example we build 3 function
(data_fetch, training and serving) we will want to create a workflow
that run those function one by one, for more information about workflow
you can check -
[link](https://docs.mlrun.org/en/stable/projects/build-run-workflows-pipelines.html).

First thing to do is create a workflow.py file, for example:

    %%writefile pipelines/training_pipeline.py
    from kfp import dsl
    import mlrun

    @dsl.pipeline(
        name="batch-pipeline-academy",
        description="Example of batch pipeline for Iguazio Academy"
    )
    def pipeline(label_column: str, test_size=0.2):
        
        # Ingest the data set
        ingest = mlrun.run_function(
            'get-data',
            handler='prep_data',
            params={'label_column': label_column},
            outputs=["iris_dataset"]
        )
        
        # Train a model   
        train = mlrun.run_function(
            "train-model",
            handler="train_model",
            inputs={"dataset": ingest.outputs["iris_dataset"]},
            params={
                "label_column": label_column,
                "test_size" : test_size
            },
            outputs=['model']
        )
        
        # Deploy the model as a serverless function
        deploy = mlrun.deploy_function(
            "deploy-model",
            models=[{"key": "model", "model_path": train.outputs["model"]}]
        )


**Set workflow**

To set workflow to the project you need to use
[project.set_workflow](https://docs.mlrun.org/en/stable/api/mlrun.projects.html?highlight=set_workflow#mlrun.projects.MlrunProject.set_workflow)
method, this method add or update a workflow, specify a name and the
code path in the project.yaml file


In this example we added a workflow named main that point to a file
located ./project-context/src/workflow.py


``` python
project.set_workflow('main','./src/workflow.py')
```

To run the workflow you can use
[project.run](https://docs.mlrun.org/en/stable/api/mlrun.projects.html?highlight=run#mlrun.projects.MlrunProject.run)
method, this method allow you to run a workflow or shceudle a workflow
using kubeflow pipelines by specifing the workflow name or the workflow
file path. This workflow will run all the functinos you set in to the
project


**Run workflow**


``` python
# run workflow named main and wait for pipeline completion (watch=True)
project.run('main',watch=True)
```

**Run Schedule workflow**

For more inforation about scheduling workflows, please check this
[link](https://docs.mlrun.org/en/latest/concepts/scheduled-jobs.html)


### Set and register MLRun artifacts


For set artfiacts to the project you can use the
[project.set_artifact](https://docs.mlrun.org/en/stable/api/mlrun.projects.html?highlight=set_artifact#mlrun.projects.MlrunProject.set_artifact)
method, this method allows you to add/set an artifact in the project
spec (will be registered on load).

In general you will want to use this method when you will want to
register the artifact when you load the project for example:

-   Develop a model artifact in development system and you want to use
    this model file in production
-   Artifacts you want to register by defualt when you load or create a
    project

**Note -** To register artifact between difrrent environments e.g dev
and prod you must upload your artifacts to a remote storage e.g s3,you
can change your project artifact path using mlrun or mlrun ui

    project.artifact_path='s3:<bucket-name/..'


**Set a model artifact**


``` python
# get model obejct to register
model_obj = project.get_artifact('model')
```

``` python
#print target path
print(model_obj.target_path)
```

    v3io:///projects/new-git-proj/artifacts/cb0cc3d2-317c-483b-afdd-1b66acbaec8a/train/0/model/


``` python
#print model file
model_obj.model_file
```

    'model.pkl'

``` python
# set model artifact to the project
project.set_artifact(key='model-test',artifact=mlrun.artifacts.ModelArtifact(model_file=model_obj.model_file),target_path=model_obj.target_path)
```

**Note -** by default the artifact type is equal to
mlrun.artifacts.Artifact() for specifing difrrent types you need to
forward the relvant artifact object (then you can specify specific
paramtest to the artifcat object type), see below list:

        "dir": mlrun.artifacts.DirArtifact,
        "link": mlrun.artifacts.LinkArtifact,
        "plot": mlrun.artifacts.PlotArtifact,
        "chart": mlrun.artifacts.ChartArtifact,
        "table": mlrun.artifacts.TableArtifact,
        "model": mlrun.artifacts.ModelArtifact,
        "dataset": mlrun.artifacts.DatasetArtifact,
        "plotly": mlrun.artifacts.PlotlyArtifact,
        "bokeh": mlrun.artifacts.BokehArtifact,


**Spicial Cases -**

-   When MLRun creating an artifact there are values that are proccesed
    in runtime e.g dataset preview or model metrics, those values are
    stored in the artifact spec, if you wish to store the artifact spec
    for registring the artifact with those values you will need to
    export the artifcat object and set the artifact.yaml file, see below
    example:


```
    model_obj = project.get_artifact('model')
    model_obj.export(./model_artifact.yaml)
    project.set_artifact(key='model',artifact='./model_artifact.yaml')

```

### Create and save project YAML


The project YAML contains metadata about the project for example you can
see that the project yaml contains all the function we set to the
project, the artifact and the workflow, and then when you will load the
project it will loaded with all those functions, artifact and workflow.

In general MLRun uses those metadata to create object for examples
funciton obejects and then use those objects to run the functions.

``` python
print(project.to_yaml())
```

 {.output .stream .stdout}
    kind: project
    metadata:
      name: new-git-proj
    spec:
      functions:
      - url: ./src/data_fetch.py
        name: data-fetch
        kind: job
        image: mlrun/mlrun
        handler: data_fetch
        with_repo: true
      - url: ./src/train.py
        name: train
        kind: job
        image: mlrun/mlrun
        handler: train
        with_repo: true
      - url: ./src/serving.yaml
        name: serving
      workflows:
      - path: ./src/workflow.py
        name: main
      artifacts:
      - kind: model
        metadata:
          project: new-git-proj
          key: model-test
        spec:
          target_path: v3io:///projects/new-git-proj/artifacts/cb0cc3d2-317c-483b-afdd-1b66acbaec8a/train/0/model/
          model_file: model.pkl
        status:
          state: created
      conda: ''
      source: git://github.com/GiladShapira94/example-ci-cd.git#master
      origin_url: git://github.com/GiladShapira94/example-ci-cd.git#refs/heads/master
      load_source_on_run: true
      desired_state: online


To export the project content to yaml file and save project in database
the
[save](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=save#mlrun.projects.MlrunProject.save)
method.


``` python
project.save()
```

    <mlrun.projects.project.MlrunProject at 0x7fe33c1cd990>



### Push and Manage your git repo or archive file


**Create a git remote**

If you do not clone any files and you do not have any git remotes
configured you can use
[project.create_remote](https://docs.mlrun.org/en/stable/api/mlrun.projects.html?highlight=create_remote#mlrun.projects.MlrunProject.create_remote)
this method creates git remote and add the remote to the project as the
project source.

for exmaple:

    project.create_remote(url='https://github.com/mlrun/example-ci-cd.git',name='mlrun-remote',branch='master')


**Push changes to git repo**

After you made changes in your code you will want to push your project
context to GitHub repo, for this you can use
[project.push](https://docs.mlrun.org/en/stable/api/mlrun.projects.html?highlight=push#mlrun.projects.MlrunProject.push)

    project.push(branch='master',message='update',add=['project.yaml','./src/data_fetch.py','./src/serving.yaml','./src/train.py','./src/workflow.py'])


### Done!

**Now you have a project YAML for CI/CD Automation - Later we will
demostrate how to load a project and use this Project YAML**

