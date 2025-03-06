/* Components, services & etc. */
import { AuthProvider } from "./services/auth/auth.provider";
import { Routes } from "./services/router/router.provider";

/* Styling */
import './App.scss';


function App() {
  return (
    <AuthProvider>
      <Routes />
    </AuthProvider>
  );
}

export default App;
