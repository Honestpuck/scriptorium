# scriptorium

A utility for managing the scripts in Jamf Pro. It uses two git repos to back them up and as a source of truth.

When it pulls a script from the server it attaches '&' and it's ID to the end of the name. It then stores the XML in one folder and extracts the script, storing it in a separate folder.

The capability set out below is currently a wish list rather than a totally implemented system.

## Commands

`scriptorium lists` lists all the scripts currently in the JPC.

`scriptorium verify` compares the local scripts with the JPC and reports differences.

`scriptorium down` downloads all scripts out of the server. It won't overwrite a script in local unless the --force option is specified. 

`scriptorium up` uploads all scripts to the server. By default it also does a git commit on the scripts folder. The pre-commit hook finds changed scripts in the scripts directory and copies them into the XML file and uploads the result to the JPC.  It then does a commit on the XML folder. You can specify `--push` to do an immediate push after the commit. `--message 'string'` sets the commit message to `string`. If you don't set the commit message it will be a list of the scripts found to process prepended by "Up: ".

The `up` option allows you to edit a script in the scripts directory and have it automatically backed up to the git repo and uploaded to the JPC. I am wavering over calling this 'commit' instead of up.

### Changing a file name

If you want to change a file name, perhaps to increment a version number, then it has to be done with the `scriptorium change` command. This takes the old name and new name as arguments. This command does a `git mv` on both the script and the XML file. It does _not_ do a commit and it does _not_ change the file name on the JPC. To do both those things you can follow the change with a `scriptorium up`.

### Adding A Script

Adding a script is done with `scriptorium add`. This expects a number of things to be defined on the command line. If they aren't defined on the command line the program will ask for them.

- -f filename
- -c category
- -n notes
- -a priority=after
- -b priority=before
- -z zero parameters for script

If `--zero` is specified then the program will not ask for any script parameters. When it _does_ ask the first blank parameter specified will stop it asking. Jamf supports from 4 to 11 parameters so we do too.

It will then write out an XML file containing the info and an empty script.
