const coordinate_scalar = 20

let diff_x = 7
let diff_y = 10

let min_x = Infinity
let min_y = Infinity
let max_x = -Infinity
let max_y = -Infinity

let planData = {
    baseDiffX: 7,
    baseDiffY: 7,
}

const labelTypes = {
    right_ascending: {
        style: {
            left: -33 + "px",
            top: -127 + "px",
            left: "-0px",
            top: "-20px",
            "white-space": "nowrap",
            transform: "rotate(-45deg)",
            "transform-origin": "middle left",
            width: "300px",
            width: "0px",
            height: "20px",
            height: "0px",
            "line-height": "20px",
            "vertical-align": "middle",
            "text-align": "left",
        },
    },
    right_descending: {
        style: {
            left: -32 + "px",
            top: 105 + "px",
            transform: "rotate(45deg)",
            width: "300px",
            height: "20px",
            "line-height": "20px",
            "vertical-align": "middle",
            "text-align": "left",
        },
    },
    left_ascending: {
        style: {
            left: -267 + "px",
            top: 107 + "px",
            transform: "rotate(-45deg)",
            width: "300px",
            height: "20px",
            "line-height": "20px",
            "vertical-align": "middle",
            "text-align": "right",
        },
    },
    left_descending: {
        style: {
            left: -267 + "px",
            top: -127 + "px",
            transform: "rotate(45deg)",
            width: "300px",
            height: "20px",
            "line-height": "20px",
            "vertical-align": "middle",
            "text-align": "right",
        },
    },
    right: {
        style: {
            left: 13 + "px",
            top: -13 + "px",
            transform: "",
            width: "300px",
            height: "20px",
            "line-height": "20px",
            "vertical-align": "middle",
            "text-align": "left",
        },
    },
    left: {
        style: {
            left: -313 + "px",
            top: -12 + "px",
            transform: "",
            width: "300px",
            height: "20px",
            "line-height": "20px",
            "vertical-align": "middle",
            "text-align": "right",
        },
    },
    centered: {
        style: {
            transform: "",
            width: "100%",
            height: "100%",
            "vertical-align": "middle",
            "text-align": "center",
        },
    },
}

function loadCSS(baseCSS) {
    let style = document.getElementById('style');
    style.innerHTML += baseCSS
    // document.getElementsByTagName('head')[0].appendChild(style);

    // document.getElementById('someElementId').className = 'cssClass';
    let shadow = coordinate_scalar / 4
    style.innerHTML += `
        .label{
            text-shadow: 0 0 ${shadow}px black, 0px 0px ${shadow}px black, 0px 0px ${shadow}px black;
        }

        .label.centered {
            text-shadow: none;
        }

        body {
            font-family: Oxygen-Sans, Arial, Helvetica, sans-serif;
            margin: 0px;
            background-color: #112;
            color: white;
            font-weight: bold;
            font-size: ${coordinate_scalar / 20 * 18}px;
        }

        .marker {
            border-style: solid;
            border-color: #eef;
            color: #000;
            background-color: #002;
            transform-origin: top left;
            box-shadow: 0px 0px ${coordinate_scalar / 20 * 3}px ${coordinate_scalar / 20}px #aaf;
            border-radius: ${coordinate_scalar / 2}px;
            border-width: ${coordinate_scalar / 10}px;
        }
    `
}

function addCSSLine(lineClass, backgroundColor, borderRadius, boxShadow, borderWidth, borderStyle, borderColor) {
    let style = document.getElementById('style');
    style.innerHTML += `
    .${lineClass} {
        background-color: ${backgroundColor};

        border-radius: ${borderRadius};  
        box-shadow: ${boxShadow};     
        border-width: ${borderWidth};   
        border-style: ${borderStyle};   
        border-color: ${borderColor};   
    }
    `
}

function getNodeData(key) {
    return planData.nodes[key]
}

