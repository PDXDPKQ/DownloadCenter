@echo off
python generate_filelist.py -q
git add .
git commit -m "1"
git push --force
pause