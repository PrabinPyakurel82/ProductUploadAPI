# ProductUploadAPI

A **Django REST Framework (DRF)** project that provides CRUD operations for products, along with the ability to **upload product data from CSV or Excel files**. The API also includes **validation** for missing or malformed data.

---

## Features

- CRUD operations for products (`sku`, `name`, `category`, `price`, `stock_qty`, `status`)
- CSV/Excel file upload to bulk import product data
- Simple validation for:
  - Missing required columns
  - Missing or malformed values
  - Invalid numeric values (price, stock)
  - Invalid status (`active` or `inactive`)
---

## Models

**Product**

| Field       | Type      | Description                  |
|------------|----------|------------------------------|
| sku        | Char     | Unique identifier (primary) |
| name       | Char     | Product name                 |
| category   | Char     | Product category             |
| price      | Float    | Product price                |
| stock_qty  | Integer  | Quantity in stock            |
| status     | Char     | `active` or `inactive`      |

---

## API Endpoints

### Standard CRUD

| Method | URL                  | Description              |
|-------|----------------------|--------------------------|
| GET   | `/products/`         | List all products        |
| POST  | `/products/`         | Create a new product     |
| GET   | `/products/{id}/`    | Retrieve a product       |
| PUT   | `/products/{id}/`    | Update a product         |
| DELETE| `/products/{id}/`    | Delete a product         |


### File Upload

| Method | URL                  | Description                  |
|-------|----------------------|------------------------------|
| POST  | `/products/upload/`  | Upload CSV/Excel product file |

**Validation on upload:**

- Missing required values → returns `"Some rows are missing values"`
- Invalid numeric values → returns `"Invalid price"` or `"Invalid stock quantity"`
- Invalid status → must be `"active"` or `"inactive"`

---

## Installation

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:

```bash
python -m venv env
source env/bin/activate  # For Windows use: env\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
Run the following command to apply database migrations:

```bash
python manage.py migrate
```

### 5. Start the Django Development Server
You can now start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