function getConnectionPoint(anchor) {
    if (typeof anchor.node == "string") {
        let nodeId = anchor.node
        let conPX = anchor.xShift || 0
        let conPY = anchor.yShift || 0

        let node = planData.nodes[nodeId]
        let locX = node.location[0]
        let locY = node.location[1]
        let rotation = node.marker.rotation || 0
        let sizeFactor = node.marker.sizeFactor || 1

        locX += Math.sin(deg_to_rad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinate_scalar / 2
        locY -= Math.cos(deg_to_rad(90 - rotation)) * conPX * sizeFactor// * Math.SQRT2 * coordinate_scalar / 2

        if (conPY) {
            locX += Math.sin(deg_to_rad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinate_scalar / 2
            locY += Math.cos(deg_to_rad(rotation)) * conPY * sizeFactor// * Math.SQRT2 * coordinate_scalar / 2
        }

        return [locX, locY]
    }
    else {
        return anchor.node
    }
}
// // take a station name + optional selector and return coordinates of the point to connect to
// function get_connection_point(nodes, node_sel) {
//     if (typeof node_sel == "string") {
//         // named node without connection point (then, the location is used)
//         // console.log(node_sel)
//         let split_str = node_sel.split(",")
//         let node_name = split_str[0]
//         let con_p_x = split_str[1] || 0
//         let con_p_y = split_str[2] || 0
// 
//         let loc_x = nodes[node_name].location[0]
//         let loc_y = nodes[node_name].location[1]
//         let rotation = nodes[node_name].marker.rotation || 0
//         let width_factor = nodes[node_name].marker.sizeFactor || 1
// 
//         // get_y(location_y) - Math.sin(deg_to_rad(45 - rotation)) * Math.SQRT2 * coordinate_scalar / 2 + "px"
//         // get_x(location_x) - Math.cos(deg_to_rad(45 - rotation)) * Math.SQRT2 * coordinate_scalar / 2 + "px"
// 
//         loc_x += Math.sin(deg_to_rad(90 - rotation)) * con_p_x * width_factor// * Math.SQRT2 * coordinate_scalar / 2
//         loc_y -= Math.cos(deg_to_rad(90 - rotation)) * con_p_x * width_factor// * Math.SQRT2 * coordinate_scalar / 2
// 
//         if (con_p_y) {
//             loc_x += Math.sin(deg_to_rad(rotation)) * con_p_y * width_factor// * Math.SQRT2 * coordinate_scalar / 2
//             loc_y += Math.cos(deg_to_rad(rotation)) * con_p_y * width_factor// * Math.SQRT2 * coordinate_scalar / 2
//         }
// 
//         return [loc_x, loc_y]
//     }
//     else if (Array.isArray(node_sel) && typeof node_sel[0] == "number" && typeof node_sel[1] == "number") {
//         // unnamed node
//         return node_sel
//     }
//     else
//         throw Error(`Node ${node_sel} doesn't match pattern <String> or <Array[Number, Number]>`)
// }


function placeLine() {

}
function drawLines() {
    let lines = planData.lines
    let nodes = planData.nodes
    let div_for_lines = document.getElementById("lines")
    div_for_lines.innerHTML = ''
    // Draw lines

    for (const [key, value] of Object.entries(lines)) {
        // console.log(key, value)
        let stops = value.connections
        let lineClass = "line" + key
        let border_width = value.borderWidth || 0

        addCSSLine(
            lineClass,
            value.color,
            value.width * coordinate_scalar / 2 + "px",
            value.box_shadow || `0px 0px 5px 1px ${value.color}`,
            border_width * coordinate_scalar + "px",
            value.borderStyle || "solid",
            value.borderColor || value.color,
            // "transform-origin": "top left",
        )

        // check if stops' pattern matches either [a, b, c,…]. If so, convert to [[a, b, c, …]]
        // let wrap_stops = true

        // for (const [idx, s] of Object.entries(stops)) {
        //     if (!((Array.isArray(s) && typeof s[0] in { "number": null, "string": null } && typeof s[1] == "number" && s.length == 2) || typeof s == "string")) {
        //         wrap_stops = false
        //     }
        // }

        //if (wrap_stops)
        //    stops = [stops]

        // iterate through list of lists, consisting of nodes to be connected each
        for (const [index, connections] of Object.entries(stops)) {
            // iterate through the list of nodes that are to be connected
            for (let i = 0; i < connections.nodes.length - 1; i++) {
                let line_segment = document.createElement("div")

                let outbound_station = connections.nodes[i]
                let inbound_station = connections.nodes[i + 1]

                let from = getConnectionPoint(outbound_station)
                let to = getConnectionPoint(inbound_station)
                // console.log("Line Segment", from, to, "\n",outbound_station, inbound_station)

                let dx = to[0] - from[0]
                let dy = to[1] - from[1]

                let direction = (360 + 90 - (Math.atan2(dx, dy)) * (180 / Math.PI)) % 360
                let length = Math.sqrt(dx ** 2 + dy ** 2)


                let line_segment_data = {
                    tag: "div",
                    attributes: {
                        id: key + "_" + from + "_" + to,
                        style: {
                            left: get_left_shift(direction, value.width + 2 * border_width) + get_x(from[0]) + "px",
                            top: get_top_shift(direction, value.width + 2 * border_width) + get_y(from[1]) + "px",
                            transform: `rotate(${direction}deg)`,
                            width: value.width * coordinate_scalar + length * coordinate_scalar + "px",//((value.height * coordinate_scalar) || 16) + "px",
                            height: (value.width - 2 * border_width) * coordinate_scalar + "px",
                        },
                        class: "line_segment " + lineClass
                    },
                }
                patch(line_segment_data.attributes, value.attributes)

                set_attributes(line_segment, line_segment_data.attributes)
                div_for_lines.appendChild(line_segment)
            }
        }
    }
}

function placeMarker(key, value) {
    let node_type = value.type || "regularStop"

    // let label_spec = value.label.class || "right_ascending,0,0"
    // console.log(label_spec)
    // let label_type = label_spec.split(",")[0]
    // console.log(label_type)
    // let lx = (label_spec.split(",")[1]) || 0
    // let ly = (label_spec.split(",")[2]) || 0

    let node_types = {}

    /////// let node_type_wrapper_data = (node_types[node_type] || { wrapper: {} }).wrapper
    let node_type_marker_data = (node_types[node_type] || { marker: {} }).marker

    let border_width = 2;

    function get_station_top(location_y, rotation) {
        return get_y(location_y) - Math.sin(deg_to_rad(45 - rotation)) * Math.SQRT2 * coordinate_scalar / 2 + "px"
    }
    function get_station_left(location_x, rotation) {
        return get_x(location_x) - Math.cos(deg_to_rad(45 - rotation)) * Math.SQRT2 * coordinate_scalar / 2 + "px"
    }

    // global defaults
    // let wrapper_node_data = {
    //     tag: "div",
    //     attributes: {
    //         id: key,
    //         style: {
    //             "z-index": 5,
    //         },
    //         class: "wrapper",
    //     },
    // }

    let left = get_station_left(value.location[0], value.marker.rotation || 0)
    let top = get_station_top(value.location[1], value.marker.rotation || 0)


    let marker_node_data = {
        tag: 'div',
        attributes: {
            id: key,//+ "_marker",
            style: {
                left: left,
                top: top,
                "transform": `rotate(${(- value.marker.rotation || 0)}deg)`,
                width: (((value.marker.width || 1) - 1) * (value.marker.sizeFactor || 1) + 1) * coordinate_scalar - 2 * border_width + "px",
                height: (((value.marker.height || 1) - 1) * (value.marker.sizeFactor || 1) + 1) * coordinate_scalar - 2 * border_width + "px",
            },
            class: "marker",
        },
    }



    patch(marker_node_data.attributes, node_type_marker_data);
    patch(marker_node_data.attributes, (value.marker || {}));

    // let wrapper = document.createElement(wrapper_node_data.tag)
    let marker = document.createElement(marker_node_data.tag);
    set_attributes(marker, marker_node_data.attributes)

    // document.body.appendChild(wrapper)
    // wrapper.appendChild(marker)
    // wrapper.appendChild(label)


    document.getElementById("nodes").appendChild(marker)
}
function drawMarkers() {
    document.getElementById("nodes").innerHTML = ""
    for (const [key, value] of Object.entries(planData.nodes)) {
        // console.log(key, value)
        placeMarker(key, value)
    }
}

function placeLabel(lbl) {
    // console.log(lbl)
    let labelClass = lbl.class
    let labelText = lbl.text
    let labelAnchor = lbl.anchor

    if (typeof labelAnchor.node === "string") {
        let forNode = labelAnchor.node
        let xShift = labelAnchor.xShift || 0
        let yShift = labelAnchor.yShift || 0

        let locX = planData.nodes[forNode].location[0] + xShift
        let locY = planData.nodes[forNode].location[1] + yShift

        // console.log(locX, locY, labelClass)




        // let node_type_label_data = (node_types[node_type] || { label: labelTypes }).label[(label_type || "right_ascending")] || {}

        let labelClassData = labelTypes[labelClass]
        let labelNodeData = {
            tag: "div",
            attributes: {
                id: forNode + "_label",
                style: {
                    left: 0 + "px",
                    top: 0 + "px",
                    transform: "rotate(-45deg)",
                    width: "0px",
                    height: "0px",
                    "text-align": "left",
                },
                class: "label " + labelClass,
            },
            innerHTML: (labelText || "")
        }

        patch(labelNodeData.attributes, labelClassData);
        // patch(labelNodeData.attributes, (lbl || {}));

        let label_point = getConnectionPoint(labelAnchor)
        let label_orig_left = parseFloat(labelNodeData.attributes.style.left.slice(0, -2))
        let label_orig_top = parseFloat(labelNodeData.attributes.style.top.slice(0, -2))

        if (labelClass === "centered") {
            console.log("Centered!")
            console.log(lbl)
            value = getNodeData(lbl.anchor.node)

            labelNodeData.attributes.style.width = (value.marker.width * coordinate_scalar) + "px"
            labelNodeData.attributes.style.height = (value.height * coordinate_scalar) + "px"
            labelNodeData.attributes.style.lineHeight = (value.marker.height * coordinate_scalar / 4) + "px"
            labelNodeData.attributes.style.fontSize = (value.marker.height * 3) + "px"
            labelNodeData.attributes.style.textAlign = "center"

            labelNodeData.attributes.style.left = get_x(value.location[0]) - coordinate_scalar / 2 + "px"
            labelNodeData.attributes.style.top = get_y(value.location[1]) - coordinate_scalar / 2 + "px"

            console.log(labelNodeData)
            //// labelNodeData.attributes.style.left = left
            //// labelNodeData.attributes.style.top = top
        }
        else {
            labelNodeData.attributes.style.left = label_orig_left + get_x(label_point[0]) + "px"
            labelNodeData.attributes.style.top = label_orig_top + get_y(label_point[1]) + "px"
        }

        let label = document.createElement(labelNodeData.tag);

        set_attributes(label, labelNodeData.attributes)

        label.innerHTML = labelNodeData.innerHTML
        document.getElementById("labels").appendChild(label)

    }
    else {
        console.log("Label is not for station.", labelAnchor)
    }
}
function drawLabels() {
    document.getElementById("labels").innerHTML = ""
    for (let lbl of planData.labels) {
        placeLabel(lbl)
    }
}

function toggleLayer(layerName) {
    let layer = document.getElementById(layerName)
    if (layer.classList.contains("halftransparent")) {
        layer.classList.toggle("halftransparent")
        layer.classList.toggle("hidden")
    } else if (layer.classList.contains("hidden")) {
        layer.classList.toggle("hidden")
    } else {
        layer.classList.toggle("halftransparent")
    }
}

function patch(object, data) {
    for (let prop in data) {
        let val = data[prop]
        if (typeof val == "object")
            patch(object[prop], val)
        else
            object[prop] = val
    }
    return object
}
function set_attributes(html_element, attributes) {
    for (let a in attributes) {
        if (a === "style") {
            Object.assign(html_element.style, attributes.style);
        } else {
            html_element.setAttribute(a, attributes[a]);
        }
    }
}
function get_x(x) {
    return (planData.diffX + x) * coordinate_scalar
}
function get_y(y) {
    return (planData.diffY + y) * coordinate_scalar
}
function deg_to_rad(x) {
    return x / (180 / Math.PI)
}
function get_top_shift(direction, width) {
    return -Math.sin(deg_to_rad(45 + direction)) * Math.SQRT2 * width * coordinate_scalar / 2
}
function get_left_shift(direction, width) {
    return -Math.cos(deg_to_rad(45 + direction)) * Math.SQRT2 * width * coordinate_scalar / 2
}

function setData(data) {
    planData._id = data._id
    planData.lines = data.lines
    planData.nodes = data.nodes
    planData.labels = data.labels
    planData.planName = data.planName
    planData.colorTheme = data.colorTheme
}

function renderAll() {
    let lines = planData.lines
    let nodes = planData.nodes

    // optional extra: collect their borders (like min/max of stations and labels)
    for (const [key, value] of Object.entries(nodes)) {
        // console.log(key)
        let loc = value.location
        if (loc[0] < min_x) {
            min_x = loc[0]
        }
        if (loc[0] > max_x) {
            max_x = loc[0]
        }
        if (loc[1] < min_y) {
            min_y = loc[1]
        }
        if (loc[1] > max_y) {
            max_y = loc[1]
        }
    }
    // TODO: Fix, as this only iterates though first level of array
    for (const [key, value] of Object.entries(lines)) {
        let stops = value.connections
        stops.forEach(element => {
            if (typeof element !== "string") {
                let loc = element
                if (loc[0] < min_x) {
                    min_x = loc[0]
                }
                if (loc[0] > max_x) {
                    max_x = loc[0]
                }
                if (loc[1] < min_y) {
                    min_y = loc[1]
                }
                if (loc[1] > max_y) {
                    max_y = loc[1]
                }
            }
        });
    }

    // console.log(min_x, min_y, max_x, max_y)

    planData.diffX = -min_x + planData.baseDiffX
    planData.diffY = -min_y + planData.baseDiffY
    // console.log("plan data:", planData)

    drawLines()
    drawMarkers()
    drawLabels()



    ///////////for (const [key, value] of Object.entries(nodes)) {
    // let default_data = node_types.default
    // let wrapper_data = default_data.wrapper 
    // let marker_data = default_data.marker
    // let label_data = default_data.label



    /***** 
    function add_events() {
        document.getElementById(marker.id).onmousedown = handle_click

        function handle_click(e) {
            start_dragging(e)
        }

        function start_dragging(e) {
            e = e || window.event;
            e.preventDefault();
            document.onmouseup = stop_dragging;
            document.onmousemove = follow_cursor;
        }

        function follow_cursor(e) {
            e = e || window.event;
            e.preventDefault();
            marker.style.left = get_station_left(Math.round(e.pageX / coordinate_scalar) - diff_x, (value.marker.rotation || 0))
            marker.style.top = get_station_top(Math.round(e.pageY / coordinate_scalar) - diff_y, (value.marker.rotation || 0))

            label.style.left = /*parseFloat(label_node_data.attributes.style.left.slice(0, -2)) + */ /****** label_orig_left + get_x(label_point[0]) + "px"
label.style.top = /*parseFloat(label_node_data.attributes.style.top.slice(0, -2)) +*/ /*********label_orig_top + get_y(label_point[1]) + "px"
                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                            function stop_dragging() {
                                                                                                                                                                                                                                                document.onmouseup = null;
                                                                                                                                                                                                                                                document.onmousemove = null;
                                                                                                                                                                                                                                                nodes[marker.id].location = [
                                                                                                                                                                                                                                                    Math.round(- diff_x + (marker.style.left.slice(0, -2)) / coordinate_scalar + marker.style.width.slice(0, -2) / 2 / coordinate_scalar),
                                                                                                                                                                                                                                                    Math.round(- diff_y + (marker.style.top.slice(0, -2)) / coordinate_scalar + marker.style.height.slice(0, -2) / 2 / coordinate_scalar),
                                                                                                                                                                                                                                                ]
                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                        add_events() ******/


    //////// }
    // function add_line() {
    //     let ln = document.getElementById("linename").value
    //     // console.log(ln)
    //     lines[ln] = selected_items
    // }
    console.log("blabliblub")
    let url = "/style.css"
    fetch(url)
        .then(response => response.text())
        .then(out => {
            loadCSS(out)
        })
        .catch(err => { console.log("Error::", err) });
}


let stationFilter = ''
let lineFilter = ''

function applyStationFilter() {
    stationFilter = document.getElementById("inputStationFilter").value.toLowerCase()
    renderSidePanel("stations")
}
function applyLineFilter() {
    lineFilter = document.getElementById("inputLineFilter").value.toLowerCase()
    renderSidePanel("lines")
}

function createNode() {
    planData.nodes[stationFilter] = {
        location: [0, 0],
        marker: {
            width: 1,
            height: 1,
            sizeFactor: 1,
            rotation: 0
        }
    }
    planData.labels.push({
        class: "right",
        text: stationFilter,
        anchor: {
            node: stationFilter
        }
    })
    renderSidePanel("stations")
}

function createLine() {
    planData.lines.push({
        symbol: lineFilter,
        name: lineFilter,
        connections: [],
        color: "white",
        width: 0.5,
    })
    renderSidePanel("lines")
}

function renderSidePanel(panel) {
    // let tabcontent = document.getElementById("tabcontent")
    let containerNodesDiv = document.getElementById("tabContent")
    planData.nodeNameByID = getMappingNodeName()
    let res = ""
    if (panel == "stations") {
        res += `
                                        <div class="input-group input-group-sm">
                                            <span class="input-group-text bg-dark text-light" id="">Filter:</span>
                                            <input id="inputStationFilter" type="text" class="form-control bg-dark text-light" aria-label="Small" onchange="applyStationFilter()"
                                                aria-describedby="inputGroup-sizing-sm"  value="${stationFilter}">
                                                <button class="btn btn-success btn-outline-light btn-sm" type="button" onclick="createNode()"><strong>+ Add Station</strong></button>
                                        </div>
        `

        for (let [key, value] of Object.entries(planData.nodes)) {
            if (key.toLowerCase().includes(stationFilter) || planData.nodeNameByID[key].toLowerCase().includes(stationFilter)) {
                res += panelItemStation(key, planData.nodeNameByID[key], value.marker.sizeFactor, value.marker.rotation, value.location, value.marker.width, value.marker.height,)
            }
        }
    } else if (panel == "lines") {
        res += `
                                        <div class="input-group input-group-sm">
                                            <span class="input-group-text bg-dark text-light" id="">Filter:</span>
                                            <input id="inputLineFilter" type="text" class="form-control bg-dark text-light" aria-label="Small" onchange="applyLineFilter()"
                                                aria-describedby="inputGroup-sizing-sm"  value="${lineFilter}">
                                                <button class="btn btn-success btn-outline-light btn-sm" type="button" onclick="createLine()"><strong>+ Add Line</strong></button>
                                        </div>
        `
        for (let line of planData.lines) {
            if (line.symbol.toLowerCase().includes(lineFilter) || line.name.toLowerCase().includes(lineFilter)) {
                res += panelItemLine(line.color, line.symbol, line.name, line.width, line.connections)
            }
        }
    }

    containerNodesDiv.innerHTML = res
}

function downloadData() {
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
        _id: planData._id,
        planName: planData.planName,
        nodes: planData.nodes,
        lines: planData.lines,
        labels: planData.labels,
        colorTheme: planData.colorTheme,
        savedAt: new Date().toISOString(),
    }));
    var dlAnchorElem = document.getElementById('downloadAnchorElem');
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", planData._id + "_metroplanner_data.json");
    dlAnchorElem.click();
}

