mkdir joinlines
xcopy *.py joinlines
xcopy README.md joinlines
xcopy LICENSE joinlines
xcopy metadata.txt joinlines
xcopy icon.png joinlines
zip -r joinlines.zip joinlines
del /Q joinlines
rd joinlines