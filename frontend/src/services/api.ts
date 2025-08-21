import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface RegionFeature {
  type: string;
  id: number;
  geometry: {
    type: string;
    coordinates: number[][][];
  };
  properties: {
    name: string;
    fiber_status: string;
    area_km2?: number;
    population?: number;
    [key: string]: any;
  };
}

export interface RegionFeatureCollection {
  type: 'FeatureCollection';
  features: RegionFeature[];
}

export const fetchRegions = async (): Promise<RegionFeatureCollection> => {
  const response = await axios.get<RegionFeatureCollection>(`${API_BASE_URL}/regions`);
  return response.data;
};

export const fetchRegionById = async (id: number): Promise<RegionFeature> => {
  const response = await axios.get<RegionFeature>(`${API_BASE_URL}/regions/${id}`);
  return response.data;
};

export const fetchRegionGeoJSON = async (): Promise<RegionFeatureCollection> => {
  const response = await axios.get<RegionFeatureCollection>(`${API_BASE_URL}/regions/geojson`);
  return response.data;
};