function redrawEverything() {
    drawLines()
    drawLabels()
    drawMarkers()
}

function incNode(inp, node, idx) {
    let d = document.getElementById(inp)
    d.value++
    applyNodeLocation(node)
}

function decNode(inp, node, idx) {
    let d = document.getElementById(inp)
    d.value--
    applyNodeLocation(node)
}
function applyNodeLocation(nodeid) {
    let d = document.getElementById("inputX" + nodeid)
    planData.nodes[nodeid].location[0] = Number.parseFloat(d.value)
    d = document.getElementById("inputY" + nodeid)
    planData.nodes[nodeid].location[1] = Number.parseFloat(d.value)
    redrawEverything()
}

function incNodeWidth(nodeID) {
    let el = document.getElementById("inputNodeWidth" + nodeID)
    el.value = Number.parseFloat(el.value) + 1
    applyNodeWidth(nodeID)
}
function decNodeWidth(nodeID) {
    let el = document.getElementById("inputNodeWidth" + nodeID)
    el.value = Number.parseFloat(el.value) - 1
    applyNodeWidth(nodeID)
}
function incNodeHeight(nodeID) {
    let el = document.getElementById("inputNodeHeight" + nodeID)
    el.value = Number.parseFloat(el.value) + 1
    applyNodeHeight(nodeID)
}
function decNodeHeight(nodeID) {
    let el = document.getElementById("inputNodeHeight" + nodeID)
    el.value = Number.parseFloat(el.value) - 1
    applyNodeHeight(nodeID)
}
function applyNodeHeight(nodeID) {
    let el = document.getElementById("inputNodeHeight" + nodeID)
    planData.nodes[nodeID].marker.height = Number.parseFloat(el.value)
    drawMarkers()
}
function applyNodeWidth(nodeID) {
    let el = document.getElementById("inputNodeWidth" + nodeID)
    planData.nodes[nodeID].marker.width = Number.parseFloat(el.value)
    drawMarkers()
}

