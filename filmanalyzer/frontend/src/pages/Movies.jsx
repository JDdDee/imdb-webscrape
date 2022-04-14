import React from "react";
import { useNavigate } from "react-router-dom";

export default function Movie() {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col text-center justify-center items-center space-y-12">
      <h1 className="font-bold text-3xl">Welcome to the Film Analyzer</h1>
      <div className="flex flex-row space-x-72 text-2xl items-center">
        <button
          className="bg-slate-300 rounded-md px-3 py-2"
          onClick={() => navigate("/test")}
        >
          Box Office Info
        </button>
        <br></br>
      </div>
      <div className="flex flex-row space-x-20 text-2xl">
        <br></br>
        <button
          className="bg-slate-300 rounded-md px-3 py-2"
          onClick={() => navigate("/test")}
        >
          Ratings
        </button>
      </div>
      <div className="flex flex-row space-x-72 text-2xl">
        <button
          className="bg-slate-300 rounded-md px-3 py-2"
          onClick={() => navigate("/cast")}
        >
          Actor/Cast Member Stats
        </button>
        <br></br>
      </div>
      <div className="flex flex-row space-x-20 text-2xl">
        <br></br>
        <button
          className="bg-slate-300 rounded-md px-3 py-2"
          onClick={() => navigate("/location")}
        >
          Locations Filmed
        </button>
      </div>
    </div>
  );
}
