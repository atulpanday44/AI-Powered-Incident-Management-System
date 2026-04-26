# AI Incident Management System - React UI

Modern React UI for the AI-Powered Incident Management System. Built with TypeScript, React 18, and modern CSS.

## Features

- **Dashboard**: Real-time statistics and incident overview
- **Incidents Management**: View, filter, and manage incidents with severity and status updates
- **Logs Viewer**: Browse and filter logs from all services
- **Log Ingestion**: Form to submit new logs to the system
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Connected to FastAPI backend via REST API

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Development Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start
```

Application will be available at `http://localhost:3000`

### Environment Variables

Create `.env` file:

```
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_ENVIRONMENT=development
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.tsx      # Page header
│   ├── Sidebar.tsx     # Navigation sidebar
│   ├── StatCard.tsx    # Statistics card
│   ├── Table.tsx       # Generic table component
│   ├── Badge.tsx       # Status/severity badges
│   └── Modal.tsx       # Modal dialog
├── pages/              # Page components
│   ├── Dashboard.tsx   # Dashboard page
│   ├── Incidents.tsx   # Incidents management
│   ├── Logs.tsx        # Logs viewer
│   └── IngestLog.tsx   # Log ingestion form
├── services/           # API communication
│   └── api.ts          # API client
├── hooks/              # Custom React hooks
│   └── useApi.ts       # API hook with loading/error handling
├── styles/             # Styling
│   ├── App.css         # Global styles
│   └── Layout.module.css # Layout styles
├── types/              # TypeScript type definitions
│   └── index.ts        # All types
├── App.tsx             # Main app component
└── index.tsx           # React DOM entry point
```

## Components

### Header
Navigation header with title and actions.

```tsx
<Header title="Dashboard" actions={<button>Refresh</button>} />
```

### Sidebar
Navigation menu with active state management.

```tsx
<Sidebar activePage={currentPage} onNavigate={handleNavigate} />
```

### StatCard
Displays key metrics with icons and optional trends.

```tsx
<StatCard
  title="Open Incidents"
  value={42}
  icon="🔴"
  color="warning"
  trend={5}
/>
```

### Table
Generic, reusable table component with column configuration.

```tsx
<Table
  columns={[
    { header: "Name", accessor: "name" },
    { header: "Status", accessor: "status", render: (value) => <Badge text={value} /> }
  ]}
  data={incidents}
  loading={loading}
  onRowClick={handleRowClick}
/>
```

### Badge
Status/severity indicators.

```tsx
<Badge text="HIGH" type="high" />
<Badge text="OPEN" type="open" />
```

### Modal
Reusable modal dialog.

```tsx
<Modal
  isOpen={isOpen}
  title="Edit Incident"
  onClose={handleClose}
>
  {/* Content */}
</Modal>
```

## Hooks

### useApi
Custom hook for handling API calls with loading and error states.

```tsx
const { data, loading, error, refetch } = useApi(
  () => api.getIncidents(),
  { immediate: true }
);
```

## Pages

### Dashboard
- Real-time statistics
- Recent open incidents
- Key metrics display

### Incidents
- List all incidents
- Filter by service, status, severity
- View incident details
- Update incident status and severity

### Logs
- Browse all logs
- Filter by service and level
- Real-time log viewing

### IngestLog
- Form to submit new logs
- Service, level, and message fields
- Success/error feedback

## API Integration

The `api.ts` service provides methods for all backend endpoints:

```tsx
// Logs
api.ingestLog(log)
api.getLogs(service, level, limit)
api.getLog(logId)

// Incidents
api.createIncident(incident)
api.getIncidents(service, status, severity, limit)
api.getIncident(incidentId)
api.updateIncident(incidentId, update)
api.getStatistics()
api.getOpenIncidents()
api.getCriticalIncidents()
```

## Styling

Global styles use CSS variables for consistent theming:

```css
--primary-color: #2563eb
--danger-color: #dc2626
--success-color: #16a34a
--bg-primary: #ffffff
--text-primary: #1e293b
```

Utility classes:

- `.card` - Card container
- `.badge` - Badge element
- `.btn-primary`, `.btn-secondary`, `.btn-danger` - Buttons
- `.grid`, `.flex` - Layout
- `.text-center`, `.text-muted` - Text utilities
- `.gap-md`, `.mb-lg` - Spacing

## Build for Production

```bash
npm run build
```

Creates optimized production build in `build/` directory.

Serve the build:

```bash
npm install -g serve
serve -s build
```

## Docker

Build Docker image:

```bash
docker build -t incident-ui .
```

Run container:

```bash
docker run -p 3000:3000 incident-ui
```

Or use Docker Compose (see main README).

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Performance

- **Code splitting**: Automatic with React
- **Bundle size**: ~50KB (gzipped)
- **Optimization**: CSS modules, lazy loading
- **Performance**: Lighthouse score 90+

## Development

### Type Checking

```bash
npm run type-check
```

### Formatting

```bash
npm run format
```

### Linting

```bash
npm run lint
```

## Troubleshooting

### CORS Errors

If you see CORS errors, make sure:
1. Backend is running on `localhost:8000`
2. `REACT_APP_API_URL` is correctly set
3. Backend has CORS middleware enabled

### API Connection Failed

```
Error: Failed to fetch
```

Solutions:
- Check backend is running: `curl http://localhost:8000/health`
- Verify `REACT_APP_API_URL` in `.env`
- Check network tab in browser DevTools

### Build Fails

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Contributing

1. Create feature branch
2. Make changes
3. Test locally with `npm start`
4. Build and verify: `npm run build`
5. Commit with clear message

## License

MIT

## Support

For issues with the UI, check:
1. Browser console for errors
2. Network tab for API failures
3. Backend logs for server errors
