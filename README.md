# BlogPresset

- Demo link: [https://blogpresset.vercel.app/](https://blogpresset.vercel.app/)

- Visualisation
![Image 1](/demo/01.png)
![Image 2](/demo/02.png)
![Image 3](/demo/03.png)
![Image 4](/demo/04.png)
![Image 5](/demo/05.png)


- Video Demo: [Link to video demo](/demo/demo.mov)

# Frontend --- BlogPresset folder

BlogPresset is a web application that allows users to create and share blog posts. It provides functionalities for creating, updating, and deleting posts, as well as adding, updating, and deleting comments on posts.

## Features

- User authentication
- Create, update, and delete blog posts
- Add, update, and delete comments on posts
- View all comments on a specific post

## Technologies Used

- Python
- Flask
- MySQL
- Vue.js
- CSS

## Setup

1. Clone the repository.
2. Install the required dependencies using `npm install or yarn install`.
3. Set up a vue js configuration in `BlogPresset`.
4. Run the app  using `npm run dev`.

# Backend --- Backend folder

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
- `/add_post` - POST - Create a new post
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
