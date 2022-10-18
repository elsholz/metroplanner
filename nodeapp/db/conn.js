require("dotenv").config({ path: "config.env" });

const { MongoClient } = require("mongodb");
const connectionString = `mongodb+srv://${process.env.MONGO_DB_USER}:${process.env.MONGO_DB_PW}@${process.env.MONGO_HOST}/test`
const client = new MongoClient(connectionString, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

let dbConnection;



// Import the mongoose module
const mongoose = require("mongoose");

// Set up default mongoose connection
mongoose.connect(connectionString, { useNewUrlParser: true, useUnifiedTopology: true });

// Get the default connection
const db = mongoose.connection;

// Bind connection to error event (to get notification of connection errors)
db.on("error", console.error.bind(console, "MongoDB connection error:"));


module.exports = {
  db: db,
  connectToServer: function (callback) {
    // Implement Database connection
    client.connect(function (err, db) {
      if (err || !db) {
        return callback(err);
      }

      dbConnection = db.db("metroplanner");
      console.log(`Successfully connected to MongoDB with user ${process.env.MONGO_DB_USER}.`);

      return callback();
    });
  },

  getDb: function () {
    return dbConnection;
  },
};