function incNodeRotation(nodeID) {
    let el = document.getElementById("inputNodeRotation" + nodeID)
    el.value = Number.parseFloat(el.value) + 45
    applyNodeRotation(nodeID)
}
function decNodeRotation(nodeID) {
    let el = document.getElementById("inputNodeRotation" + nodeID)
    el.value = Number.parseFloat(el.value) - 45
    applyNodeRotation(nodeID)
}
function applyNodeRotation(nodeID) {
    let el = document.getElementById("inputNodeRotation" + nodeID)
    planData.nodes[nodeID].marker.rotation = Number.parseFloat(el.value)
    redrawEverything()
}
function applySizeFactor(nodeID) {
    let el = document.getElementById("selectSizeFactor" + nodeID)
    planData.nodes[nodeID].marker.sizeFactor = Number.parseFloat(el.value)
    redrawEverything()
}

function changeNodeID(oldNodeID) {
    alert("Not implemented")
    // renderSidePanel("stations")
}

function changeNodeName(nodeID) {
    let el = document.getElementById("inputStationName" + nodeID)
    let newName = el.value
    changeLabel(nodeID, newName)
    drawLabels()
}

function getMappingNodeName() {
    res = {}
    for (let item of planData.labels) {
        res[item.anchor.node] = item.text
    }
    return res
}

