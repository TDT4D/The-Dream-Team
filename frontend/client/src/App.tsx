/* Components, services & etc. */
import { ProjectProvider } from "./services/project/project.provider";
import { AuthProvider } from "./services/auth/auth.provider";
import { Routes } from "./services/router/router.provider";

/* Styling */
import './App.scss';


function App() {
  return (
    <AuthProvider>
      <ProjectProvider>
        <Routes />
      </ProjectProvider>
    </AuthProvider>
  );
}

export default App;
