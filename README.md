# Load project YAML from - Git, Zip, Tar source

After you create your project YAML you can simply load that project and run, build and deploy your function.
You can found an addional information of how to create a project YAML for CI/CD [here](https://github.com/GiladShapira94/load-project-example/blob/master/CI-CD%20automation%20creation.md)

In this session you would learn how to:
* Load or Create a new project for remote URL
* get a function object 
* run a function
* build a function
* deploy a function
* run a workflow

#### Load or Create a new project
For loading a project you can use :
1. [load_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=load_project#mlrun.projects.load_project) thats Load an MLRun project from git or tar or dir 
````
# load the project and run the 'main' workflow
project = load_project("./", "git://github.com/mlrun/project-demo.git",url=<name (in DB) or git or tar.gz or .zip sources archive path>)
````
2. [new_project](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=new_project#mlrun.projects.new_project) thats Create a new MLRun project, optionally load it from a yaml/zip/git template.
````
# create a project with local and marketplace functions, a workflow, and an artifact
project = mlrun.new_project("myproj", "./", init_git=True, description="my new project",url=<name (in DB) or git or tar.gz or .zip sources archive path>)
````
***Important Note-*** If you want to run your code locally you must clone the files to the context directory, execute automaticlly when you load project or create new project and define a url params

#### Get Function Object 
For gets function object you will need to use the [get_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=get_function#mlrun.projects.MlrunProject.get_function) method.
This method allows you to get a function object based on the metadata in your project YAML file.
````
serving_func = project.get_function('<function name>')
````
#### Run Function 
For run a function you will need to use the [run_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=run_function#mlrun.projects.MlrunProject.run_function) method.
This method allows you to run a MLRun **jobs** locally and remotely as long as there is no requirments ( if there is any requirments you will need to build a new image before you run a function)
It is equivalent to func.run method.
````
project.run_function(function='<function name>',params={'num':3},local=False)
````
````
project.run_function(function='<function name>',params={'num':3},local=True)
````
#### Build Function
For building a new images for MLRun jobs you will need to use the [build_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=build_function#mlrun.projects.MlrunProject.build_function) method
This method allows you to build a new image based on your job requirements or custom attributes - this method it only for non remote function for example MLRun jobs.
It is equivalent to func.deploy() method.
````
project.build_function('<function name>')
````

#### Deploy Function
For deplying remote function as nuclio or serving you will need to use the [deploy_function](https://docs.mlrun.org/en/latest/api/mlrun.projects.html?highlight=deploy_function#mlrun.projects.MlrunProject.deploy_function) method.
You must use this method beofre invoke nuclio or serving fucntions.
It is equivalent to func.deploy() method.
````
nuclio_func=project.deploy_function(function='<function name>')

nuclio_func.function.invoke('/',{'int':4})
````

For more Examples you can see [Load_project](https://github.com/GiladShapira94/load-project-example/blob/master/load_project.ipynb) and [load_project_clone](https://github.com/GiladShapira94/load-project-example/blob/master/load_project_clone.ipynb)
