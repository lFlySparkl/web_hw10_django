создаем контейнер
docker run -d -p 27017:27017 --name my_mongodb mongo
docker run --name my_postgres_container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=1111 -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres

запускаем контейнер
docker start my_postgres_container
docker start my_mongodb

django admin

admin
admin

запускаем django
python manage.py runserver

с помощью "load_data.py" загружаем данные в монгу
с помощью "migration.py" переносим с монги в postgres