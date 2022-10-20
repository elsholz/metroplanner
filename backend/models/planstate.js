const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;

const Planstate = new Schema({
    createdAt: String,
    nodes: Object,
    lines: Object,
    additionalLabels: Object,
    numberOfNodes: Number,
    numberOfLines: Number,
});

module.exports = {
    Planstate: mongoose.model('plan_state', Planstate)
}
