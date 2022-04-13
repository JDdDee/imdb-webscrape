const oracledb = require("oracledb");

// default is oracledb.outFormat = oracledb.ARRAY;
oracledb.outFormat = oracledb.OBJECT;

let connection;

async function initConnection() {
  connection = await oracledb.getConnection({
    user: process.env.ORACLEDB_USER || "hr",

    password: process.env.ORACLEDB_PASSWORD,

    connectString:
      process.env.ORACLEDB_CONNECTIONSTRING || "localhost/orclpdb1",

    externalAuth: process.env.ORACLEDB_EXTERNALAUTH ? true : false,
  });
}

function getConnection() {
  return connection;
}

module.exports = {
  connection,
  initConnection,
  getConnection,
};
