# BlogPresset backend API

This API is built using Flask and MySQL for a simple blogging platform called BlogPresset. It includes functionalities for user management, posting, commenting, and email verification.

## Features

- User Management:
  - Register new users
  - Login with JWT authentication
  - Update user profile
  - Deactivate user account

- Posts:
  - Create new posts
  - Upload images with posts
  - View all posts
  - Update and delete posts

- Comments:
  - Add comments to posts
  - Update and delete comments
  - View comments for a specific post

- Email Verification:
  - Send verification code via email
  - Verify email with the code

## Installation

1. Clone the repository
2. Install the required dependencies using `pip install -r requirements.txt`
3. Set up a MySQL database named `BlogPresset`
4. Update the database configuration in `api.py`
5. Run the Flask application using `python api.py`

## API Endpoints

- `/register` - POST - Register a new user
- `/login` - POST - Login with JWT authentication
- `/update_profile` - PUT - Update user profile
- `/delete_user_account` - DELETE - Deactivate user account
- `/create_post` - POST - Create a new post
- `/update_post/<post_id>` - PUT - Update a post
- `/delete_post/<post_id>` - DELETE - Delete a post
- `/add_comments/<email>/<post_id>` - POST - Add comments to a post
- `/update_comments/<email>/<comments_id>` - PUT - Update comments
- `/delete_comments/<comments_id>` - DELETE - Delete comments
- `/get_comments/<post_id>` - GET - Get comments for a post
- `/send_email` - POST - Send verification email
- `/verify_email/<email>/<code>` - GET - Verify email with code

## Author

- Charbel MAMLANKOU, a student in the 4th year of engineering cycle at the National School of Mathematical and Modeling Engineering.

Feel free to contribute to this project by submitting a pull request!
