# SideEyes Frontend

A modern, visually appealing Vue.js 3 frontend application for displaying scraped data collected by the SideEyes web scraper.

## Features

- **Dashboard**: Overview of all scraped data statistics
- **Quotes**: Browse and search inspiring quotes with filtering
- **Books**: View book collection with sorting and filtering
- **Sites**: Information about all scraped websites
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Beautiful UI**: Modern gradient backgrounds and smooth animations
- **Real-time Data**: Live data from the SideEyes API

## Prerequisites

- Node.js (v14+)
- npm or yarn package manager

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
npm run dev
```

The application will open at `http://localhost:3000`

Make sure the backend API is running on `http://localhost:5000`

## Build

Build for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── assets/
│   │   └── styles.css          # Global styles
│   ├── services/
│   │   └── api.js              # API communication
│   ├── views/
│   │   ├── Home.vue            # Dashboard page
│   │   ├── Quotes.vue          # Quotes page
│   │   ├── Books.vue           # Books page
│   │   └── Sites.vue           # Sites information page
│   ├── router/
│   │   └── index.js            # Vue Router configuration
│   ├── App.vue                 # Main app component
│   └── main.js                 # App entry point
├── index.html                  # HTML template
├── package.json                # Project dependencies
├── vite.config.js              # Vite configuration
└── README.md                   # This file
```

## Technologies Used

- **Vue 3**: Progressive JavaScript framework
- **Vue Router 4**: Client-side routing
- **Vite**: Fast build tool and development server
- **CSS3**: Styling with modern features (gradients, flexbox, grid)

## API Integration

The frontend communicates with the SideEyes API at `http://localhost:5000/api`

### Available Endpoints

- `GET /api/data` - Get all scraped data
- `GET /api/quotes` - Get all quotes
- `GET /api/books` - Get all books
- `GET /api/sites` - Get all sites

## Features in Detail

### Home (Dashboard)
- Statistics cards showing counts
- Last updated timestamp
- Feature overview cards

### Quotes
- Search functionality
- Tag-based filtering
- Quote cards with author and tags
- Source attribution

### Books
- Search by title or author
- Sort by title, rating, or price
- Star ratings
- Availability status
- Price information

### Sites
- Overview of all scraped websites
- Record counts per site
- Active status indicators
- Tags for categorization
- Direct links to source websites

## Styling

The application uses a modern design system with:
- **Primary Colors**: Indigo (#6366f1), Purple (#764ba2)
- **Gradients**: Linear gradients from indigo to purple
- **Cards**: Rounded corners with shadows and hover effects
- **Spacing**: Consistent 8px grid system
- **Fonts**: System font stack for optimal performance

## Performance Optimizations

- Code splitting with Vue Router
- Lazy loading of components
- Optimized animations with CSS transforms
- Efficient event handling
- Minimal re-renders

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project as you wish.

## Support

For issues or questions about the frontend, please check:
1. The backend API is running and accessible
2. Network tab in browser dev tools for API errors
3. Browser console for JavaScript errors

## Future Enhancements

- [ ] Data export functionality
- [ ] Advanced filtering options
- [ ] Data visualization charts
- [ ] Dark mode support
- [ ] Pagination for large datasets
- [ ] Favorites/bookmarking feature
- [ ] Data refresh scheduling
