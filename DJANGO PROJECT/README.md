# Smart Fertilizer Planner

A comprehensive Django web application for generating customized fertilizer input plans for land parcel optimization. The system helps farmers and agricultural professionals optimize nutrient use, reduce costs, and improve crop yield through data-driven decision support.

## Features

### 🔐 User Authentication
- User registration and login system
- User profile management
- Secure session management

### 📍 Land Parcel Management
- Add, edit, and delete land parcels
- Assign crops to parcels
- Track parcel details (location, area, soil type)
- Multiple parcel management per user

### 🌾 Crop Management
- Define crop types with nutrient requirements (N-P-K)
- Track nitrogen, phosphorus, and potassium requirements per crop
- Flexible crop database

### 🧪 Soil Test Data
- Upload soil test reports (PDF, DOC, CSV, Excel)
- Enter soil nutrient levels (N, P, K)
- Record pH levels and organic matter percentage
- Historical soil test tracking

### 💊 Fertilizer Product Management
- Add fertilizer products with NPK ratios
- Set pricing per unit (kg, ton, bag)
- Track active/inactive products
- Product search and filtering

### 🧮 Automated Recommendation Engine
- **Intelligent Nutrient Calculation**: Converts soil test data from ppm to kg/ha
- **Deficit Analysis**: Calculates nutrient deficits based on crop requirements
- **Fertilizer Matching**: Automatically selects optimal fertilizers
- **Cost Estimation**: Provides total cost estimates for recommendations
- **Area-based Calculations**: Considers parcel area in recommendations

### 📊 Reports & Export
- Detailed recommendation reports
- **PDF Export**: Professional formatted PDF reports
- **CSV Export**: Data export for analysis
- Historical recommendation tracking
- Status tracking (Draft, Finalized, Applied)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd "DJANGO PROJECT"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Load sample data (optional)**
   You can create sample crops and fertilizer products through the admin interface or directly in the application.

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Main application: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

## Usage Guide

### Getting Started

1. **Register an Account**
   - Click "Register" on the homepage
   - Fill in your details and create an account
   - Log in with your credentials

2. **Add a Crop**
   - Navigate to "Land Parcels" → "Manage Crops"
   - Add crop details including NPK requirements

3. **Create a Land Parcel**
   - Go to "Land Parcels" → "Add New Parcel"
   - Enter parcel details (name, location, area)
   - Assign a crop to the parcel
   - Select soil type

4. **Upload Soil Test Data**
   - View your parcel details
   - Click "Upload Soil Test"
   - Enter nutrient levels from your soil test report
   - Optionally upload the test report file

5. **Generate Recommendation**
   - From the parcel detail page, click "Generate Recommendation"
   - The system will automatically calculate fertilizer needs
   - View the detailed recommendation with fertilizer products and costs

6. **Export Reports**
   - View recommendation details
   - Click "Export PDF" or "Export CSV"
   - Download and share your fertilizer plan

### Managing Fertilizer Products

- Add fertilizer products with NPK percentages
- Set pricing to get accurate cost estimates
- Mark products as active/inactive
- Search and filter products

## Project Structure

```
fertilizer_planner/
├── accounts/           # User authentication and profiles
├── parcels/            # Land parcel and crop management
├── fertilizers/        # Fertilizer products and recommendations
├── reports/            # Report viewing and export
├── fertilizer_planner/ # Project settings
├── templates/          # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # Uploaded files
└── manage.py          # Django management script
```

## Key Models

- **UserProfile**: Extended user information
- **LandParcel**: Land parcel details
- **Crop**: Crop definitions with nutrient requirements
- **SoilTest**: Soil test data and reports
- **FertilizerProduct**: Available fertilizer products
- **FertilizerRecommendation**: Generated recommendations
- **RecommendationItem**: Individual fertilizer items in recommendations

## Recommendation Algorithm

The system uses a sophisticated algorithm to calculate fertilizer needs:

1. **Soil Analysis**: Converts ppm values to kg/ha using soil depth and bulk density
2. **Deficit Calculation**: Compares crop requirements with soil availability
3. **Efficiency Factor**: Accounts for fertilizer use efficiency (typically 50%)
4. **Fertilizer Selection**: Matches fertilizers based on nutrient content
5. **Cost Calculation**: Estimates total costs based on current pricing

## Technologies Used

- **Django 4.2.7**: Web framework
- **Bootstrap 5**: Frontend styling
- **ReportLab**: PDF generation
- **Crispy Forms**: Form styling
- **SQLite**: Database (default, can be changed for production)

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Update `SECRET_KEY` with a secure key
3. Configure a production database (PostgreSQL recommended)
4. Set up static file serving (WhiteNoise or similar)
5. Configure media file storage (AWS S3, etc.)
6. Set up proper security headers
7. Use HTTPS/SSL

## Contributing

This is a Django project following standard Django conventions. When contributing:

- Follow PEP 8 style guidelines
- Write clear commit messages
- Test your changes thoroughly
- Update documentation as needed

## License

This project is created for educational and agricultural use.

## Support

For issues or questions, please refer to the Django documentation or create an issue in the project repository.

---

**Optimize nutrient use, reduce costs, improve yields!** 🌾

