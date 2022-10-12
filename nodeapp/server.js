// Loads the configuration from config.env to process.env

const express = require("express");
// const cors = require("cors");
// get MongoDB driver connection
const dbo = require("./db/conn");

const PORT = 3000;
const app = express();

const utils = require("./utils")

//app.use(cors());
app.use(express.json());


// Routes:
app.use(require("./routes/statsPublic"));
app.use(require("./routes/plansPublic"));
app.use(require("./routes/colorThemesPublic"));
app.use(require("./routes/usersPublic"));
app.use(require("./routes/_plans"));
app.use(require("./routes/_users"));

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
