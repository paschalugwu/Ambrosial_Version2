# Ambrosial

## Overview

**Ambrosial** is a Flask-based web application designed to manage user accounts, posts, and messaging. The application is deployed and can be accessed at [https://ambrosial-webapp.vercel.app/](https://ambrosial-webapp.vercel.app/). It features user authentication, profile management, and a robust system for creating and managing posts. The application supports multiple languages and includes error handling, user authentication, and various utilities to enhance the user experience.

## Installation

To set up the Ambrosial project on your local machine, follow these steps:

### Prerequisites

- Python 3.8 or later
- Flask
- Flask-Babel
- Flask-Login
- Flask-Bcrypt
- Flask-SQLAlchemy
- Flask-Testing
- Flask-WTF
- Other dependencies listed in `requirements.txt`

### Step-by-Step Instructions

1. **Clone the Repository**

    ```bash
    git clone https://github.com/paschalugwu/ambrosial.git
    cd ambrosial
    ```

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**

    The application uses SQLite for database management. By default, databases are created in the `instance` directory.

    ```bash
    flask db upgrade
    ```

5. **Run the Application**

    ```bash
    python run.py
    ```

## Usage

Once the application is running, you can access it via the deployed web app:

**Production URL:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

Here are some common use cases:

- **Register a New Account:** Navigate to `http://127.0.0.1:5000/register` to create a new user account.
- **Log In:** Use the `http://127.0.0.1:5000/login` route to access your account.
- **Create a Post:** Visit `http://127.0.0.1:5000/create_post` to add a new post.
- **View Posts:** Go to `http://127.0.0.1:5000/post/<post_id>` to see individual posts.
- **Manage Account:** Access `http://127.0.0.1:5000/account` to update your profile information.

## Project Structure

Here is a detailed description of the project tree structure:

- **`AUTHORS.md`**: Contains information about the contributors to the project.
- **`README.md`**: This file, providing an overview and instructions for the project.
- **`flask_ambrosial/`**: Main application directory.
  - **`__init__.py`**: Initializes the Flask application and brings together various components.
  - **`apis/`**: Contains API routes and their tests.
    - **`api_routes.py`**: Defines API routes.
    - **`tests/`**: Unit tests for API routes.
  - **`babel.cfg`**: Configuration file for Flask-Babel, managing translations.
  - **`chats/`**: Handles chat functionality.
    - **`routes.py`**: Defines routes for chat features.
    - **`tests/`**: Tests for chat routes.
  - **`config.py`**: Configuration settings for different environments.
  - **`errors/`**: Manages error handling.
    - **`handlers.py`**: Defines custom error handlers.
    - **`tests/`**: Unit tests for error handlers.
  - **`main/`**: Core functionality of the application.
    - **`routes.py`**: Main application routes.
    - **`tests/`**: Tests for main routes.
  - **`messages.pot`**: Translation template file for messages.
  - **`models.py`**: Defines database models.
  - **`posts/`**: Manages posts, including forms and routes.
    - **`forms.py`**: Forms related to posts.
    - **`routes.py`**: Routes for managing posts.
    - **`tests/`**: Tests for post forms and routes.
  - **`static/`**: Static files like JavaScript, CSS, and images.
    - **`js/`**: JavaScript files for various functionalities.
    - **`main.css`**: Main stylesheet for the application.
    - **`post_pics/`**: Directory for post images.
    - **`profile_pics/`**: Directory for user profile pictures.
  - **`templates/`**: HTML templates for rendering pages.
    - **`errors/`**: Templates for error pages.
  - **`tests/`**: General application tests.
  - **`translations/`**: Translation files for different languages.
  - **`users/`**: Manages user accounts, including forms and routes.
    - **`forms.py`**: User-related forms.
    - **`routes.py`**: Routes for user functionality.
    - **`tests/`**: Tests for user forms, routes, and utilities.
    - **`utils.py`**: Utility functions for user management.
- **`instance/`**: Contains database files.
- **`package-lock.json`**: Lock file for npm dependencies (if applicable).
- **`package.json`**: Defines npm dependencies and scripts (if applicable).
- **`requirements.txt`**: Lists Python dependencies.
- **`run.py`**: Entry point for running the Flask application.
- **`project_structure.txt`**: Provides a textual description of the project structure.

## Configuration

Configuration settings are managed through the `config.py` file. You may need to set up environment variables for sensitive configurations. 

**Example Environment Variables:**

- `SECRET_KEY`: Secret key for Flask sessions.
- `SQLALCHEMY_DATABASE_URI`: Database connection string.
- `MAIL_USERNAME`: Email username for sending emails.
- `MAIL_PASSWORD`: Email password for sending emails.

Create a `.env` file in the root directory to manage these environment variables.

## Testing

To run the tests for the application, use the following command:

```bash
pytest
```

Tests are organized into different modules, including `test_forms.py`, `test_routes.py`, and `test_utils.py`, covering various aspects of the application.

## Contributing

Contributions to the Ambrosial project are welcome! To contribute:

1. **Fork the Repository**: Create your own fork of the repository.
2. **Create a Branch**: Make a new branch for your changes.
3. **Commit Changes**: Write clear commit messages.
4. **Submit a Pull Request**: Open a pull request with a description of your changes.

Please ensure that your code follows the project's coding standards and includes tests for any new functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- **Flask**: The core framework used for building the web application.
- **Flask-Babel**: Provides internationalization and localization.
- **Flask-Login**: Manages user sessions.
- **Flask-SQLAlchemy**: Provides SQLAlchemy integration for Flask.
- **Flask-WTF**: Provides form handling and validation.
- **Flask-Bcrypt**: Hashes passwords securely.

Special thanks to all contributors and open-source libraries that have supported this project.
