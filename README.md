# My EShop

This project is an e-commerce platform built with Django. It includes product management, user authentication, and shopping cart functionality.

## 🚀 Features

- User registration and authentication
- Product and category management
- Shopping cart system
- API support with Django REST Framework
- Extensive test coverage with pytest
- Advanced filtering options for product search

## 🌟 Advantages

- **Scalability** – The project is built with Django, making it easy to scale as needed.
- **Modular Structure** – The application follows Django’s best practices, making it easy to extend and maintain.
- **API Ready** – Fully integrated with Django REST Framework, allowing easy API expansion.
- **Secure Authentication** – Implements Django’s built-in authentication system for secure user management.
- **Customizable** – Can be modified to fit specific business needs.
- **Well-Tested** – Includes numerous automated tests using pytest to ensure reliability and stability.
- **Advanced Filtering** – Products can be filtered based on multiple parameters, improving the user experience.

## 🏗️ Architecture Overview

### Applications

The project is divided into three main Django applications:

1. **Users App** – Handles user authentication, registration, and profile management.
2. **Products App** – Manages product listings and categories.
3. **Cart App** – Manages the shopping cart functionality.

---
## 📂 Users App

### API Endpoints

#### **User Registration**
- **Endpoint:** `POST /api/auth/register/`
- **Description:** Registers a new user.
- **Request Body:**
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
  ```

#### **User Login**
- **Endpoint:** `POST /api/auth/login/`
- **Description:** Authenticates a user and returns a token.
- **Request Body:**
  ```json
  {
    "username": "testuser",
    "password": "securepassword"
  }
  ```
- **Response:**
  ```json
  {
    "token": "abcdef123456"
  }
  ```

#### **User Profile**
- **Endpoint:** `GET /api/auth/profile/`
- **Description:** Retrieves or updates the user profile.
- **Response:**
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
  ```

---
## 🛍️ Products App

### API Endpoints

#### **Get All Products**
- **Endpoint:** `GET /api/products/`
- **Description:** Retrieves a paginated list of all products.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "name": "Laptop",
      "brand": "Asus",
      "description": "A high-performance laptop",
      "price": 1200.99,
      "category": 1
    }
  ]
  ```

#### **Create a New Product**
- **Endpoint:** `POST /api/products/`
- **Description:** Creates a new product.
- **Request Body:**
  ```json
  {
    "name": "Smartphone",
    "brand": "Apple",
    "description": "Latest model with great features",
    "price": 899.99,
    "category": "Electronics"
  }
  ```
- **Response:**
  ```json
  {
    "id": 2,
    "name": "Smartphone",
    "brand": "Apple",
    "description": "Latest model with great features",
    "price": 899.99,
    "category": "Electronics"

  }
  ```

#### **Filter Products**
- **Endpoint:** `GET /api/products/?category=<category_name>&price_min=<min>&price_max=<max>`
- **Description:** Filters products by category, price range, and other attributes.

---
## 🛒 Cart App

### API Endpoints

#### **Add Product to Cart**
- **Endpoint:** `POST /api/cart/add/`
- **Description:** Adds a product to the user’s cart.
- **Request Body:**
  ```json
  {
    "product_id": 1,
    "quantity": 2
  }
  ```
- **Response:**
  ```json
  {
    "message": "Product added to cart"
  }
  ```

#### **View Cart**
- **Endpoint:** `GET /api/cart/`
- **Description:** Retrieves the current contents of the user's cart.

#### **Remove Product from Cart**
- **Endpoint:** `DELETE /api/cart/remove/<id>/`
- **Description:** Removes a product from the cart.

---
## 🧪 Testing

This project is thoroughly tested using **pytest** to ensure high reliability and prevent regressions. The test suite includes:

- Unit tests for models, views, and serializers
- Integration tests for API endpoints
- Functional tests for core user interactions
- Performance testing to optimize response times

Run the test suite with:
```bash
pytest
```

## 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sonwayr/e_shop.git
   cd shop_pr
   ```
2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   pip install -r requirements.txt
   ```
3. **Apply migrations and create a superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. **Run the server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Technologies Used

- Python, Django, Django REST Framework
- PyJWT for authentication
- Django extensions
- Django Filters for advanced product filtering
- HTML, CSS, JavaScript, Bootstrap
- Pytest for automated testing
- SQLite (can be replaced with PostgreSQL)

## 📜 License

This project is licensed under the MIT License.

---

✉️ Contact me: [GitHub](https://github.com/sonwayr), [LinkedIn](https://www.linkedin.com/in/vitalii-lypovetskyi-81233b281/), [Insta](https://www.instagram.com/vetal_l4/), [Telegram](https://t.me/sonwayr)

