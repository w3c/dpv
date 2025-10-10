# DPVCG minutes generator

Structure:

- All raw minutes / meeting notes are kept in `/code/minutes-generator/data`
- All generated output minutes are kept in `/meetings`

To generate latest minutes:

1. copy `./template.irc` as `./data/meeting-YYYY-MM-DD.irc` with the date in the filename
2. edit the meeting minutes file according to irc / w3c bot format -- see https://harshp.com/dev/webdev/w3c-irc for relevant links and a cheatsheet
3. execute `./generate_latest_minutes.sh` (requires perl) to generate the latest minutes based on filename OR execute `./generate_specific_minutes.sh MM-DD` to generate based on parameters; This will produce the HTML for the minutes
4. run `uv run generate_index.py` or `python3 generate_index.py` to update the `index.html` with link to latest minutes

To publish:

1. All raw minutes and the code for minutes generator is kept on `dev`, therefore minutes should be first generated here (as above)
2. (ensure you are in root) `git switch dev` and then run `git add . && git commit -m "minutes for DD MMM YYYY" && git push`
3. Then to publish this for everyone, `git switch master`, and then `git reset -- code && git rm -r` to discard the code and raw files. Then `git commit --amend --no-edit && git push` to publish.