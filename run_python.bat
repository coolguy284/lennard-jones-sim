rem sets current directory to batch file's directory
rem https://serverfault.com/questions/95686/change-current-directory-to-the-batch-file-directory/95696#95696
cd /D "%~dp0"

python generation/py_src/main.py
