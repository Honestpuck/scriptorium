# scriptorium
A utility for managing the scripts in Jamf Pro. It uses a git repo to back them up and as a source of truth.

When it pulls a script from the server it attaches '&' and it's ID to the end of the name. It then stores the XML in one folder and extracts the script, storing it in a separate folder.

`scriptorium` with no args lists all the scripts currently in the system.

`scriptorium out` pulls all scripts out of the server. It won't overwrite a script in storage unless the --force option is specified.

`scriptorium in` does a git commit on the scripts folder. The pre-commit hook finds changed scripts in the scripts directory and copies them into the XML file and uploads the result to the JPC before doing a commit on the XML folder. 

The `in` option allows you to edit a script in the scripts directory and have it automatically backed up to the git repo and uploaded to the JPC.

### Changing a file name

If you want to change a file name, perhaps to increment a version number, then it has to be done with the `scriptorium change` command. This takes the old name and new name as arguments. This command does a `git mv` on both the script and the XML file. It does _not_ do a commit.

### Adding A Script

Adding a script is done with `scriptorium add`. This expects a number of things to be defined on the command line. If they aren't defined on the command line the program will ask for them.

-F filename
-C category
-N Notes
-PR priority
-P0 No script parameters
-P4 parameter 4
-P11 parameter 11

If any script parameters are defined on the command line, including P0, then the program will not ask for any. When it _does_ ask then the first blank parameter specified will stop it asking. Jamf supports up to number 11 so we do too.

It will then write out an XML file containing the info and an empty script.