function changeLabel(nodeID, newLabelText) {
    for (let item of planData.labels) {
        if (item.anchor.node === nodeID) {
            console.log("Item found!", item)
            item.text = newLabelText
            break
        }
    }
    planData.nodeNameByID = getMappingNodeName()
}

// Templates
function panelItemStation(stationID, stationName, sizeFactor, rotation, location, width, height) {
    return `
            <div class="card ">
                <div class="card-header bg-dark" id="headingOne">
                    <div class="row">
                        <div class="col col-md-2">
                            <button class="btn btn-dark collapsed" data-toggle="collapse" data-target="#collapse_${stationID}"
                                aria-expanded="false" aria-controls="collapseOne">
                                ≡
                            </button>
                        </div>
                        <div class="col-md-10">
                            <div class="input-group input-group-md mb-0">
                                <input type="text" class="form-control mono" aria-label="Small"
                                    style="background-color: #222; margin-left:10px; color: #ccc; text-align: center; border-radius: 15px; border-color: #777;"
                                    aria-describedby="inputGroup-sizing-sm" value="${stationID}">

                                <input id="inputStationName${stationID}" type="text" class="form-control" aria-label="Small" onchange="changeNodeName('${stationID}')"
                                    style="margin-left: 5px; width: 40%; background-color: #222; color:white; border-radius: 15px; text-align: center; border-color: #777;"
                                    aria-describedby="inputGroup-sizing-sm" value="${stationName}">
                            </div>
                        </div>
                    </div>
                </div>
                <hr style="margin: 0">
                <div id="collapse_${stationID}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
                    <div class="card-body">
                        <!-- Location -->
                        <div class="row bg-inherit mb-2">
                            <div class="col-md-6 bg-inherit ml0 ml-0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-prepend input-group-text bg-dark text-light" id="">x:</span>
                                    <button class="btn btn-outline-light" type="button" onclick="decNode('inputX${stationID}', '${stationID}', 0)">-</button>
                                    <input id="inputX${stationID}" type="text" class="form-control bg-dark text-light" aria-label="Small"
                                        aria-describedby="inputGroup-sizing-sm" onchange="applyNodeLocation('${stationID}')" value="${location[0]}">
                                    <button class="input-group-append btn btn-outline-light" type="button" onclick="incNode('inputX${stationID}', '${stationID}', 0)">+</button>
                                </div>
                            </div>
                            <div class="col-md-6 bg-inherit ml0 ml-0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">y:</span>
                                    <button class="btn btn-outline-light" type="button" onclick="decNode('inputY${stationID}', '${stationID}', 1)">-</button>
                                    <input id="inputY${stationID}" type="text" onchange="applyNodeLocation('${stationID}')" class="form-control bg-dark text-light" aria-label="Small"
                                        aria-describedby="inputGroup-sizing-sm" value="${location[1]}">
                                    <button class="btn btn-outline-light" type="button" onclick="incNode('inputY${stationID}', '${stationID}', 1)">+</button>
                                </div>
                            </div>
                        </div>

                        <!-- Dimensions -->
                        <div class="row bg-inherit mb-2">
                            <div class="col-md-6 bg-inherit">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Width:</span>
                                    <button class="btn btn-outline-light" type="button" onclick="decNodeWidth('${stationID}')">-</button>
                                    <input id="inputNodeWidth${stationID}" type="text" class="form-control bg-dark text-light" aria-label="Small" onchange="applyNodeWidth('${stationID}')"
                                        aria-describedby="inputGroup-sizing-sm" value="${width || 0}">
                                    <button class="btn btn-outline-light" onclick="incNodeWidth('${stationID}')" type="button">+</button>
                                </div>
                            </div>
                            <div class="col-md-6 bg-inherit">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Height:</span>
                                    <button class="btn btn-outline-light" type="button" onclick="decNodeHeight('${stationID}')">-</button>
                                    <input id="inputNodeHeight${stationID}" type="text" class="form-control bg-dark text-light" aria-label="Small" onchange="applyNodeHeight('${stationID}')"
                                        aria-describedby="inputGroup-sizing-sm" value="${height || 0}">
                                    <button class="btn btn-outline-light" onclick="incNodeHeight('${stationID}')" type="button">+</button>
                                </div>
                            </div>
                        </div>

                        <div class="row bg-inherit">
                            <div class="col-md-7 bg-inherit">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Rotation:</span>
                                    <button class="btn btn-outline-light" onclick="decNodeRotation('${stationID}')" type="button">-</button>
                                    <input id="inputNodeRotation${stationID}" type="text" class="form-control bg-dark text-light" aria-label="Small" onchange="applyNodeRotation('${stationID}')"
                                        aria-describedby="inputGroup-sizing-sm" value="${rotation || 0}">
                                    <button class="btn btn-outline-light" onclick="incNodeRotation('${stationID}')" type="button">+</button>
                                </div>
                            </div>
                            <div class="col-md-5 bg-inherit">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Scale:</span>
                                    <select id="selectSizeFactor${stationID}" class="custom-select bg-dark text-light rounded-right" onchange="applySizeFactor('${stationID}')"
                                        id="inputGroupSelect02" value="${sizeFactor || 1}">
                                        <option selected>1</option>
                                        <option value="2">√2</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`
}

