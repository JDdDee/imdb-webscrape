import React from "react";
import { useNavigate } from "react-router-dom";
import { Chart } from "react-charts";
import { executeQuery } from "../utils/api";
import TextField from "@mui/material/TextField";

export default function Test() {
  const [inputText, setInputText] = React.useState("");
  const [data, setData] = React.useState([
    { label: "React Charts", data: [{ x: 0, y: 0 }] },
  ]);
  const [yaxis, setYaxis] = React.useState("Y-Axis");
  const [xaxis, setXaxis] = React.useState("X-Axis");

  async function searchCast(name) {
    let res = await executeQuery(
      'SELECT * FROM "JONATHAN.CUNNING".CAST WHERE lower (CASTNAME)=\'' +
        name +
        "'"
    );
    return res;
  }

  async function setRoles() {
    let temp = await searchCast(inputText);
    temp = temp.rows;
    console.log(temp);
    setData([
      {
        label: "Roles",
        data: temp.map(function (row) {
          return { x: row.BIRTH, y: row.CASTID };
        }),
      },
    ]);
    setYaxis("Cast ID");
    setXaxis("Birth Year");
  }

  const navigate = useNavigate();

  const primaryAxis = React.useMemo(
    () => ({
      getValue: (datum) => datum.x,
    }),

    []
  );
  const secondaryAxes = React.useMemo(
    () => [
      {
        getValue: (datum) => datum.y,
      },
    ],

    []
  );

  let inputLog = (e) => {
    var lowerCase = e.target.value.toLowerCase();
    setInputText(lowerCase);
  };
  return (
    <div className="flex-col flex space-y-5 h-full">
      <h1 className="text-3xl font-bold underline text-center">
        Actor/Cast Member Stats
      </h1>
      <div className="flex flex-row justify-center">
        <TextField
          id="outlined-basic"
          onChange={inputLog}
          variant="outlined"
          label="Search for Actors/Cast"
        />
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
          onClick={() => setRoles()}
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
            {yaxis}
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
          <h1>{xaxis}</h1>
          <div className="flex bg-slate-300 rounded-md px-3 py-2">
            <button onClick={() => navigate("/")}>Back</button>
          </div>
        </div>
      </div>
    </div>
  );
}
