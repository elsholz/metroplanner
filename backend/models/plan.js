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
    currentNumberOfNodes: Number,
    currentNumberOfLines: Number,
    currentNumberOfEdges: Number,
    currentNumberOfLabels: Number,
    currentColorTheme: Schema.ObjectId,
    likeCount: Number,
    history: [Schema.ObjectId],
    deleted: Object,
});

module.exports = {
    Plan: mongoose.model('plan', Plan)
}
