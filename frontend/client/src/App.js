import logo from './logo.svg';
import './App.css';

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Base from "./pages/base/base.page";
import Sort from "./pages/sort/sort.page";
import Select from './pages/select/select.page';
import Error from "./pages/error/error.page";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Base />}>
        <Route index element={<Select />} />
        <Route path="sort/:id" element={<Sort />} />
        <Route path="sort" element={<Error reason={"sort without ID!"} />} />
        <Route path="*" element={<Error reason={"Check path!"} />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
