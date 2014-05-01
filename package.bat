mkdir joinlines
xcopy *.py joinlines
xcopy README.md joinlines
xcopy metadata.txt joinlines
zip -r joinlines.zip joinlines
del /Q joinlines
rd joinlines