

# Simple Todo App with Django

Welcome to the **Simple Todo App** built with Django! This project is designed to help beginners get started with Django by building a simple, functional todo application.

## Features

- Add new tasks to your todo list
- View the list of tasks
- Mark tasks as completed
- Delete tasks

## Requirements

Before you start, make sure you have the following installed:

- Python (3.8 or above)
- Django (4.0 or above)
- SQLite (comes pre-configured with Django, no need to install separately)

## Setup Instructions

Follow these steps to get your Todo App up and running:

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/simple-todo-app.git
cd simple-todo-app
```

### Step 2: Create a Virtual Environment

We recommend creating a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```


### Step 3: Apply Migrations

Django uses migrations to apply database changes. Run the following command to set up your database:

```bash
python manage.py migrate
```

### Step 4: Create a Superuser 

To access the Django admin panel and manage your todos, you can create a superuser account.

```bash
python manage.py createsuperuser
```

Follow the prompts to create the superuser.

### Step 5: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Now, open your web browser and visit `http://127.0.0.1:8000/` to see your Todo app in action!

### Step 6: Access the Admin Panel (Optional)

If you created a superuser in Step 4, you can access the Django admin panel by navigating to `http://127.0.0.1:8000/admin/` and logging in with the superuser credentials.

## Project Structure

Here's a brief overview of the project structure:

```
todoprj/
│
├── manage.py            # Django's command-line utility
├── requirements.txt     # List of dependencies for the project
├── todoprj/     # Project folder containing settings and apps
│   ├── __init__.py
│   ├── settings.py      # Django project settings
│   ├── urls.py          # URL routing configuration
│   ├── wsgi.py
│   └── todoapp/         # The main app for the todo functionality
│       ├── __init__.py
│       ├── admin.py      # Admin configuration
│       ├── models.py     # Database models
│       ├── views.py      # Views for displaying and managing tasks
│       ├── urls.py       # URL routing for the app
│       └── templates/    # HTML templates for the app
└── db.sqlite3           # SQLite database file (automatically created)
```

## Basic Usage

- **Add a Todo**: Visit the homepage and enter a new task in the form to add it to your todo list.
- **Mark as Completed**: Click on a task to toggle its completion status.
- **Delete a Todo**: Delete any todo by clicking the delete button next to it.

## License

This project is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Enjoy building with Django! If you have any questions or run into any issues, feel free to open an issue on the GitHub repository.

