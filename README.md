# scriptorium

A utility for managing the scripts in Jamf Pro. It provides backup, change tracking, and an easier edit process. 

The system comprises two git repos in two local directories that should echo the scripts in your Jamf Pro server. One git repo stores the entire record from the server in XML format and the other stores the actual script as text. The script has the same name in all three spots.

With the system installed you can make changes to the scripts in the text directory and use the tools in the system to keep the three in sync.

The basic structure is `scriptorium <command>` some with required parameters and command options. 

_Note for testers: At the moment this is fairly well tested. I'm not quite using this script in production, YMMV._

## Commands

- `add`       used to add a script to the system.
- `commit`    `git commit` in both directories.
- `down`      pulls all scripts from the server
- `git`       asks for a string and runs it as a git command in both directories
- `list`      lists all scripts on the JP server
- `push`      `git push` in both directories
- `remove`    remove a script in all three spots
- `rename`    rename a script in all three spots
- `up`        uploads all changes and additions to the server
- `verify`    verify text against XML against Jamf server

## Command Descriptions

### `add`

```
usage: scriptorium add [-h] [-f FILENAME] [-c CATEGORY] [-n NOTES] [-p | -d] [-m MESSAGE] [-a | -b | -r] [-z]

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
usage: scriptorium commit [-h] [-p] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -p, --push            do a git push after commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

If you've made a number of changes with `--dont-commit` then you are going to want to perform a commit eventually. This does a `git add *` before the commit. If you don't specify a message it will be a list of files altered.

### `down`

```
usage: scriptorium down [-h] [-n] [-p | -d] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-force        don't force overwrite of existing script or XML file
  -p, --push            do a git push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

This downloads all the scripts from the JPC server copying over the current contents 

### `git`

```
usage: scriptorium git [-h] [-c COMMAND]

optional arguments:
  -h, --help  show this help message and exit
  -c, --command quoted string containing git command
```

The `git` command will ask for a string and run it as a git command in both directories. The string is split using `shlex`, a library that splits the string into command "words" honouring any quoted strings and leaving the quotes in the "word". An example, the string 'this that "and that"' will split into `['this', 'that', '"and that"']`

### `list`

```
usage: scriptorium list [-h]

optional arguments:
  -h, --help  show this help message and exit
```

It's simple, no arguments. Just lists the scripts on the server

### `push`

```
usage: scriptorium push [-h]

optional arguments:
  -h, --help  show this help message and exit
```

If you make a number of commits without a `--push` then you will need to do it eventually. This does it in both directories at once.

### `remove`

```
usage: scriptorium remove [-h] [-p | -d] [-m MESSAGE] name

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
usage: scriptorium rename [-h] [-p | -d] [-m MESSAGE] src dst

positional arguments:
  src                   current name of script
  dst                   new name of script

optional arguments:
  -h, --help            show this help message and exit
  -p, --push            do a git push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

### `up`

```
usage: scriptorium up [-h]

optional arguments:
  -h, --help  show this help message and exit
```

Uploads all changes and adds to the server. Behind scenes it does a `git diff` in the scripts directory to get a list of changes then updates those scripts in the XMl files and uploads them.

### `verify`

Verify does a compare of the two directories and the server. The quick option just lists the files in each location and compares the lists. If they are different it prints a diff. If you don't specify `--quick` then the actual text is compared. The normal form just prints a short message if they differ. With `--diff` a diff is printed, this can quickly become quite large.

## Install

`scriptorium` requires the `requests` and `inquirer` libraries. Make sure they are installed.

Then you will want to get the git bits working. Create the two empty repositories in your git store (such as Github, though if you use Github make them private).

Now clone the two repos down to your Mac.

Set the variables at the top of scriptorium to point to the two directories and the location of the prefs file containing the JSS location, user and password. The script assumes it is in the same format as the AutoPkg prefs.

Put `scriptorium` somewhere in your path, like `/usr/local/bin`

Now run `scriptorium down` and all the scripts will be populated on your Mac. When you make changes to the scripts in the text directory you can upload them to your JSS with `scriptorium up`.

The other important command is `add`. So that you can keep everything in sync when you want to add a new script to the system you use `scriptorium add` and the script will spring into existence in all three places.

The file `_scriptorium` is a bash command completion for scriptorium. See https://github.com/Honestpuck/apple_complete for instructions on how to install it for your shell.

### Work practices

The remove, rename and up commands do a commit by default at the moment. The problem in doing a commit is that the up command relies on changed files not being committed until after up.

The best way of solving this dilemma would be for all commits to be preceded by an up command within scriptorium. Since remove, rename and add already modify the server this problem is only triggered when you edit a script so this seems acceptable and has been implemented.

### Still to be done

On the roadmap is a command `modify` which will modify the aspects of the script record in Jamf that aren't the actual script such as notes and parameters. I'm also going to add a `--command COMMAND` option to `git` so you can do it all from the command line without prompts.

Some notes on best practices and work methods should also appear at some point. Contributions to these would be greatly appreciated.

### Suggestions 

Suggestions for changes or extensions are always appreciated.
