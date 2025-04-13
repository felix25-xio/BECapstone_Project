📦 Inventory Management API A simple RESTful Inventory Management API built with Django and Django REST Framework to help track inventory items, stock changes, and user activities for small to medium-sized businesses.

✅ Features ✅ User Registration (JWT Authentication) ✅ Add, View, Update Inventory Items ✅ Track Inventory Changes (Restock / Sale) ✅ Filter Inventory Levels (by category, price, quantity) ✅ View Inventory Change History ✅ Pagination and Sorting of Inventory Items ✅ Category Management ❌ Delete Inventory Items (pending final debugging)

🚀 Technologies Used Python 3 Django Django REST Framework SimpleJWT (for Authentication) PostgreSQL (DB)

🛠️ Installation 1. Clone the repository git clone cd

2. Create and activate virtual environment python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies pip install -r requirements.txt

4. Run migrations python manage.py makemigrations python manage.py migrate

5. Create a superuser (for admin access) python manage.py createsuperuser

6. Run the development server python manage.py runserver

🔐 Authentication All modifying endpoints require JWT authentication.

1. Register a new user POST /api/auth/register/ { "username": "yourusername", "email": "youremail@example.com", "password": "yourpassword" }

2. Login to get tokens POST /api/token/ { "username": "yourusername", "password": "yourpassword" }

3. Use the access token in headers Authorization: Bearer <access_token>

📂 API Endpoints

🔧 Inventory Method Endpoint Description GET /api/inventory/ List inventory items POST /api/inventory/ Add inventory item GET /api/inventory// View specific item PUT /api/inventory// Update item DELETE /api/inventory// Delete item (not working)

📊 Inventory Levels GET /api/inventory-levels/?category=food&min_price=10&low_stock=5

🔁 Inventory Changes Method Endpoint Description GET /api/inventory-changes/ All changes (admin access) GET /api/inventory/<item_id>/changes/ History per item

🗂️ Categories Method Endpoint Description GET/POST /api/categories/ List or create categories GET/PUT/DELETE /api/categories// Detail, update, or delete

🔍 Filtering & Pagination Ordering supported on name, quantity, price, date_added Example: /api/inventory/?ordering=price

Pagination enabled by default (if you added it via DRF settings).

💡 Notes All modifying actions (POST, PUT) require authentication. You can view and manage inventory through Django Admin (/admin). You must attach a valid JWT token to modify any inventory data.

📽️ Loom Demo Include your Loom video link here after recording your walkthrough of the API.

🧠 Known Issues DELETE endpoint currently triggers an error due to unresolved ProgrammingError. The issue is likely due to missing on_delete=models.CASCADE or integrity constraints.

🙏 Acknowledgments Django REST Framework ALX Backend Engineering Team
