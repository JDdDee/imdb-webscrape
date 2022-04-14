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
  const [searchBy, setSearchBy] = React.useState("CASTNAME");

  async function searchRating(name) {
    let res = "";
    if (searchBy == "CASTNAME") {
      res = await executeQuery(
        'SELECT IMDBRATING, RELEASEDATE FROM (SELECT MOVIEID FROM "JONATHAN.CUNNING".WORKSON INNER JOIN (SELECT CASTID FROM "JONATHAN.CUNNING".CAST WHERE lower ( CASTNAME )= :name ) A ON "JONATHAN.CUNNING".WORKSON.CASTID = A.CASTID) B INNER JOIN "JONATHAN.CUNNING".MOVIE ON B.MOVIEID = "JONATHAN.CUNNING".MOVIE.MOVIEID',
        [name]
      );
    } else {
      res = await executeQuery(
        'SELECT IMDBRATING, RELEASEDATE FROM (SELECT MOVIEID FROM "JONATHAN.CUNNING".WORKSON WHERE CASTID = :name) B INNER JOIN "JONATHAN.CUNNING".MOVIE ON B.MOVIEID = "JONATHAN.CUNNING".MOVIE.MOVIEID',
        [parseInt(name)]
      );
    }
    return res;
  }

  async function searchGross(name) {
    let res = "";
    if (searchBy == "COUNTRY") {
      res = await executeQuery(
        'SELECT MOVIEID, GrossingWorld,releasedate FROM (SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE lower (COUNTRY) = :name) natural join ("JONATHAN.CUNNING".MOVIE)',
        [name]
      );
    } else if (searchBy == "LOCATIONNAME") {
      res = await executeQuery(
        'SELECT GrossingWorld,releasedate FROM (SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE lower (LOCATIONNAME) = :name) natural join ("JONATHAN.CUNNING".MOVIE)',
        [name]
      );
    } else {
      res = await executeQuery(
        'SELECT GrossingWorld,releasedate FROM (SELECT * FROM "JONATHAN.CUNNING".FILMEDAT natural join "JONATHAN.CUNNING".LOCATION WHERE LOCATIONID = :name) natural join ("JONATHAN.CUNNING".MOVIE)',
        [parseInt(name)]
      );
    }
    console.log(res);
    return res;
  }

  async function searchGrossUSCA(name) {
    let res = "";
    if (searchBy == "CASTNAME") {
      res = await executeQuery(
        'SELECT GROSSINGUSCA, RELEASEDATE FROM (SELECT MOVIEID FROM "JONATHAN.CUNNING".WORKSON INNER JOIN (SELECT CASTID FROM "JONATHAN.CUNNING".CAST WHERE lower ( CASTNAME )= :name ) A ON "JONATHAN.CUNNING".WORKSON.CASTID = A.CASTID) B INNER JOIN "JONATHAN.CUNNING".MOVIE ON B.MOVIEID = "JONATHAN.CUNNING".MOVIE.MOVIEID',
        [name]
      );
    } else {
      res = await executeQuery(
        'SELECT GROSSINGUSCA, RELEASEDATE FROM (SELECT MOVIEID FROM "JONATHAN.CUNNING".WORKSON WHERE CASTID = :name) B INNER JOIN "JONATHAN.CUNNING".MOVIE ON B.MOVIEID = "JONATHAN.CUNNING".MOVIE.MOVIEID',
        [parseInt(name)]
      );
    }
    return res;
  }

  async function setRoles() {
    let temp = await searchRating(inputText);

    temp = temp.rows;
    if (temp.length == 0) {
      console.log(searchBy);
      return;
    }
    temp = temp.filter((a) => a.RELEASEDATE != null && a.IMDBRATING != null);
    temp = temp.sort(
      (a, b) => new Date(a.RELEASEDATE) - new Date(b.RELEASEDATE)
    );
    temp = temp.map(function (row) {
      return {
        RELEASEDATE: row.RELEASEDATE.substr(0, 10),
        IMDBRATING: row.IMDBRATING,
      };
    });
    console.log(temp);
    setData([
      {
        label: "Ratings",
        data: temp.map(function (row) {
          return { x: new Date(row.RELEASEDATE), y: row.IMDBRATING };
        }),
      },
    ]);
    setYaxis("IMDb Rating");
    setXaxis("Year of Release");
  }

  async function setGross() {
    let temp = await searchGross(inputText);

    temp = temp.rows;
    if (temp.length == 0) {
      console.log(searchBy);
      return;
    }
    temp = temp.filter((a) => a.RELEASEDATE != null && a.GROSSINGWORLD != null);
    temp = temp.sort(
      (a, b) => new Date(a.RELEASEDATE) - new Date(b.RELEASEDATE)
    );
    console.log(temp);
    temp = temp.map(function (row) {
      return {
        RELEASEDATE: row.RELEASEDATE.substr(0, 10),
        GROSSINGWORLD: row.GROSSINGWORLD,
      };
    });
    console.log(temp);
    setData([
      {
        label: "Grossing",
        data: temp.map(function (row) {
          return { x: new Date(row.RELEASEDATE), y: row.GROSSINGWORLD };
        }),
      },
    ]);
    setYaxis("Grossing Worldwide");
    setXaxis("Year of Release");
  }

  async function setBoth() {
    let temp = await searchGross(inputText);

    temp = temp.rows;
    if (temp.length == 0) {
      console.log(searchBy);
      return;
    }
    temp = temp.filter((a) => a.RELEASEDATE != null && a.GROSSINGWORLD != null);
    temp = temp.sort(
      (a, b) => new Date(a.RELEASEDATE) - new Date(b.RELEASEDATE)
    );
    temp = temp.map(function (row) {
      return {
        RELEASEDATE: row.RELEASEDATE.substr(0, 10),
        GROSSINGWORLD: row.GROSSINGWORLD,
      };
    });

    let temp1 = await searchRating(inputText);

    temp1 = temp1.rows;
    if (temp1.length == 0) {
      console.log(searchBy);
      return;
    }
    temp1 = temp1.filter((a) => a.RELEASEDATE != null && a.IMDBRATING != null);
    temp1 = temp1.sort(
      (a, b) => new Date(a.RELEASEDATE) - new Date(b.RELEASEDATE)
    );
    temp1 = temp1.map(function (row) {
      return {
        RELEASEDATE: row.RELEASEDATE.substr(0, 10),
        IMDBRATING: row.IMDBRATING,
      };
    });
    console.log(temp);
    setData([
      {
        label: "Grossing",
        data: temp.map(function (row) {
          return { x: new Date(row.RELEASEDATE), y: row.GROSSINGWORLD };
        }),
      },
      {
        label: "IMDb Rating",
        data: temp1.map(function (row) {
          return { x: new Date(row.RELEASEDATE), y: row.IMDBRATING };
        }),
        secondaryAxisId: "2",
      },
    ]);
    setYaxis("Grossing US/CA");
    setXaxis("Year of Release");
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
