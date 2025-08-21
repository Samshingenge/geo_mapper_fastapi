import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { RegionFeature } from '../services/api';
import polylabel from 'polylabel';

// Define manual center coordinates for problematic regions
const manualCenters: { [key: string]: L.LatLngTuple } = {
  'Kunene': [-19.0, 14.0],
  'Oshana': [-18.0, 15.7],
  'Oshikoto': [-18.5, 16.5],
  'Omaheke': [-22.0, 19.5],
  'Zambezi': [-17.8, 24.0]
};

// Fix for default marker icons in React Leaflet
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Define the props that this component will receive from App.tsx
interface MapComponentProps {
  regions: RegionFeature[];
  getRegionStyle: (feature: RegionFeature) => object;
  onFeatureClick: (feature: RegionFeature) => void;
}

const MapComponent: React.FC<MapComponentProps> = ({ regions, getRegionStyle, onFeatureClick }) => {
  // Function to calculate the visual center of a GeoJSON feature
  const getCenter = (feature: RegionFeature): L.LatLngTuple => {
    const regionName = feature.properties.name;

    // Use manual center if available, otherwise calculate it
    if (manualCenters[regionName]) {
      return manualCenters[regionName];
    }

    // polylabel expects an array of polygons
    const polygon = feature.geometry.coordinates;

    // Find the pole of inaccessibility, which is the visual center
    const center = polylabel(polygon, 1.0);
    return [center[1], center[0]]; // Leaflet expects [lat, lng]
  };

  return (
    <MapContainer center={[-22, 17]} zoom={6} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {regions.map((region, index) => {
        const center = getCenter(region);
        const style = getRegionStyle(region);
        const { name, fiber_status, population, area_km2 } = region.properties;

        return (
          <CircleMarker
            key={index}
            center={center}
            pathOptions={style}
            radius={10}
            eventHandlers={{
              click: () => onFeatureClick(region),
            }}
          >
            <Popup>
              <div>
                <h3 style={{ margin: 0, paddingBottom: '0.5rem', borderBottom: '1px solid #eee' }}>{name || 'Unnamed Region'}</h3>
                <p><strong>Status:</strong> {fiber_status || 'N/A'}</p>
                {population && <p><strong>Population:</strong> {population.toLocaleString()}</p>}
                {area_km2 && <p><strong>Area:</strong> {area_km2.toLocaleString()} km²</p>}
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
};

export default MapComponent;