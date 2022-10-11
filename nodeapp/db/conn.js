require("dotenv").config({ path: "config.env" });

const { MongoClient } = require("mongodb");
const connectionString = `mongodb+srv://${process.env.MONGO_DB_USER}:${process.env.MONGO_DB_PW}@${process.env.MONGO_HOST}/test`
const client = new MongoClient(connectionString, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

let dbConnection;

module.exports = {
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
