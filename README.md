# Namibia Geo-Coverage Mapper

A web application for visualizing fiber coverage across different regions in Namibia. This project provides an interactive map interface to view and manage fiber coverage status across various regions in Namibia.

## Features

- Interactive map showing regions of Namibia
- Color-coded regions based on fiber coverage status (Active, Planned, Unavailable)
- Detailed information about each region's fiber status
- RESTful API for accessing coverage data
- Docker-based development and production environments

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy + GeoAlchemy2
- PostGIS (PostgreSQL with spatial extensions)
- Docker

### Frontend
- React
- Leaflet for interactive maps
- TypeScript
- Axios for API requests

## Prerequisites

- Docker and Docker Compose
- Node.js (for frontend development, optional with Docker)
- Python 3.11 (for backend development, optional with Docker)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/namibia-geo-coverage-mapper.git
cd namibia-geo-coverage-mapper
```

### 2. Set up environment variables

Create a `.env` file in the root directory with the following content:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=geo_mapper

# Application
APP_ENV=development
DEBUG=True
```

### 3. Start the application with Docker Compose

```bash
docker-compose up --build
```

This will start the following services:
- PostgreSQL with PostGIS (port 5432)
- FastAPI backend (port 8000)
- React frontend (port 3000)

### 4. Access the application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

## Project Structure

```
.
├── backend/                  # FastAPI backend
│   ├── app/                  # Application code
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core functionality
│   │   ├── db/               # Database configuration
│   │   ├── models/           # Database models
│   │   └── schemas/          # Pydantic schemas
│   ├── data/                 # GeoJSON data files
│   ├── scripts/              # Utility scripts
│   ├── Dockerfile            # Backend Dockerfile
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React frontend
│   ├── public/               # Static files
│   ├── src/                  # Source code
│   ├── Dockerfile            # Frontend Dockerfile
│   └── package.json          # Node.js dependencies
├── docker-compose.yml        # Docker Compose configuration
└── README.md                # This file
```

## API Endpoints

### Regions

- `GET /api/v1/regions/` - List all regions
- `GET /api/v1/regions/geojson` - Get regions in GeoJSON format
- `GET /api/v1/regions/{region_id}` - Get a specific region by ID
- `GET /api/v1/regions/name/{region_name}` - Get a region by name
- `GET /api/v1/regions/coverage/{region_name}` - Get fiber coverage for a region

## Development

### Backend Development

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Development

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## Deployment

### Production Build

1. Update the `.env` file with production settings:
   ```env
   APP_ENV=production
   DEBUG=False
   ```

2. Build and start the production containers:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenStreetMap](https://www.openstreetmap.org/) for map data
- [PostGIS](https://postgis.net/) for spatial database functionality
- [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- [React Leaflet](https://react-leaflet.js.org/) for interactive maps
