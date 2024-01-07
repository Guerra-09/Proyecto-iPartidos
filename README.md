# Documentation

Project for university. This website it's a sport fields booker where there are two main actors, the Tenant, who has a club and manage their fields and the Client, who reserves the fields. 

## Technologies used

- Django: Framework used for Backend and FrontEnd activities. Powered by python.
- SQLite: Databse used as ORM by default in django.
- Bootstrap: For some components templates.
- google-auth: Library used for sending emails with reservations and recovering passwords.


## Instalation


- Cloning repository to local pc
```
$ git clone https://github.com/Guerra-09/Proyecto-iPartidos.git
```

- Moving to folder clonned
```
$ cd proyecto-ipartidos
```

- Setting up environment. If pipenv it's not installed try using $python install pipenv
```
$ pipenv --python 3.11  # Python version can be lower e.g 3.10
```

- This line will initialize the environment and you'll  have '(Proyecto-iPartidos)' at begging, this means you entered correctly
```
$ pipenv shell
```

- Installing dependencies inside environment, so you dont need to have it locally.
```
(Proyecto-iPartidos)$ pipenv install django pillow pylint python-dotenv django-widget-tweaks
```
- Finally run server using this line
```
(Proyecto-iPartidos)$ python manage.py runserver
```



## Screenshots

<div class="image-grid">
  <div class="column">
    <img src="https://github.com/Guerra-09/Proyecto-iPartidos/assets/91816666/5381a9a9-9ccf-4b27-90ba-912a22de2982" alt="Screenshot 1" width="450">
    <img src="https://github.com/Guerra-09/Proyecto-iPartidos/assets/91816666/5947b9de-81d9-46de-a648-4ac1daab5b73" alt="Screenshot 2" width="450">
  </div>

  <div class="column">
    <img src="https://github.com/Guerra-09/Proyecto-iPartidos/assets/91816666/a2cc735e-23ea-4b48-8eaa-22b4c36b10c5" alt="Screenshot 3" width="450">
    <img src="https://github.com/Guerra-09/Proyecto-iPartidos/assets/91816666/a570a33a-ee70-4f28-a504-e6e772bc48b7" alt="Screenshot 4" width="450">
  </div>
    
  <div class="column">
    <img src="https://github.com/Guerra-09/Proyecto-iPartidos/assets/91816666/80a585e7-3e6d-49f1-8265-bddd0ae56240" alt="Screenshot 5" width="450">
    <img src="https://github.com/Guerra-09/Proyecto-iPartidos/assets/91816666/5f062cdb-d75a-4afa-b485-28437d5ddedb" alt="Screenshot 6" width="450">
  </div>
</div>

