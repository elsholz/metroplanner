const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;

const Plan = new Schema({
    forkedFrom: Schema.ObjectId,
    ownedBy: Schema.ObjectId,
    planName: String,
    colorTheme: Schema.ObjectId,
    createdAt: String,
    lastModified: String,
    currentState: Schema.ObjectId,
    history: [Schema.ObjectId],
});

module.exports = {
    Plan: mongoose.model('plan', Plan)
}
