const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;

const Plan = new Schema({
    forkedFrom: Object,
    ownedBy: Schema.ObjectId,
    planName: String,
    createdAt: String,
    lastModifiedAt: String,
    currentState: Schema.ObjectId,
    numberOfNodes: Number,
    numberOfLines: Number,
    numberOfEdges: Number,
    numberOfLabels: Number,
    likeCount: Number,
    history: [Schema.ObjectId],
    deleted: Object,
});

module.exports = {
    Plan: mongoose.model('plan', Plan)
}
