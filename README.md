<!-- GETTING STARTED -->
## About The Project
This is a simple Task Management API project that allows users to create, update, delete, and view tasks. Each task has a title, description, due date, and status. User are able to view all task as well as filter task by their status.
## Getting Started

This is an example of how you can set up this project locally.
Please follow these simple example steps to set up this project locally.

### Prerequisites

Install Python
* Python
    ```sh
    sudo apt-get update
    sudo apt-get install python3.8
    ```
* Install PostgresSQL or use cloud database <br />
For installing PostgresSQL and create database
    ```sh
    sudo apt install postgresql postgresql-contrib
    sudo -u postgres
    psql
    CREATE USER sample_user WITH PASSWORD 'sample_password';
    CREATE DATABASE sample_database WITH OWNER sample_user;
    ```

### Installation
1. Setup virtual environment
    ```sh
    pip install virtualenv
    python3 -m venv <virtual-environment-name>
    source <virtual-environment-name>/bin/activate
    ```
2. Install requirement packages
    ```sh
    python install -r requirement.txt
    ```
3. Create .env that contains database credentials in te same folder as manage.py. Example of .env file:
    ```sh
    DB_NAME='task_management'
    DB_USER='hgpnguyen'
    DB_PASS='******'
    DB_HOST='localhost'
    DB_PORT=5432
    ```
4. Migrate database
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Start server
    ```sh
    python manage.py runserver
    ```
## Usage
Endpoint that allows user to create task or view and filter list of tasks.
```sh
/tasks/?[status_filter]&[page]&[page_size]
```
1. `[status_filter]`(Optional): filter tasks base on status which are 'Pending' or 'Completed'. Accepting status value that is a variation of 'p', 'c', 'pending' or 'completed'. If empty or invalid value then return all tasks.
2. `[page]`(Optional): page number of pagination. Default value is 1.
2. `[page_size]`(Optional): page size of pagination. Default value is 10.

### Request Method
| Method   | Description                              |
| -------- | ---------------------------------------- |
| `GET`    | Used to retrieve list of filtered tasks. |
| `POST`   | Used to create new task. |

### Examples
| Method   | URL                                   | Description                              |
| -------- | --------------------------------------| ---------------------------------------- |
| `GET`    | `/tasks/`                             | Retrieve page 1 of all tasks with size of 10.                      |
| `POST`   | `/tasks/`                             | Create a new task.                       |
| `GET`    | `/tasks/?status=c`                          | Retrieve page 1 of all 'completed' tasks with size of 10.                       |
| `GET`    | `/tasks/?status=pending&page_size=5`                          | Retrieve page 1 of all 'pending' tasks with size of 5.                 |


Endpoint for view, update, delete a specific task.
```sh
/tasks/{task_id}/
```
- `{task_id}`: id of task.

### Request Method
| Method   | Description                              |
| -------- | ---------------------------------------- |
| `GET`    | Used to retrieve a single tasks. |
| `PUT`   | Used to update task. |
| `DELETE`| Used to delete task.|

### Examples
| Method   | URL                                   | Description                               |
| -------- | --------------------------------------| ------------------------------------------|
| `GET`    | `/tasks/1/`                           | Retrieve task #1.                         |
| `PUT`    | `/tasks/2/`                           | Updated data in task #2.                  |
| `DELETE` | `/tasks/3/`                           | Deleted task #3.                          |

## Explanation & Justification
- Model `Task`:
    - `title = models.CharField(max_length=100, blank=False)`: Limit the length of title to 100 and make this field a required because every tasks need title.
    - `description = models.TextField(blank=True)`: Allow empty description because not every tasks need description
    - `due_date = models.DateField(blank=False)`: This field is required to show when the task need to be finished.
    - `status = models.CharField(max_length=1, choices=[('P', 'Pending'), ('C', 'Completed')], blank=False)`: This field store the two status of task, 'Pending' and 'Completed', in value of 'P' and 'C', respectively. This is to save space for database.
- The use of `TaskViewSerializer`: Make the java response shows 'Pending' and 'Completed' for status instead of 'P' and 'C'. This make the response more readable.
- The use of the field `status = serializers.CharField(max_length=10)` and function `validate_status(self, status)` in serializer `TaskSerializer`: Allow endpoint to accept value 'p', 'c', 'pending', 'completed' and it's variation for status field and convert it to 'P' and 'C'. Make the API more flexible and easy to use.
- Endpoint `/tasks/?[status_filter]&[page]&[page_size]`: Allow user to filter tasks by their status or get all tasks and return paginated results.
## Room for improvement
1. Add partial update for API
2. Make the pagination result consistent
3. Add test cases for API