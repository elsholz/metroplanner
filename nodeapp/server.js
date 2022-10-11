// Loads the configuration from config.env to process.env

const express = require("express");
const cors = require("cors");
// get MongoDB driver connection
const dbo = require("./db/conn");

const PORT = 3000;
const app = express();

const utils = require("./utils")

app.use(cors());
app.use(express.json());

// Routes:
app.use(require("./routes/stats"));
app.use(require("./routes/plans"));
app.use(require("./routes/colorThemes"));

// perform a database connection when the server starts
dbo.connectToServer(function (err) {
  if (err) {
    console.error(err);
    process.exit();
  }

  // start the Express server
  app.listen(PORT, () => {
    console.log(`Server is running on port: ${PORT}`);
  });
});
