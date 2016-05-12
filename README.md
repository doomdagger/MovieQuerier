# MovieQuerier
Movie Clips Query for input of actor image, scene image, and motion description

### How to build the assets?

Try to run the commands below.
```bash
# This is comment

# run build.py under source package
$ python ./source/build.py -m MOV_FILE_PATH
```

For now, we only support `mov` video file format. The built assets will be placed under `resources` folder.

### How to run the application?

Try to run the commands below.
```bash
# run app.py
$ python ./app.py
```

The server, by default, will listen at `http://localhost:5000`. Before running the application, please make sure you have at least one movie being built already.
