const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;

const Stats = new Schema({
    _id: {
        plan: Schema.ObjectId,
        link: String,
    },
    views: Object,
});

module.exports = {
    Stats: mongoose.model('stat', Stats)
}
