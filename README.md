# scriptorium
A utility for managing the scripts in Jamf Pro. It uses a git repo to back them up and as a source of truth.

When it pulls a script from the server it attaches '&' and it's ID to the end of the name. It then stores the XML in one folder and extracts the script, storing it in a separate folder.

`scriptorium -o` pull all scripts out of the server. It won't overwrite a script in storage.

`scriptorium -i` does a git commit on the scripts folder. The pre-commit hook goes through the changed files and copies them into the XML and uploads the result to the JPC. 

The `-i` option allows you to edit a script in the scripts directory and have it automatically backed up to the git repo and uploaded to the 

