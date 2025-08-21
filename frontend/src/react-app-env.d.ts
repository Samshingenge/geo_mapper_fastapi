/// <reference types="react-scripts" />

// Fix for Leaflet type definitions
import 'leaflet';

declare module 'leaflet' {
  namespace Icon {
    interface Default {
      _getIconUrl: string;
    }
  }
}

// Fix for CSS modules
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

// Fix for image imports
declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.gif';
declare module '*.svg' {
  import * as React from 'react';
  export const ReactComponent: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  const src: string;
  export default src;
}
