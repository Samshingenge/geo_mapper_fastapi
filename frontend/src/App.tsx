import React, { useState, useEffect } from 'react';
import L from 'leaflet';

import MapComponent from './components/MapComponent'; // Import your map component
import { fetchRegionGeoJSON, RegionFeature } from './services/api'; // Import from your api service
import './App.css'; // Your main app styles

// Define the shape of a region's properties for clarity
// This type can be expanded based on the properties in your GeoJSON
type RegionProperties = {
  id?: number | string;
  name: string;
  fiber_status: 'Active' | 'Planned' | 'Unavailable' | string;
  population?: number;
  area_km2?: number;
  [key: string]: any; // Allow other properties
};

const App: React.FC = () => {
  const [regions, setRegions] = useState<RegionFeature[]>([]);
  const [selectedRegion, setSelectedRegion] = useState<RegionProperties | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch regions data from the API when the component mounts
  useEffect(() => {
    const fetchRegionsData = async () => {
      try {
        const regionsData = await fetchRegionGeoJSON();
        setRegions(regionsData.features);
      } catch (err) {
        console.error('Error fetching regions:', err);
        setError('Failed to load region data. Please check the backend connection.');
      } finally {
        setLoading(false);
      }
    };

    fetchRegionsData();
  }, []); // The empty array [] means this effect runs only once

  // Function to get color based on fiber status
  const getStatusColor = (status: string | undefined): string => {
    if (!status) return '#9E9E9E'; // Grey for unknown status
    
    const statusLower = status.toLowerCase();
    switch (statusLower) {
      case 'active':
        return '#4CAF50'; // Green
      case 'planned':
        return '#FFC107'; // Yellow/Orange
      case 'unavailable':
        return '#F44336'; // Red
      default:
        return '#9E9E9E';
    }
  };

  // Function to define the style for each GeoJSON feature
  const getRegionStyle = (feature: RegionFeature) => {
    return {
      fillColor: getStatusColor(feature.properties.fiber_status),
      weight: 1.5,
      opacity: 1,
      color: 'white',
      fillOpacity: 0.7,
    };
  };

  // Function to handle click events on each feature
  const onFeatureClick = (feature: RegionFeature) => {
    setSelectedRegion({ ...feature.properties, id: feature.id });
  };

  if (loading) {
    return <div className="state-message">Loading map data...</div>;
  }

  if (error) {
    return <div className="state-message error">{error}</div>;
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>Namibia Fiber Coverage Map</h1>
        <p>Visualizing fiber optic coverage across regions</p>
      </header>

      <div className="app-content">
        <div className="map-container">
          <MapComponent
            regions={regions}
            getRegionStyle={getRegionStyle}
            onFeatureClick={onFeatureClick}
          />
        </div>

        <div className="sidebar">
          <h2 className="sidebar-title">Region Information</h2>
          {selectedRegion ? (
            <div className="sidebar-content">
              <h3>{selectedRegion.name || 'Unnamed Region'}</h3>
              <p><strong>Status:</strong> {selectedRegion.fiber_status}</p>
              {selectedRegion.population && (
                <p><strong>Population:</strong> {selectedRegion.population.toLocaleString()}</p>
              )}
              {selectedRegion.area_km2 && (
                <p><strong>Area:</strong> {selectedRegion.area_km2.toLocaleString()} km²</p>
              )}
            </div>
          ) : (
            <div className="sidebar-placeholder">
              Click on a region on the map to see details.
            </div>
          )}

          <div className="legend">
            <h3>Legend</h3>
            <div>
              <span className="legend-color" style={{ backgroundColor: '#4CAF50' }}></span> Active
            </div>
            <div>
              <span className="legend-color" style={{ backgroundColor: '#FFC107' }}></span> Planned
            </div>
            <div>
              <span className="legend-color" style={{ backgroundColor: '#F44336' }}></span> Unavailable
            </div>
          </div>
        </div>
      </div>

      <footer className="app-footer">
        <p>Namibia Fiber Coverage Mapper {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
};

export default App;