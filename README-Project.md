# Comet 3i/Atlas Real-Time Tracker

## 🌟 Project Overview

A comprehensive real-time comet tracking application that monitors the 3i/Atlas comet using NASA JPL Horizons API data. Features a beautiful space-themed dashboard with proximity visualization and detailed astronomical data.

## ✨ Features

### 🎯 Core Functionality
- **Real-time comet tracking** using NASA JPL Horizons API
- **Proximity visualization** showing Earth-comet relationship
- **Live position data** (Right Ascension, Declination, distances)
- **Velocity tracking** (Radial and Tangential velocities)
- **Orbital mechanics** (Eccentricity, Inclination, Perihelion, etc.)
- **Physical properties** (Magnitude, Coma diameter, Tail length)
- **Visibility information** (Constellation, best viewing times)

### 🎨 Visual Design
- **Space-themed UI** with dark slate color scheme
- **Proximity visualization** with Earth and comet representations
- **Real astronomical background** imagery
- **Animated proximity indicators** based on distance
- **Color-coded data** for easy interpretation
- **Responsive design** for all devices

### 🔧 Technical Features
- **Auto-refresh** every 15 minutes
- **Intelligent caching** to reduce API calls
- **Fallback mechanisms** when APIs are unavailable
- **Error handling** with graceful degradation
- **MongoDB storage** for historical data
- **RESTful API** architecture

## 🏗️ Architecture

### Frontend (React)
- **Framework**: React 19.0.0 with functional components
- **UI Library**: Shadcn/UI with Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Routing**: React Router DOM

### Backend (FastAPI)
- **Framework**: FastAPI with async/await
- **Database**: MongoDB with Motor (async driver)
- **External APIs**: NASA JPL Horizons System
- **Caching**: MongoDB-based intelligent caching
- **Error Handling**: Comprehensive fallback mechanisms

## 📁 Project Structure

```
/app/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/          # Shadcn/UI components
│   │   │   ├── CometTracker.jsx
│   │   │   └── CometProximityVisualization.jsx
│   │   ├── App.js
│   │   └── index.css
│   ├── package.json
│   └── tailwind.config.js
├── backend/                  # FastAPI backend application
│   ├── services/
│   │   └── comet_service.py # NASA JPL API integration
│   ├── routes/
│   │   └── comet_routes.py  # API endpoints
│   ├── server.py           # Main application
│   └── requirements.txt
├── contracts.md            # API contracts documentation
├── test_result.md         # Testing results
└── backend_test.py        # Automated tests
```

## 🚀 API Endpoints

### Comet Tracking
- `GET /api/comet/3i-atlas/current` - Current comet data
- `GET /api/comet/3i-atlas/history?hours=30` - Historical data
- `GET /api/comet/status` - API health status

### Health Check
- `GET /api/` - Base health check

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 18+ and Yarn
- Python 3.11+
- MongoDB
- NASA JPL Horizons API access

### Frontend Setup
```bash
cd frontend
yarn install
yarn start
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Environment Variables
Create `.env` files:

**Frontend (.env)**:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

**Backend (.env)**:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=comet_tracker
```

## 🧪 Testing

### Backend Testing
- **Comprehensive API tests** - 6/6 tests passed
- **NASA JPL integration tests**
- **Error handling verification**
- **Caching mechanism tests**

### Frontend Testing
- **UI component tests** - 9/9 tests passed
- **User interaction testing**
- **Visual design verification**
- **Responsive behavior testing**

## 📊 Data Sources

### Primary: NASA JPL Horizons System
- **Base URL**: `https://ssd.jpl.nasa.gov/api/horizons.api`
- **Comet ID**: `90003242` (3i/Atlas designation)
- **Update Frequency**: Every 15 minutes
- **Fallback**: Intelligent cached data when API unavailable

## 🎨 Visual Assets

### Astronomical Images
- **Comet NEOWISE** photograph for hero background
- **Observatory tracking** imagery
- **Space trajectory** visualizations
- All images sourced ethically from Unsplash

## 📈 Performance

### Optimization Features
- **Intelligent caching** - 15-minute cache duration
- **Lazy loading** for images
- **Optimized bundle size** with code splitting
- **MongoDB indexing** for fast queries
- **Rate limiting** compliance with NASA APIs

## 🔒 Security & Reliability

### Error Handling
- **Graceful degradation** when APIs fail
- **Fallback data** for continuous operation
- **Comprehensive logging** for debugging
- **Input validation** and sanitization

### Monitoring
- **API health checks**
- **Performance metrics**
- **Error tracking**
- **Uptime monitoring**

## 🌍 Browser Support

- **Chrome 90+**
- **Firefox 88+**
- **Safari 14+**
- **Edge 90+**
- **Mobile browsers** (iOS Safari, Chrome Mobile)

## 📝 License

This project is built for educational and astronomical research purposes. NASA data is public domain.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add comprehensive tests
4. Ensure all tests pass
5. Submit pull request

## 📞 Support

For questions about:
- **NASA JPL API**: Consult JPL Horizons documentation
- **Technical issues**: Check test_result.md for debugging info
- **Feature requests**: Submit via GitHub issues

## 🔮 Future Enhancements

### Planned Features
- **Multiple comet tracking**
- **Historical trajectory visualization**
- **Email notifications** for proximity alerts
- **Mobile app** (React Native)
- **3D orbital visualization**
- **Social sharing** features
- **Advanced filtering** and search

### Technical Improvements
- **WebSocket real-time updates**
- **Progressive Web App** features
- **Advanced caching strategies**
- **Machine learning** for prediction models
- **GraphQL API** implementation

---

Built with ❤️ for astronomical enthusiasts and space tracking professionals.

**Last Updated**: September 5, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