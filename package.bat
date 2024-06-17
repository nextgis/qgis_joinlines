mkdir joinlines
mkdir joinlines\i18n
xcopy src\joinlines\*.py joinlines
xcopy src\joinlines\*.ui joinlines
xcopy README.md joinlines
xcopy LICENSE joinlines
xcopy src\joinlines\metadata.txt joinlines
xcopy src\joinlines\icon.png joinlines
xcopy src\joinlines\i18n\joinlines_ru.ts joinlines\i18n\joinlines_ru.ts
lrelease joinlines\i18n\joinlines_ru.ts
del joinlines\i18n\joinlines_ru.ts
zip -r joinlines.zip joinlines
del /s /q joinlines
rmdir /s /q joinlines
