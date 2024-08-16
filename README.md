NB: "" use 'admin' for the username and also 'admin' for the password to obtain token 

JWT Authentication
To get authnenticated user token Run:
mutation {
  tokenAuth(username: "admin", password: "admin") {
    token
    refreshToken
  }
}

Add the token to your GraphQL requests as a Bearer token:
{
  "Authorization": "Bearer <your_token_here>"
} 

 ""



BLOG API WITH GRAPHQL

This Django-based blog API supports creating, updating, deleting, and querying posts, authors, and comments. JWT authentication secures the GraphQL endpoint.

Project Setup

Prerequisites
Python 3.12+
Django 5.1+
Virtual environment

Installation
Clone the Repository:
git clone https://github.com/Okpara007/blog_api.git
cd blog_api

Create and Activate a Virtual Environment:
python3 -m venv venv
source venv/bin/activate

Install Dependencies:
pip install -r requirements.txt

Apply Migrations:
python manage.py makemigrations
python manage.py migrate

Create a Superuser:
python manage.py createsuperuser

Run the Server:
python manage.py runserver

Hosting on Render
The API is hosted on Render, a cloud platform that provides easy deployment for web applications.

Deployment Steps:
Push the project to a Git repository.
Create a new web service on Render and link it to the Git repository.
Configure environment variables and settings in the Render dashboard.
Deploy the application.

Access the deployed API via the provided Render URL.

GraphQL Endpoint:
Access the GraphQL interface at /graphql/: https://blog-api-vyot.onrender.com/graphql

JWT Token Endpoints:
Obtain Token: https://blog-api-vyot.onrender.com/api/token
Refresh Token: https://blog-api-vyot.onrender.com/api/token/refresh

Architecture: MTV (Model-Template-View)
This Django Project follows the MTV (Model-Template-View) architecture, which is a variation of the traditional MVC (Model-View-Controller) pattern. The key components in the MTV architecture are:

Model:
The Model represents the data layer. It defines the structure of the data (the database schema) and interacts with the database to perform CRUD operations.
In this project, models like Author, Post, and Comment are defined in the models.py file. These models represent the tables in the database and their relationships.

Template:
The Template is the presentation layer. It controls how data is displayed to the user. In a traditional web application, templates are HTML files that render the data passed from the views.
In this project, since it's an API-based application with GraphQL, the concept of templates is abstracted. The GraphQL queries and mutations serve as the interface between the frontend and the backend, replacing traditional HTML templates.

View:
The View in Django is responsible for processing user requests, interacting with the model, and returning a response. In the context of this project, the views are represented by the GraphQL queries and mutations.
Django's views.py isn't used in the traditional sense here. Instead, GraphQL schema definitions handle the view logic, processing the queries and mutations sent by the clients.

GraphQL:
GraphQL is used in this project to define the schema, queries, and mutations that replace Django's traditional views. It allows for a flexible and powerful API that can be queried by the frontend to fetch or modify data.
The GraphQL queries and mutations are defined in the schema.py file. They interact with the models to fetch, create, update, or delete data.

JWT Authentication:
The project uses JWT (JSON Web Token) authentication for securing the API. Users must obtain a token by providing their credentials, and this token is used to authenticate subsequent API requests.
The authentication logic is integrated with the GraphQL queries and mutations to ensure that only authenticated users can perform certain actions.

Assumptions and Decisions

JWT Authentication: JWT is used for the GraphQL interface to ensure secure access, separating it from the session-based authentication of the admin panel.
Custom Middleware: EnforceJWTAuthenticationMiddleware was created to enforce JWT authentication for GraphQL requests, maintaining the separation between admin and GraphQL authentication.
GraphQL Pagination: Basic pagination has been implemented using skip and limit parameters in the allPosts query.
Django's Built-in User Model: The built-in User model is used for authentication, and posts are linked to users.

Running GraphQL Queries and Mutations
JWT Token Endpoints:
Obtain Token: https://blog-api-vyot.onrender.com/api/token/
Refresh Token: https://blog-api-vyot.onrender.com/api/token/refresh/

Access the GraphQL interface at https://blog-api-vyot.onrender.com/graphql/
Use JWT tokens to authenticate when making requests.
Test various queries and mutations as described in the Testing section.

JWT Authentication
To get authnenticated user token Run:
mutation {
  tokenAuth(username: "admin", password: "admin") {
    token
    refreshToken
  }
}

Add the token to your GraphQL requests as a Bearer token:
{
  "Authorization": "Bearer <your_token_here>"
}

Testing

GraphQL Queries
Fetch All Posts:
query {
  allPosts {
    id
    title
    content
    author {
      username
    }
  }
}

Fetch Post by ID:
query {
  postById(id: 6) {
    title
    content
    comments {
      content
    }
  }
}

GraphQL Mutations
Create a Post:
mutation {
  createPost(title: "New Post", content: "This is a new post content") {
    post {
      id
      title
    }
  }
}

Update a Post:
mutation {
  updatePost(id: 7, title: "Updated Title") {
    post {
      id
      title
    }
  }
}

Delete a Post:
mutation {
  deletePost(id: 1) {
    success
  }
}

Additional Testing
Ensure that only authenticated users can create, update, or delete posts.
Validate the filtering and pagination functionalities for posts.





