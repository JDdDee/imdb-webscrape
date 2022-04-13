import React from "react";
import { useNavigate } from "react-router-dom";
import { Chart } from "react-charts";
import { executeQuery } from "../utils/api";
import TextField from "@mui/material/TextField";

export default function Test() {
  async function doQuery() {
    let res = await executeQuery('SELECT * FROM "JONATHAN.CUNNING".MOVIE');
    console.log(res);
  }

  const navigate = useNavigate();
  const data = [
    {
      label: "React Charts",

      data: [
        {
          primary: 1,

          likes: 130,
        },

        {
          primary: 2,

          likes: 150,
        },
        {
          primary: 3,
          likes: 50,
        },
      ],
    },
  ];

  const primaryAxis = React.useMemo(
    () => ({
      getValue: (datum) => datum.primary,
    }),

    []
  );
  const secondaryAxes = React.useMemo(
    () => [
      {
        getValue: (datum) => datum.likes,
      },
    ],

    []
  );
  return (
    <div className="flex-col flex space-y-5 h-full">
      <h1 className="text-3xl font-bold underline text-center">
        Actor/Cast Member Stats
      </h1>
      <div className="flex flex-row justify-center">
        <TextField
          id="outlined-basic"
          variant="outlined"
          label="Search for Actors/Cast"
        />
        <button
          className="flex bg-slate-300 rounded-md px-3 py-3"
          onClick={() => navigate("/")}
        >
          Go
        </button>
      </div>
      <div className="flex flex-row justify-center space-x-72">
        <button
          className="flex bg-slate-300 rounded-md px-3 py-2"
          onClick={() => doQuery()}
        >
          Style
        </button>
        <button
          className="flex bg-slate-300 rounded-md px-3 py-2"
          onClick={() => doQuery()}
        >
          Roles
        </button>
        <button
          className="flex bg-slate-300 rounded-md px-3 py-2"
          onClick={() => doQuery()}
        >
          Profit
        </button>
      </div>
      <div className="flex flex-1 flex-col">
        <div className="flex flex-1">
          <h1 className="flex flex-col justify-center max-w-[5rem] break-all">
            Y-Axis
          </h1>
          <div className="flex-1 relative">
            <Chart
              options={{
                data,

                primaryAxis,

                secondaryAxes,
              }}
            />
          </div>
        </div>
        <div className="flex justify-between">
          <br></br>
          <h1>X-Axis</h1>
          <div className="flex bg-slate-300 rounded-md px-3 py-2">
            <button onClick={() => navigate("/")}>Back</button>
          </div>
        </div>
      </div>
    </div>
  );
}
