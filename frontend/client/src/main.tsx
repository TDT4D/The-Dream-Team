/* Lib imports */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

/* Components, services & etc. */
import App from './App.tsx'

/* Styling */
import './index.scss'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
