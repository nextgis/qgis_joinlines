mkdir joinlines
mkdir joinlines\i18n
xcopy *.py joinlines
xcopy *.ui joinlines
xcopy README.md joinlines
xcopy LICENSE joinlines
xcopy metadata.txt joinlines
xcopy icon.png joinlines
xcopy i18n\joinlines_ru.ts joinlines\i18n\joinlines_ru.ts
lrelease joinlines\i18n\joinlines_ru.ts
del joinlines\i18n\joinlines_ru.ts
zip -r joinlines.zip joinlines
del /s /q joinlines
rmdir /s /q joinlines