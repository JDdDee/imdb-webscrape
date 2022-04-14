import { executeQuery } from "./utils/api";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Movie from "./pages/Movies";
import Cast from "./pages/Cast";
import Location from "./pages/Location";

// const queries = {
//   "query-name": (params) => {
//     return "SELECT * FROM table WHERE ${params.column} = ${params.value}";
//   },
// };

// executeQuery(queries[selectedQuery]());

export default function App() {
  async function handleQueryClick() {
    const res = await executeQuery("SELECT * FROM JONATHAN.CUNNING.MOVIE");
    console.log("query result:");
    console.log(res);
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Movie />} />
        <Route path="/cast" element={<Cast />} />
        <Route path="/location" element={<Location />} />
      </Routes>
    </BrowserRouter>
  );
}
