## Testing Plan

"check everywhere" means both directories, both upstream repos and Jamf.

Starting from a blank slate
 - make test directory "testing scriptorium"
   - it has to have a space so we can check if that's a problem
 - Build the directories and repos
 - set folder names in scriptorium Y
 - scriptorium list Y
 - scriptorium down (doesn't commit) Y
 - scriptorium commit -m "first commit"
 - scriptorium push Y
 - scriptorium add --don't commit --zero Y
   - name = "lots of words.sh"
 - scriptorium commit --push -m "added lots of words.sh" Y
   - check everywhere for "lots of words.sh"
 - scriptorium add --push
   - check everywhere for name Y
 - scriptorium rename "lots of words.sh" "lots of little words.sh"
   - check for new name everywhere Y
 - scriptorium delete "lots of little words.sh"
 - scriptorium verify --quick
 - edit a script <name>
 - scriptorium verify --quick
 - scriptorium verify
 - scriptorium verify --diff
 - scriptorium verify --script <name>
 - scriptorium verify --script <name> --diff
 - scriptorium up
 - scriptorium commit -m "edit of <name>"
   - check correct script everywhere
