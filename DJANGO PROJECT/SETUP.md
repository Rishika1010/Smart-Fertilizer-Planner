# Setup Instructions

## Quick Start Guide

Follow these steps to get the Smart Fertilizer Planner running:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file in the project root (you can copy from `.env.example`):

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Step 3: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Step 5: Load Sample Data (Optional)

Load sample crops and fertilizer products:

```bash
python manage.py load_sample_data
```

This will create:
- 5 sample crops (Wheat, Rice, Corn, Soybean, Tomato)
- 6 sample fertilizer products (Urea, DAP, MOP, NPK variants)

### Step 6: Run the Server

```bash
python manage.py runserver
```

### Step 7: Access the Application

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First Steps After Setup

1. **Register a User Account**
   - Go to http://127.0.0.1:8000/register/
   - Fill in your details
   - Log in with your credentials

2. **Add Crops** (if not using sample data)
   - Navigate to Land Parcels → Manage Crops
   - Add crops with their NPK requirements

3. **Add Fertilizer Products** (if not using sample data)
   - Navigate to Fertilizers → Add New Product
   - Enter product details including NPK percentages and pricing

4. **Create Your First Land Parcel**
   - Go to Land Parcels → Add New Parcel
   - Enter parcel information
   - Assign a crop

5. **Upload Soil Test Data**
   - View your parcel
   - Click "Upload Soil Test"
   - Enter nutrient levels from your soil test report

6. **Generate Recommendation**
   - From the parcel detail page, click "Generate Recommendation"
   - View and export your fertilizer plan

## Troubleshooting

### Migration Issues

If you encounter migration errors:

```bash
python manage.py makemigrations --merge
python manage.py migrate
```

### Static Files Issues

If static files don't load:

```bash
python manage.py collectstatic --noinput
```

### Port Already in Use

If port 8000 is in use, specify a different port:

```bash
python manage.py runserver 8080
```

## Production Deployment

For production:

1. Set `DEBUG=False` in your `.env` file
2. Generate a secure `SECRET_KEY`
3. Configure a production database (PostgreSQL recommended)
4. Set up proper static file serving
5. Configure media file storage
6. Use HTTPS/SSL

## Need Help?

Refer to the main README.md for detailed documentation.