function addStation(lineID, conIdx, element) {
    let container = element.parentNode.parentNode.parentNode
    let children = Array.from(container.children)

    console.log("container:", container)
    console.log("children:", children)

    for (let item of planData.lines) {
        if (item.symbol === lineID) {
            let stops = item.connections[conIdx].nodes
            let obj = {
                node: "",
                xShift: 0,
                yShift: 0
            }

            let index = children.indexOf(element)

            let p = new DOMParser()
            let newElement = p.parseFromString(stopNodeHTML(obj, lineID, conIdx), "text/html").firstChild.childNodes[1].childNodes[0]
            console.log("new Element:", newElement)

            if (index >= stops.length) {
                stops.push(obj)
                container.appendChild(newElement)
            }
            else {
                stops.splice(index, 0, obj);
                container.insertBefore(newElement, element.parentNode.parentNode)
            }
        }
    }
    // renderSidePanel("lines")
    drawLines()
}

function addConnections(lineID) {
    for (let item of planData.lines) {
        if (item.symbol === lineID) {
            item.connections.push({
                nodes: []
            })
        }
    }
    renderSidePanel("lines")
}

function panelSubItemStops(cons, idx, lineID) {
    let res = ''

    for (let [index, stop] of cons.nodes.entries()) {
        // console.log(stop)
        res += stopNodeHTML(stop, lineID, idx)
    }

    res += `
                                <div class="row bg-inherit mt-2 mb-2">
                                    <div class="col-md-12 bg-inherit">
                                        <button class="btn btn-success btn-outline-light btn-sm" type="button" onclick="addStation('${lineID}', ${idx}, this)"><strong>+ Add Station</strong></button>
                                    </div>
                                </div>
                                `

    return res
}

