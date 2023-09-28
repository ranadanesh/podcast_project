# PodcastProject
   
### Installation

<br />

> 👉 The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ranadanesh/podcast_project.git

```


<br />

> 👉 Create a virtual environment to install dependencies in:

```sh
$ python3 -m venv env
```
 Activate the  virtual environment
 
<br />

> 👉 For Mac/Linux:

```sh
$ source env/bin/activate
```

<br />

> 👉 For Windows:

```sh
env\Scripts\activate
```

<br />

> 👉 Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Note the `(env)` in front of the prompt. This indicates that this terminal.

<br />

> 👉 Make migrations: 

```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
<br />

> 👉 Create an account for admin:

```sh
python manage.py createsuperuser
```
### Running The Project
Once `pip` has finished downloading the dependencies:


<br />

> 👉 Run the project

```sh
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000`.

To access the admin panel, go to http://localhost:8000/admin and log in using admin account you created earlier.
