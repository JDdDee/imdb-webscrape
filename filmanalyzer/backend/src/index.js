const Application = require("./application");

require("dotenv").config();

async function main() {
  const application = new Application();
  await application.init();
  application.start();
}

main();
