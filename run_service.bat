docker build . -t task:01
set url=%1
set result_dir=%2
docker run -it task:01 %url% %result_dir%
docker ps -aqf ancestor=task:01 > id
set /p id= < id
docker cp %id%:/%result_dir% .
del id
