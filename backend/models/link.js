const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;

const Link = new Schema({
    _id: String,
    plan: Schema.ObjectId,
    active: Boolean,
});

module.exports = {
    Link: mongoose.model('link', Link)
}
