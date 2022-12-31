const mongoose = require("mongoose");

const Schema = mongoose.Schema

const PlanState = new Schema({
    createdAt: String,
    nodes: Object,
    lines: Object,
    labels: Object,
})

module.exports = {
    PlanState: mongoose.model('plan_state', PlanState)
}
