@rem sets current directory to batch file's directory
@rem https://serverfault.com/questions/95686/change-current-directory-to-the-batch-file-directory/95696#95696
@cd /D "%~dp0"

@date /t
@time /t
@date /t > output-date1.txt
@time /t >> output-date1.txt
@cmd /c run_python.bat
@date /t
@time /t
@date /t > output-date2.txt
@time /t >> output-date2.txt
@timeout 150
@shutdown /h
