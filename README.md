# scriptorium

A utility for managing the scripts in Jamf Pro. It provides backup, change tracking, and an easier edit process. 

The system comprises two git repos in two local directories that should echo the scripts in your Jamf Pro server. One git repo stores the entire record from the server in XML format and the other stores the actual script as text. The script has the same name in all three spots.

With the system installed you can make changes to the scripts in the text directory and use the tools in the system to keep the three in sync.

The basic structure is `scriptorium <command>` some with required parameters and command options.

There is a `#scriptorium` channel on the MacAdmins Slack. Hit me up there if you want some help setting up. Raise an issue here if you find a bug or want a particular improvement.

See [Docker](#docker) and [Poetry](#poetry) sections for container and virtual environment usage.

_Note: Bug reports and change suggestions gratefully accepted_

## Commands

- `add`       used to add a script to the system.
- `commit`    `git commit` in both directories.
- `delete`    remove a script in all three spots
- `down`      pulls all scripts from the server
- `git`       asks for a string and runs it as a git command in both directories
- `list`      lists all scripts on the JP server
- `push`      `git push` in both directories
- `rename`    rename a script in all three spots
- `up`        uploads all changes and additions to the server
- `verify`    verify text against XML against Jamf server

## Install

`scriptorium` requires the `requests` and `inquirer` libraries. They can be installed by running `pip3 install requests` and `pip3 install inquirer`.

Now pull down a copy of this repo so you can keep it up to date easily. `git clone git@github.com:Honestpuck/scriptorium.git` will do the trick.

At this point you need to create the repositories, `text` and `xml` in your git store. Create them as empty (and private if you are using a public repo store such as Github).

Now create a directory `scripts` on your computer, cd into it and perform a git clone to pull down both repositories. Git will tell you you just pulled blank repositories.

Set the variables at the top of scriptorium to point to the two directories and the location of the prefs file containing the JSS location, user and password. The script assumes it is in the same format as the jss_importer prefs in the AutoPkg prefs file. Here is the minimum required plist:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>API_PASSWORD</key>
	<string>password</string>
	<key>API_USERNAME</key>
	<string>account</string>
	<key>JSS_URL</key>
	<string>https://example.jamfcloud.com</string>
</dict>
</plist>
```

You can create it or add it to your existing AutoPkg preference file with:
```
defaults write com.github.autopkg.plist API_PASSWORD 'password'
defaults write com.github.autopkg.plist USERNAME 'account'
defaults write com.github.autopkg.plist JSS_URL 'https://example.jamfcloud.com'
```

You can find the spot to set the variables in scriptorium, it looks like:
```
# where we stash the XML files
xml_dir = "~/work/test/XML"
# where we stash the text files
txt_dir = "~/work/test/text"
# prefs file
prefs_file = "~/Library/Preferences/com.github.autopkg.stage.plist"
```

Link `scriptorium` into somewhere in your path like `/usr/local/bin`, personally I have a bin directory in my home directory just for tools like this.

Now run `scriptorium down` and all the scripts will be populated on your Mac. Now send them to the upstream repositories with `scriptorium commit --message "First commit" --push`. You are now at point where you can use the system.

The other important command is `add`. So that you can keep everything in sync when you want to add a new script to the system you use `scriptorium add` and the script will spring into existence in all three places. It will be as good as empty, it's contents are set to `# <name>` where `<name>` is the name you have given it.

The file `_scriptorium` is a bash command completion for scriptorium. See https://github.com/Honestpuck/apple_complete for instructions on how to install it for your shell.

## Work practices

The delete and rename commands do a commit by default at the moment. The problem in doing a commit is that the up command relies on changed files not being committed until after up.

The best way of solving this dilemma would be for all commits to be preceded by an up command within scriptorium. Since remove, rename and add already modify the server this problem is only triggered when you edit a script so this seems acceptable and has been implemented.

You have to run the system from the directory that holds the text files. If you do that in a shell that has a git add on you can have the prompt give you useful information. It also means you can use file name completion when you need to specify a file. I also have Visual Studio Code open to the same folder, adding the "GitLens" extension to VS Code gives you good feedback on when various changes were made to your script.

#### Adding a script

The process of adding a script starts with running `scriptorium add`. I usually put `-d` so that the system doesn't do a commit so I can edit the script before it goes into Jam Pro. After the add completes I can edit the stub in my editor and when ready for final testing run `scriptorium commit -m "First commit for script something.sh" --push`. That propagates the new script through the system.
#### Editing a script

Editing a script just means opening it in your editor of choice. Once you've made your changes and saved them in your editor the process is almost identical to adding a script. Run `scriptorium commit -m "Fixed widgets in script acme.sh" --push`
### Still to be done

On the roadmap is a command `modify` which will modify the aspects of the script record in Jamf that aren't the actual script such as notes and parameters.

Some notes on best practices and work methods should also appear at some point. Contributions to these would be greatly appreciated.

Modification of the script to produce another to handle extension attributes instead of scripts is in the planning stages.

### Suggestions 

Suggestions for changes or extensions are always appreciated.

## Command Descriptions

### `add`

```
usage: scriptorium add [-h] [-f FILENAME] [-c CATEGORY] [-n NOTES] [-p | -d] [-m MESSAGE] 
                       [-a | -b | -r] [-z]

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

Add goes through the process of adding a script in all the required spots. You end up with an almost empty script in the scripts folder, an XML file with all the bits filled in and uploaded to the server.

If you don't specify something on the command line you will be prompted for it.

You will also be prompted for the 4th to 11th parameters if you don't specify zero. When you _are_ prompted for parameters entering a blank will stop the process.

By default it will do a commit but not a push.

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

If you've made a number of changes with `--dont-commit` then you are going to want to perform a commit eventually. This does an `up` and `git add *` before the actual commit.

### `delete`

```
usage: scriptorium delete [-h] [-p | -d] [-m MESSAGE] name

positional arguments:
  name                  name of script to remove

optional arguments:
  -h, --help            show this help message and exit
  -p, --push            do a git push after commit
  -d, --dont-commit     don't do a commit
  -m MESSAGE, --message MESSAGE
                        set commit message
```

Deletes a script from both directories and Jamf

### `down`

```
usage: scriptorium down [-h] [-n] [-p | -d] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-force        don't force overwrite of existing script or XML file
  -s SCRIPT, --script SCRIPT download just one script
```

This downloads all the scripts from the JPC server copying over the current contents.

### `git`

```
usage: scriptorium git [-h] [-c COMMAND]

optional arguments:
  -h, --help  show this help message and exit
  -c, --command quoted string containing git command
```

The `git` command will ask for a string and run it as a git command in both directories. The string is split using `shlex`, a library that splits the string into command "words" honouring any quoted strings and leaving the quotes in the "word". An example, the string 'this that "and that"' will split into `['this', 'that', '"and that"']`. You don't need to include the `git` at the front, scriptorium will add it for you.

### `list`

```
usage: scriptorium list [-h]

optional arguments:
  -h, --help  show this help message and exit
```

It's simple, no arguments. Just lists the scripts on the server.

### `push`

```
usage: scriptorium push [-h]

optional arguments:
  -h, --help  show this help message and exit
```

If you make a number of commits without a `--push` then you will need to do it eventually. This does it in both directories at once.

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

Uploads all changes and additions to the server. Behind scenes it does a `git diff` in the scripts directory to get a list of changes then updates those scripts in the XMl files and uploads them. This means it must be done before any commits, which is why `scriptorium commit` does an up before the requested commit.

### `verify`

```
optional arguments:
  -h, --help            show this help message and exit
  -d, --diff            print diff when checking every script
  -q, --quick           Just check lists not actual text
  -s SCRIPT, --script SCRIPT
                        specify a single script to check
```
Verify does a compare of the two directories and the server. The quick option just lists the files in each location and compares the lists. If they are different it prints a diff. If you don't specify `--quick` then the actual text is compared. The normal form just prints a short message if they differ. With `--diff` a diff is printed, this can quickly become quite large. You can specify a single script to verify with `-s`.

## Poetry

[Poetry](https://python-poetry.org/docs/) covers three common Python hurdles: dependencies, virtual environments (`venv`), and packaging.

For `scriptorium`'s use case, it generates the `venv` and `requirements.txt`, respectively.

### Usage
```bash
# Install
curl -sSL https://install.python-poetry.org | $(which python3) -

# Change config
poetry config virtualenvs.in-project true           # .venv in `pwd`

# Activate virtual environment (venv)
poetry shell

# Deactivate venv
exit  # ctrl-d

# Install multiple libraries
poetry add requests inquirer

# Initialize existing project
poetry init

# Run script and exit environment
poetry run scriptorium

# Install from requirements.txt
poetry add `cat requirements.txt`

# Update dependencies
poetry update

# Remove library
poetry remove icecream

# Generate requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Alternative to Poetry
It's possible to create a `venv` and `requirements.txt` file with built-in Python and pip.

```bash
# create a virtual environment via python
python3 -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies
python3 -m pip install requests inquirer

# generate requirements.txt
python3 -m pip freeze > requirements.txt

# exit virtual environment
deactivate
```

## Docker

As mentioned in the [MacAdmins Slack](https://macadmins.slack.com/archives/C02JJ35PZ51/p1644515156418309?thread_ts=1644273031.107999&cid=C02JJ35PZ51), this section adds experimental Docker support to the `scriptorium` script.

Please feel free to reach out via DM [@pythoninthegrass](https://macadmins.slack.com/archives/D1TE80HA7).

### Setup
* The `Dockerfile` heavily borrows from a [Medium](https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8) article
    * It creates two images:
        * `builder-image`: scaffolds the environment and its dependencies
        * `runner-image`:
            * installs minimal dependencies
            * creates user, sets permissions, copies virtualenv from builder
            * creates a virtualenv and sets `$PATH` for Python
            * calls `ENTRYPOINT` and/or `CMD`
    * By discarding the first `builder-image` it reduces file size of the final image
* To initiate the build process via `docker-compose`:
    ```bash
    # clean build (remove `--no-cache` to improve rebuilds with minor edits)
    docker-compose build --no-cache --parallel
    ```
    * Other functionality
        * Mounts the current working directory as a volume in the `WORKDIR`
            * This allows for testing on the host machine while running the container
        * Setup an interactive environment via `stdin_open` and `tty` directives set to `true`
            * Equivalent to `docker run -it`
            * If both are set to `false`, `docker-compose` will look for `ENTRYPOINT` and/or `CMD` in the `Dockerfile`

### Usage
* For general testing within a shell, leave the entrypoint commented out to simply call `CMD [ "bash" ]`
* After the main script is refactored, uncommenting out the entrypoint and `CMD ["-h"]` will run `scriptorium` with the `-h` or _help_ argument passed
* Docker commands
    ```bash
    # start container
    docker-compose up --remove-orphans -d

    # exec into container
    docker attach scriptorium

    # run command inside container
    python scriptorium.py

    # destroy container
    docker-compose down
    ```

## Further Reading
[Basic usage | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/basic-usage/)

[venv — Creation of virtual environments — Python 3.7.2 documentation](https://docs.python.org/3/library/venv.html)

[pip freeze - pip documentation v22.0.3](https://pip.pypa.io/en/stable/cli/pip_freeze/)

[Orientation and setup | Docker Documentation](https://docs.docker.com/get-started/)

[Creating the Perfect Python Dockerfile | by Luis Sena | Medium](https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8)

[Dockerfile: ENTRYPOINT vs CMD - CenturyLink Cloud Developer Center](https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/)

[Interactive shell using Docker Compose - Stack Overflow](https://stackoverflow.com/a/39150040)
