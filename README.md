# MovieWeb App

MovieWeb App is a web application for managing movies and their reviews. Built using Flask, this app allows users to view movie details, add, edit, and delete reviews, and manage a list of movies.

## Features

- **View Movies**: Browse a list of movies with details including name, director, and IMDb rating.
- **Manage Reviews**: Add, edit, and delete reviews for each movie.
- **User Management**: Each user can manage their own movie list and reviews.

## Installation

### Prerequisites

- Python 3.x
- Flask

### Setting Up the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/Welat-E/movieweb_app.git
   cd movieweb_app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Usage

- **Home Page**: Navigate to the home page to view a list of movies.
- **Movie Details**: Click on a movie to see its details and reviews.
- **Manage Reviews**: Add, edit, or delete reviews for movies you have permission to modify.
- **User Management**: View and manage the list of movies associated with your user account.

## File Structure

- `app.py`: Main Flask application file.
- `templates/`: Directory containing HTML templates.
- `static/`: Directory for static files (CSS, JS, images).
- `requirements.txt`: List of Python dependencies.
- `README.md`: Project documentation.

## Customization

To customize the styling and add new features:

1. **CSS**: Modify styles in the `style.css` file to adjust the appearance as needed.
2. **Flask Routes**: Update routes and logic in `app.py` to handle new features or change existing functionality.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