function removeStop(lineID, idx, stop) {
    for (let item of planData.lines) {
        if (item.symbol === lineID) {
            let stops = item.connections[idx].nodes
            let itemIndex = Array.from(stop.parentNode.parentNode.parentNode.children).indexOf(stop.parentNode.parentNode)

            stops.splice(itemIndex, 1)
            stop.parentNode.parentNode.parentNode.removeChild(stop.parentNode.parentNode)
        }
    }

    console.log("Drawing lines")
    drawLines()
}

function stopNodeHTML(stop, lineID, idx) {
    return `
                                <div class="row bg-inherit mb-3 mt-3" style="">
                                    <div class="col-md-6 bg-inherit">
                                        <div class="input-group input-group-sm" style="">
                                            <span class="input-group-prepend input-group-text bg-dark text-light" id="">Node:</span>
                                            <input id="anchorNodeInput" class="form-control bg-dark text-light custom-select" aria-label="Small"
                                                aria-describedby="inputGroup-sizing-sm" list="nodesDataList" value="${stop.node}">
                                        </div>
                                    </div>
                                    <div class="col-md-6 bg-inherit">
                                            <button class="btn btn-sm btn-outline-light" type="button">v</button>
                                            <button class="btn btn-sm btn-outline-light" type="button">^</button>
                                            <button class="btn btn-sm btn-outline-light bg-success" onclick="addStation('${lineID}', ${idx}, this)" type="button">+</button>
                                            <button class="btn btn-sm btn-outline-light bg-danger" onclick="removeStop('${lineID}', ${idx}, this)" type="button">x</button>
                                    </div>
                                    <div class="col-md-6 bg-inherit">
                                        <div class="input-group input-group-sm">
                                            <span class="input-group-text bg-dark text-light" id="">x:</span>
                                            <button class="btn btn-outline-light" type="button">-</button>
                                            <input type="text" class="form-control bg-dark text-light" aria-label="Small"
                                                aria-describedby="inputGroup-sizing-sm" value="${stop.xShift || 0}">
                                            <button class="btn btn-outline-light" type="button">+</button>
                                        </div>
                                    </div>
                                    <div class="col-md-6 bg-inherit">
                                        <div class="input-group input-group-sm">
                                            <span class="input-group-text bg-dark text-light" id="">y:</span>
                                            <button class="btn btn-outline-light" type="button">-</button>
                                            <input type="text" class="form-control bg-dark text-light" aria-label="Small"
                                                aria-describedby="inputGroup-sizing-sm" value="${stop.yShift || 0}">
                                            <button class="btn btn-outline-light" type="button">+</button>
                                        </div>
                                    </div>
                                </div>
    `
}

