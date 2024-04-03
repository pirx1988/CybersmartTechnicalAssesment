## Setup
In root directory of the project create `.env` file with content from `env.example`.
Remember to replace `OPEN_WEATHER_MAP_API_KEY` to your own key obtained from: https://openweathermap.org/api to your personal email after after you start your subscription.


Run docker container from the root directory via command:

```
docker-compose up
```
Run migration scripts required for tables creation based on task model:
```
docker-compose exec django-webapp python manage.py migrate
```

Create user with admion rights from command line (django-webapp container must be working) which will be required in logging in to the application :
```
docker-compose exec django-webapp python manage.py createsuperuser
```
You can create furhter users from admin panel http://localhost:8080/admin/auth/user/add/.
(in order to test it out if tasks are correctly assigned to specific users)

## Logic applied for background colors calculation:
### Temperature ranges for determination of cold, warm or hot weather
```
cold: below 10°C (50°F)
warm: 10°C (50°F) to 25°C (77°F)
hot: above 25°C (77°F)
```
### Condition for determination of background color in form: condition => Background color
```
cold or rain => Blue
warm or cloudy => Yellow-Orange
hot or sunny => Red
other => White
```

