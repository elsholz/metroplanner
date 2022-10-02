const coordinate_scalar = 20

let diff_x = 7
let diff_y = 10

let min_x = Infinity
let min_y = Infinity
let max_x = -Infinity
let max_y = -Infinity

let planData = {
    diffX: 7,
    diffY: 7,
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
                class: "label",
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

function renderAll(data) {
    let lines = data.lines
    let nodes = data.nodes

    planData._id = data._id
    planData.lines = data.lines
    planData.nodes = data.nodes
    planData.labels = data.labels
    planData.planName = data.planName
    planData.colorTheme = data.colorTheme


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

    planData.diffX = -min_x + planData.diffX
    planData.diffY = -min_y + planData.diffY
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



function renderSidePanel(panel) {
    // let tabcontent = document.getElementById("tabcontent")
    let containerNodesDiv = document.getElementById("tabContent")
    let res = ""
    if (panel == "stations") {
        for (let [key, value] of Object.entries(planData.nodes)) {
            console.log(key)
            res += panelItemStation(key, key, value.marker.sizeFactor, value.marker.rotation, value.location, value.marker.width, value.marker.height)
        }
    } else if (panel == "lines") {
        for (let line of planData.lines) {
            res += panelItemNode(line.color, line.symbol, line.name)
        }
    }

    containerNodesDiv.innerHTML = res
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

                                <input type="text" class="form-control" aria-label="Small"
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
                            <div class="col-md-6 bg-inherit ml0 ml-0" style="padding:0; ">
                                <div class="input-group input-group-sm" style="">
                                    <span class="input-group-prepend input-group-text bg-dark text-light" id="">x:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${location[0]}</span>
                                    <button class="input-group-append btn btn-outline-light" type="button">+</button>
                                        <!--<div class="input-group-btn">-->
                                </div>

                            </div>
                            <div class="col-md-6 bg-inherit ml0 ml-0" style="padding:0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">y:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${location[1]}</span>
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
                                    <span class="input-group-text bg-dark text-light" id="" style="">${width || 0}</span>
                                    <button class="btn btn-outline-light" type="button">+</button>
                                </div>
                            </div>
                            <div class="col-md-6 bg-inherit " style="padding: 0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Height:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${height || 0}</span>
                                    <button class="btn btn-outline-light" type="button">+</button>
                                </div>
                            </div>
                        </div>

                        <div class="row bg-inherit">
                            <div class="col-md-6 bg-inherit" style="padding: 0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Rotation:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${rotation || 0}°</span>
                                    <!--<input type="text" class="form-control" style="width: 10%">-->
                                    <button class="btn btn-outline-light" type="button">+</button>
                                </div>
                            </div>
                            <div class="col-md-6 bg-inherit" style="padding: 0">
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-light" id="">Size Factor:</span>
                                    <select class="custom-select bg-dark text-light rounded-right"
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

function panelItemNode(lineColor, lineSymbol, lineName) {
    return `
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
                        <!-- Location -->
                        <div class="row bg-inherit mb-2">
                            <div class="col-md-6 bg-inherit ml0 ml-0" style="padding:0; ">
                                <div class="input-group input-group-sm" style="">
                                    <span class="input-group-prepend input-group-text bg-dark text-light" id="">x:</span>
                                    <button class="btn btn-outline-light" type="button">-</button>
                                    <span class="input-group-text bg-dark text-light" id="">${0}</span>
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
