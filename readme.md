# Django Project Setup

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.10
- pip (Python package installer)
- virtualenv (optional but recommended)

## 1. Create a Virtual Environment

Start by creating a virtual environment using Python 3.10:

```bash
python3.10 -m venv myenv
```

## 2. Activate the Virtual Environment

Activate the virtual environment with the following command:

- On **Windows**:

```bash
myenv\Scripts\activate
```

- On **macOS/Linux**:

```bash
source myenv/bin/activate
```

## 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 4. Set Up the Django Project

Navigate to the project directory and apply the necessary migrations:

```bash
cd myproject
python manage.py migrate
```


## 5. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The server will start on `http://127.0.0.1:8000/`.

## 6. Access the Admin Interface

You can access the Django admin interface at `http://127.0.0.1:8000/admin/` using the superuser credentials you created.

## 7. Additional Commands

- **To create new Django apps**:

```bash
python manage.py startapp appname
```

- **To check for project issues**:

```bash
python manage.py check
```

- **To collect static files**:

```bash
python manage.py collectstatic
```

## 8. Deactivate the Virtual Environment

Once you're done working on the project, you can deactivate the virtual environment by running:

```bash
deactivate
```

---

That's it! Your Django project is now set up and ready for development.
```