function panelItemLine(lineColor, lineSymbol, lineName, lineWidth, lineConnections) {
    let stopDivs = ''
    let options = ''
    for (let [k, v] of Object.entries(planData.nodes)) {
        options += `
                                                <option value="${k}">${k}</option>
        `
    }
    for (const [idx, item] of lineConnections.entries()) {
        stopDivs += `
                                <div class="row bg-inherit mb-2" style="border: 2px solid #00f6">
                                    <div class="col-md-12 bg-inherit ml0 ml-0">
                                        ${panelSubItemStops(item, idx, lineSymbol)}
                                    </div>
                                </div>
    `}
    stopDivs += `
                                <div class="row bg-inherit mb-2">
                                    <div class="col-md-12 bg-inherit ml0 ml-0">
                                        <button class="btn btn-success btn-outline-light " type="button" onclick="addConnections('${lineSymbol}')"><strong>Add more connected Nodes to this line</strong></button>
                                    </div>
                                </div>
                                `
    return `
            <datalist id="nodesDataList">
                ${options}
            </datalist>
            <div class="card ">
                <div class="card-header " id="headingOne" style=" background-color: ${lineColor}">
                    <div class="row">
                        <div class="col col-md-2">
                            <button class="btn btn-dark collapsed" data-toggle="collapse" data-target="#collapse_${lineSymbol}"
                                aria-expanded="false" aria-controls="collapseOne" >
                                ≡
                            </button>
                        </div>
                        <div class="col-md-10">
                            <div class="input-group input-group-md mb-0">
                                <input type="text" class="form-control mono" aria-label="Small"
                                    style="background-color: #222; margin-left:10px; color: #ccc; text-align: center; border-radius: 15px; border-color: #777;"
                                    aria-describedby="inputGroup-sizing-sm" value="${lineSymbol}">

                                <input type="text" class="form-control" aria-label="Small"
                                    style="margin-left: 5px; width: 40%; background-color: #222; color:white; border-radius: 15px; text-align: center; border-color: #777;"
                                    aria-describedby="inputGroup-sizing-sm" value="${lineName}">
                            </div>
                        </div>
                    </div>
                </div>
                <hr style="margin: 0">
                <div id="collapse_${lineSymbol}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
                    <div class="card-body">
                        Settings:
                        <!-- Basics -->
                        <div class="row bg-inherit mt-2 mb-2">
                            <div class="col-md-8 bg-inherit ml0 ml-0">
                                <div class="input-group input-group-sm" style="">
                                    <span class="input-group-prepend input-group-text bg-dark text-light" id="">Color:</span>
                                    <input id="lineColorTextInput" class="form-control bg-dark text-light custom-select" aria-label="Small"
                                        aria-describedby="inputGroup-sizing-sm" list="colorDataList" value="${lineColor}">
                                    <datalist id="colorDataList">
                                        <option value="hsl(0, 100%, 50%)">Line Color 1</option>
                                        <option value="hsl(40, 100%, 50%)">Line Color 2</option>
                                        <option value="hsl(80, 100%, 50%)">Line Color 3</option>
                                        <option value="hsl(120, 100%, 50%)">Line Color 4</option>
                                        <option value="hsl(160, 100%, 50%)">Line Color 5</option>
                                        <option value="hsl(200, 100%, 50%)">Line Color 6</option>
                                        <option value="hsl(240, 100%, 50%)">Line Color 7</option>
                                        <option value="hsl(280, 100%, 50%)">Line Color 8</option>
                                        <option value="hsl(320, 100%, 50%)">Line Color 9</option>

                                        <option value="white">White</option>
                                        <option value="black">Black</option>

                                        <option value="hsl(207.2, 89.8%, 23.1%)">Water</option>
                                    </datalist>
                                </div>
                            </div>
                            <div class="col-md-4 bg-inherit ml0 ml-0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Width:</span>
                                    <input type="text" class="form-control bg-dark text-light" aria-label="Small"
                                        aria-describedby="inputGroup-sizing-sm" value="${lineWidth}">
                                </div>
                            </div>
                        </div>

                        <hr>

                        Connections:
                        <!-- Connections-->
                        <div class="row bg-inherit mb-2">
                            <div class="col-md-12 bg-inherit">
                                ${stopDivs}
                            </div>
                        </div>


                        <!-- Location -->
                        <div class="row bg-inherit mb-2">
                            <div class="col-md-6 bg-inherit ml0 ml-0" style="padding:0; ">
                                <div class="input-group input-group-sm" style="">
                                    <span class="input-group-prepend input-group-text bg-dark text-light" id="">x:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <input type="text" class="form-control bg-dark text-light" aria-label="Small"
                                        aria-describedby="inputGroup-sizing-sm" value="${0}">
                                    <button class="input-group-append btn btn-outline-light" type="button">+</button>
                                        <!--<div class="input-group-btn">-->
                                </div>

                            </div>
                            <div class="col-md-6 bg-inherit ml0 ml-0" style="padding:0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">y:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${1}</span>
                                    <button class="btn btn-outline-light" type="button">+</button>
                                </div>
                            </div>
                        </div>

                        <!-- Dimensions -->
                        <div class="row bg-inherit mb-2">
                            <div class="col-md-6 bg-inherit " style="padding: 0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Width:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="" style="">${0}</span>
                                    <button class="btn btn-outline-light" type="button">+</button>
                                </div>
                            </div>
                            <div class="col-md-6 bg-inherit " style="padding: 0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Height:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${0}</span>
                                    <button class="btn btn-outline-light" type="button">+</button>
                                </div>
                            </div>
                        </div>

                        <div class="row bg-inherit">
                            <div class="col-md-6 bg-inherit" style="padding: 0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Rotation:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${0}°</span>
                                    <!--<input type="text" class="form-control" style="width: 10%">-->
                                    <button class="btn btn-outline-light" type="button">+</button>
                                </div>
                            </div>
                            <div class="col-md-6 bg-inherit" style="padding: 0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Size Factor:</span>
                                    <select class="custom-select bg-dark text-light rounded-right"
                                        id="inputGroupSelect02" value="${1}">
                                        <option selected>1</option>
                                        <option value="2">√2</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`
}

let expandedLines = []
let expandedStations = []
