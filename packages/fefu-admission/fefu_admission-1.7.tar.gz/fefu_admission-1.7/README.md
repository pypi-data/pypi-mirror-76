Fefu
====

A command-line application for monitoring the competitive situation of admission to a university

## Installing
 1. Install [python 3](https://www.python.org/)
 2. Open ```cmd.exe``` in Windows or ```terminal``` in Linux/MacOS and write: ```pip install fefu_admission --user```
 3. (optional) Create a file ```~/.fefu_admission/settings.json```. If you don't create a file, the 
 file will be created automatically. Sample content:
    ```json
    {
        "me": {
          "name": "Second name First Name",
          "points": [100, 100, 100, 10],
          "agreement": "true"
        },
        "list_of_departments": [
            "01.03.02 Прикладная математика и информатика",
            "02.03.01 Математика и компьютерные науки",
            "09.03.03 Прикладная информатика",
            "09.03.04 Программная инженерия"
        ]
    }
    ```

## Usage

```
Usage: fefu_admission [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  list   Show list of any department
  load   Load data from website and save to ~/.fefu_admission/data/
  stats  Get statistics of the competitive situation

```

## Classes

![](classes_fefu_admission.png)
(scheme created with the following command: ```pyreverse -o png -p fefu_admission fefu_admission/```)
## License

Copyright (c) Andrey Varfolomeev. Licensed under the MIT license