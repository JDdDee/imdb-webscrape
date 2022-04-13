const path = require("path");
const express = require("express");
const cors = require("cors");
const { connection, initConnection, getConnection } = require("./db");

class Application {
  expressApp;

  async connect() {
    if (!connection) {
      try {
        await initConnection();
      } catch (err) {
        console.error("Error connecting to database: ", err);
      }
    }
  }

  async init() {
    await this.connect();

    this.expressApp = express();

    this.expressApp.use(express.json());
    this.expressApp.use(express.urlencoded({ extended: true }));

    const corsOptions = {
      origin: "*",
    };

    this.expressApp.use(cors(corsOptions));

    if (process.env.NODE_ENV === "production") {
      this.expressApp.use(
        "/static",
        express.static(path.join(__dirname, "../../frontend/dist/static"))
      );

      // handle all get routing that isn't prefixed with '/api' using react
      this.expressApp.get(/^(?!\/api).*/, function (_req, res) {
        res.sendFile("index.html", {
          root: path.join(__dirname, "../../frontend/dist/"),
        });
      });
    }

    // send a json of all available endpoints
    this.expressApp.get("/api", (_, res) => {
      let payload = this.expressApp._router.stack
        .filter((r) => r && r.route)
        .map((r) => ({
          path: r.route.path,
          methods: Object.keys(r.route.methods),
        }));

      res.json(payload);
    });

    this.expressApp.post("/api/execute", (req, res) => {
      const { sql, params } = req.body;

      if (!sql) {
        res.status(400).json({ error: "missing sql" });
      } else {
        // `SELECT field FROM table WHERE id = :id`, [3], {}, () => {}

        let binds = params || {};

        getConnection().execute(sql, binds, (err, result) => {
          if (err) {
            console.error(err);
            res.status(500).send(err);
          } else {
            res.send(result);
          }
        });
      }
    });
  }

  start() {
    const PORT = process.env.PORT || 5000;

    this.expressApp.listen(PORT, () => {
      console.log(`Server listening at http://localhost:${PORT}`);
    });
  }
}

module.exports = Application;
