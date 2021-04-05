# scriptorium

A utility for managing the scripts in Jamf Pro.

The system composes two git repos in two local directories and in your git store that should echo the scripts in your Jamf Pro server. One git repo stores the entire record from the server in XML format and the other stores the actual script as text. The script has the same name in all three spots.

With the system installed you can make changes to the scripts in the text directory and use the tools in the system to keep the three in sync.

The basic structure is `scriptorium <command>` some with required parameters and command options. 

## Commands

- `add`       used to add a script to the system.
- `commit`    `git commit` in both directories.
- `down`      pulls all scripts from the server
- `git`       asks for a string and runs it as a git command in both directories
- `list`      lists all scripts on the JP server
- `push`      `git push` in both directories
- `remove`    remove a script in all three spots
- `rename`    rename a script in all scripts
- `up`        Uploads all changes and additions to the server

## Command Descriptions

### `add`

```
usage: scriptorium.py add [-h] [-f FILENAME] [-c CATEGORY] [-n NOTES] [-p | -d] [-m MESSAGE] [-a | -b | -r] [-z]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        name of new script
  -c CATEGORY, --category CATEGORY
                        category of script
  -n NOTES, --notes NOTES
                        note about script
  -p, --push            do a git push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
  -a, --after           run script with priority 'after'
  -b, --before          run script with priority 'before'
  -r, --reboot          run script at reboot
  -z, --zero            zero parameters for script
```

Add goes through the process of adding a script in all the required spots. You end up with an empty script in the scripts folder, an XML file with all the bits filled in and uploaded to the server.

If you don't specify something on the command line you will be prompted for it.

You will also be prompted for the 4th to 11th parameters if you don't specify zero. When you are prompted for parameters entering a blank will stop the process.

If you allow a commit and don't specify a commit message it will be the name of the new file.

### `commit`

```
usage: scriptorium.py commit [-h] [-p] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -p, --push            do a git push after commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

If you've specified a number of changes with `--dont-commit` then you are going to want to perform a commit eventually. This does a `git add *` before the commit. If you don't specify a message it will be a list of files altered.

### `down`

```
usage: scriptorium.py down [-h] [-n] [-p | -d] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-force        don't force overwrite of existing script or XML file
  -p, --push            do a git push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

### `git`

```
usage: scriptorium.py git [-h]

optional arguments:
  -h, --help  show this help message and exit
```

The `git` command will ask for a string and run it as a git command in both directories. The string is split using a routine that will split the string into command "words" honouring any quoted strings and leaving the quote in the "word". An example, the entry 'this that "and that"' will split into `['this', 'that', '"and that"']`

### `list`

```
usage: scriptorium.py list [-h]

optional arguments:
  -h, --help  show this help message and exit
```

It's simple, no arguments. Just lists the scripts on the server

### `push`

```
usage: scriptorium.py push [-h]

optional arguments:
  -h, --help  show this help message and exit
```

If you make a number of commits without a `--push` then you will need to do it eventually. This does it in both directories at once.

### `remove`

```
usage: scriptorium.py remove [-h] [-p | -d] [-m MESSAGE] name

positional arguments:
  name                  name of script to remove

optional arguments:
  -h, --help            show this help message and exit
  -p, --push            do a git push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

Removes a script from all three spots.

### `rename`

```
usage: scriptorium.py remove [-h] [-p | -d] [-m MESSAGE] name

positional arguments:
  name                  name of script to remove

optional arguments:
  -h, --help            show this help message and exit
  -p, --push            do a git push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

### `up`

```
usage: scriptorium.py up [-h] [-p | -d] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -p, --push            do a push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

Uploads all changes and adds to the server. Behind scenes it does a `git diff` in the scripts directory to get a list of changes then updates those scripts in the XMl files and uploads them.

## Install

First you will want to get the git bits working. Create the two repositories 