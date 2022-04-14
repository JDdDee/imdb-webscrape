import React from "react";
import { useNavigate } from "react-router-dom";
import { Chart } from "react-charts";
import { executeQuery } from "../utils/api";
import TextField from "@mui/material/TextField";

export default function Test() {
  const [inputText, setInputText] = React.useState("");
  const [yaxis2, setYaxis2] = React.useState("");
  const [data, setData] = React.useState([
    { label: "React Charts", data: [{ x: 0, y: 0 }] },
  ]);
  const [yaxis, setYaxis] = React.useState("Y-Axis");
  const [xaxis, setXaxis] = React.useState("X-Axis");
  const [searchBy, setSearchBy] = React.useState("CASTNAME");

  async function searchRating(name) {
    let res = "";
    if (searchBy == "COUNTRY") {
      res = await executeQuery(
        'SELECT AVG(IMDBRATING) as IMDBRATING, yr FROM ( SELECT imdbrating, extract(year from releasedate) as yr FROM ( SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE lower (COUNTRY) = :name) natural join ("JONATHAN.CUNNING".MOVIE) ) where yr > 1976 group by YR',
        [name]
      );
    } else if (searchBy == "LOCATIONNAME") {
      res = await executeQuery(
        'SELECT AVG(IMDBRATING) as IMDBRATING, yr FROM ( SELECT imdbrating, extract(year from releasedate) as yr FROM ( SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE lower (LOCATIONNAME) = :name) natural join ("JONATHAN.CUNNING".MOVIE) ) where yr > 1976 group by YR',
        [name]
      );
    } else {
      res = await executeQuery(
        'SELECT AVG(IMDBRATING) as IMDBRATING, yr FROM ( SELECT imdbrating, extract(year from releasedate) as yr FROM ( SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE LOCATIONID = :name) natural join ("JONATHAN.CUNNING".MOVIE) ) where yr > 1976 group by YR',
        [parseInt(name)]
      );
    }
    console.log(res);
    return res;
  }

  async function searchGross(name) {
    let res = "";
    if (searchBy == "COUNTRY") {
      res = await executeQuery(
        'SELECT FLOOR(AVG(GROSSINGWORLD)) as GROSSINGWORLD, YR FROM ( SELECT GROSSINGWORLD, extract(year from releasedate) as YR FROM ( SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE lower (COUNTRY) = :name) natural join ("JONATHAN.CUNNING".MOVIE) ) where YR > 1976 group by YR',
        [name]
      );
    } else if (searchBy == "LOCATIONNAME") {
      res = await executeQuery(
        'SELECT FLOOR(AVG(GROSSINGWORLD)) as GROSSINGWORLD, YR FROM ( SELECT GROSSINGWORLD, extract(year from releasedate) as YR FROM ( SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE lower (LOCATIONNAME) = :name) natural join ("JONATHAN.CUNNING".MOVIE) ) where YR > 1976 group by YR',
        [name]
      );
    } else {
      res = await executeQuery(
        'SELECT FLOOR(AVG(GROSSINGWORLD)) as GROSSINGWORLD, YR FROM ( SELECT GROSSINGWORLD, extract(year from releasedate) as YR FROM ( SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE LOCATIONID = :name) natural join ("JONATHAN.CUNNING".MOVIE) ) where YR > 1976 group by YR',
        [parseInt(name)]
      );
    }
    console.log(res);
    return res;
  }

  async function setRoles() {
    let temp = await searchRating(inputText);
    console.log(temp);
    temp = temp.rows;
    if (temp.length == 0) {
      console.log(searchBy);
      return;
    }
    temp = temp.filter((a) => a.YR != null && a.IMDBRATING != null);
    temp = temp.sort((a, b) => a.YR - b.YR);
    console.log(temp);
    setData([
      {
        label: "Ratings",
        data: temp.map(function (row) {
          return { x: new Date(row.YR, 0), y: row.IMDBRATING };
        }),
      },
    ]);
    setYaxis("IMDb Rating");
    setXaxis("Year of Release");
    setYaxis2("");
  }

  async function setGross() {
    let temp = await searchGross(inputText);

    temp = temp.rows;
    if (temp.length == 0) {
      console.log(searchBy);
      return;
    }
    console.log(temp);
    temp = temp.filter((a) => a.YR != null && a.GROSSINGWORLD != null);

    temp = temp.sort((a, b) => a.YR - b.YR);
    console.log(temp);
    setData([
      {
        label: "Grossing",
        data: temp.map(function (row) {
          return { x: new Date(row.YR, 1), y: row.GROSSINGWORLD };
        }),
      },
    ]);
    setYaxis("Grossing Worldwide");
    setXaxis("Year of Release");
    setYaxis2("");
  }

  async function setBoth() {
    let temp = await searchGross(inputText);

    temp = temp.rows;
    if (temp.length == 0) {
      console.log(searchBy);
      return;
    }

    temp = temp.filter((a) => a.YR != null && a.GROSSINGWORLD != null);

    temp = temp.sort((a, b) => a.YR - b.YR);

    let temp1 = await searchRating(inputText);
    console.log(temp1);
    temp1 = temp1.rows;
    if (temp1.length == 0) {
      console.log(searchBy);
      return;
    }
    temp1 = temp1.filter((a) => a.YR != null && a.IMDBRATING != null);
    temp1 = temp1.sort((a, b) => a.YR - b.YR);

    // console.log(temp);
    // console.log(temp1);
    setData([
      {
        label: "Grossing",
        data: temp.map(function (row) {
          return { x: new Date(row.YR, 0), y: row.GROSSINGWORLD };
        }),
      },
      {
        label: "IMDb Rating",
        data: temp1.map(function (row) {
          return { x: new Date(row.YR, 0), y: row.IMDBRATING };
        }),
        secondaryAxisId: "2",
      },
    ]);

    setYaxis("Grossing Worldwide");
    setXaxis("Year of Release");
    setYaxis2("IMDb Rating");
    return;
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
      {
        id: "2",
        getValue: (datum) => datum.y,
        elementType: "line",
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
        Locations Filmed
      </h1>
      <div className="flex flex-row justify-center space-x-5">
        <TextField
          id="outlined-basic"
          onChange={inputLog}
          variant="outlined"
          label="Search for Location"
        />
        <div
          className="flex flex-row space-x-5 items-center"
          onChange={(event) => setSearchBy(event.target.value)}
        >
          <input
            type="radio"
            name="input"
            value="LOCATIONID"
            className="flex bg-slate-300 rounded-md p-3"
          />
          Location ID
          <input
            type="radio"
            name="input"
            value="LOCATIONNAME"
            className="flex bg-slate-300 rounded-md p-3"
          />
          Location Name
          <input
            type="radio"
            name="input"
            value="COUNTRY"
            className="flex bg-slate-300 rounded-md p-3"
          />
          Country
        </div>
      </div>
      <div className="flex flex-row justify-center space-x-72">
        <button
          className="flex bg-slate-300 rounded-md px-3 py-2"
          onClick={() => setRoles()}
        >
          IMDb Ratings of Movies
        </button>
        <button
          className="flex bg-slate-300 rounded-md px-3 py-2"
          onClick={() => setGross()}
        >
          Grossing Worldwide
        </button>
        <button
          className="flex bg-slate-300 rounded-md px-3 py-2"
          onClick={() => setBoth()}
        >
          Both
        </button>
      </div>
      <div className="flex flex-1 flex-col">
        <div className="flex flex-1">
          <h1 className="flex flex-col justify-center max-w-[60rem] break-all">
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
          <h1 className="flex flex-col justify-center max-w-[60rem] break-all">
            {yaxis2}
          </h1>
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
