let color_themes = {
    dark: {
        line_colors: [
            "#C724B1",
            "#4D4DFF",
            "#E0E722",
            "#FFAD00",
            "#D22730",
            "#db3eb1",
            "#44D62C",
        ],
        river: "#8585ff",
        deep_river: "#064070",
        city_border: "#777",
    },
    bright: {
        line_colors: [
            "#cc21ff",
            "#32b6e0",
            "#19ef8d",
            "#e2eb9c",
            "#e4773b",
            "#f70e4c",
            "#0a908c",
            "#3265ff",
            "#8585ff",
        ],
        river: "#92b6ff",
        deep_river: "#064070",
        city_border: "#777",
    }
}

let current_color_theme = color_themes.dark

let octo_shift_x = -3
let octo_shift_y = 0

let octo2_shift_x = 10
let octo2_shift_y = 0

let nodes = {
    test_width_4: {
        name: "",
        width: 4,
        height: 4,
        location: [
            23, 1
        ]
    },
    test_width_3_height_2_rot: {
        name: "",
        width: 3,
        height: 2,
        rotation: 45,
        factor: Math.SQRT2,
        location: [
            0, 15
        ]
    },
    test_width_3_height_2: {
        name: "",
        width: 3,
        height: 2,
        location: [
            -10, 15
        ]
    },

    test_2_1: {
        name: "A",
        width: 2,
        rotation: 90,
        label_type:"right_ascending.1",
        location: [
            octo2_shift_x, octo2_shift_y - 4
        ]
    },
    test_2_2: {
        name: "2",
        width: 2,
        rotation: 135,
        label_type:"left_descending.1",
        location: [
            octo2_shift_x - 2 * Math.SQRT2, octo2_shift_y - 2 * Math.SQRT2
        ]
    },
    test_2_3: {
        name: "3",
        width: 2,
        rotation: 180,
        label_type:"left.1",
        location: [
            octo2_shift_x - 4, octo2_shift_y
        ]
    },
    test_2_4: {
        name: "4",
        width: 2,
        rotation: 225,
        label_type:"left_ascending.1",
        location: [
            octo2_shift_x - 2 * Math.SQRT2, octo2_shift_y + 2 * Math.SQRT2
        ]
    },
    test_2_5: {
        name: "5",
        width: 2,
        rotation: 270,
        label_type:"left_ascending.1",
        location: [
            octo2_shift_x, octo2_shift_y + 4
        ]
    },
    test_2_6: {
        name: "6",
        width: 2,
        rotation: 315,
        label_type:"right_descending.1",
        location: [
            octo2_shift_x + 2 * Math.SQRT2, octo2_shift_y + 2 * Math.SQRT2
        ]
    },
    test_2_7: {
        name: "7",
        width: 2,
        rotation: 0,
        label_type:"right.1",
        location: [
            octo2_shift_x + 4, octo2_shift_y
        ]
    },
    test_2_8: {
        name: "8",
        width: 2,
        rotation: 45,
        label_type:"right_ascending.1",
        location: [
            octo2_shift_x + 2 * Math.SQRT2, octo2_shift_y - 2 * Math.SQRT2
        ]
    },


    test_1: {
        name: "1",
        location: [
            octo_shift_x, octo_shift_y - 4
        ],
        //label_type: "right_ascending",
    },
    test_2: {
        name: "2",
        location: [
            octo_shift_x - 2 * Math.SQRT2, octo_shift_y - 2 * Math.SQRT2
        ],
        label_type: "left_descending",
    },
    test_3: {
        name: "3",
        location: [
            octo_shift_x - 4, octo_shift_y
        ],
        label_type: "left",
    },
    test_4: {
        name: "4",
        location: [
            octo_shift_x - 2 * Math.SQRT2, octo_shift_y + 2 * Math.SQRT2
        ],
        label_type: "left_ascending",
    },
    test_5: {
        name: "5",
        location: [
            octo_shift_x, octo_shift_y + 4
        ],
        label_type: "left_ascending",
    },
    test_6: {
        name: "6",
        location: [
            octo_shift_x + 2 * Math.SQRT2, octo_shift_y + 2 * Math.SQRT2
        ],
        label_type: "right_descending",
    },
    test_7: {
        name: "7",
        location: [
            octo_shift_x + 4, octo_shift_y
        ],
        label_type: "right",
    },
    test_8: {
        name: "8",
        location: [
            octo_shift_x + 2 * Math.SQRT2, octo_shift_y - 2 * Math.SQRT2
        ],
        label_type: "right_ascending",
    },
}



let lines = {
    test_large_station: {
        color: current_color_theme.line_colors[0],
        width: 0.4,
        stops: [
            [[-13, 15], "test_width_3_height_2,0,0"],
            [[-13, 16], "test_width_3_height_2,0,1"],
            [[-10, 12], "test_width_3_height_2,0"],
            [[-9, 12], "test_width_3_height_2,1"],
            [[-8, 12], "test_width_3_height_2,2"],
            ["test_width_3_height_2,0,0", "test_width_3_height_2_rot,0,0"],
            ["test_width_3_height_2,2,1", "test_width_3_height_2_rot,0,1"],
        ]
    },
    test_line_2: {
        color: current_color_theme.line_colors[4],
        width: 0.4,
        attributes: {
            style: {
                // "box-shadow": "0 0 3px 1px " + current_color_theme.line_colors[4],
            }
        },
        stops: [
            [
                "test_2_1",
                "test_2_2",
                "test_2_3",
                "test_2_4",
                "test_2_5",
                "test_2_6",
                "test_2_7",
                "test_2_8",
                "test_2_1",
            ], [
                "test_2_1,1",
                "test_2_2,1",
                "test_2_3,1",
                "test_2_4,1",
                "test_2_5,1",
                "test_2_6,1",
                "test_2_7,1",
                "test_2_8,1",
                "test_2_1,1",
            ],
        ]
    },
    test_line_1: {
        color: current_color_theme.line_colors[1],
        width: 0.4,
        attributes: {
            style: {
                // "box-shadow": "0 0 3px 1px " + current_color_theme.line_colors[4],
            }
        },
        stops: [
            [
                "test_1",
                "test_2",
                "test_3",
                "test_4",
                "test_5",
                "test_6",
                "test_7",
                "test_8",
                "test_1",
            ],
            [
                "test_1",
                "test_5",
            ],
            [
                "test_2",
                "test_6",
            ],
            [
                "test_3",
                "test_7",
            ],
            [
                "test_4",
                "test_8",
            ],
        ]
    },
    rhein: {
        color: current_color_theme.deep_river,
        width: 5,
        attributes: {
            style: {
                "z-index": -10,
                // "box-shadow": "0 0 5px 2px " + current_color_theme.deep_river
            },
        },
        stops: [
            [24, -9,],
            [36, -9,],
            [36, 7],
            [34, 9],
            [25, 9],
        ]
    },
    grid: {
        color: current_color_theme.city_border,
        width: 1,
        stops: [

        ]
    },
    border: {
        color: current_color_theme.city_border,
        width: 0.4,
        stops: [
            [-15, -13,],
            [-15, 23,],
            [40, 23,],
            [40, -13,],
            [-15, -13,],
        ]
    },
    test_factor: {
        color: current_color_theme.line_colors[6],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[6]
            },
        },
        stops: [
            "test_width_multiplicator_315"
        ]
    },
    test_factor2: {
        color: current_color_theme.line_colors[3],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[3]
            },
        },
        stops: [
            "test_width_multiplicator_315,1"
        ]
    },
    test_factor3: {
        color: current_color_theme.line_colors[5],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[5]
            },
        },
        stops: [
            "test_width_multiplicator_315,2"
        ]
    },
    test_factor4: {
        color: current_color_theme.line_colors[1],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[1]
            },
        },
        stops: [
            "test_width_multiplicator_315,3"
        ]
    },
    test_rotated_large: {
        color: current_color_theme.line_colors[1],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[1]
            },
        },
        stops: [
            "test_large_node_rot_315,0",
            "test_large_node_rot_0,0",
            "test_large_node_rot_45,1",
            "test_large_node_rot_45,0",
            "test_large_node_rot_90,0",
            "test_large_node_rot_135,1",
            "test_large_node_rot_135,0",
            "test_large_node_rot_180,0",
            "test_large_node_rot_225,1",
            "test_large_node_rot_225,0",
            "test_large_node_rot_270,0",
            "test_large_node_rot_270,0",
            "test_large_node_rot_315,1",
        ]
    },
    test_rotated_large2: {
        color: current_color_theme.line_colors[5],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[5]
            },
        },
        stops: [
            "test_large_node_rot_315,1,0",
            "test_large_node_rot_0,1,1",
            "test_large_node_rot_45,1,1",
            "test_large_node_rot_45,1",
            "test_large_node_rot_90,1,1",
            "test_large_node_rot_135,1,1",
            "test_large_node_rot_135,1",
            "test_large_node_rot_180,1",
            "test_large_node_rot_225,1,1",
            "test_large_node_rot_225,1",
            "test_large_node_rot_270,1,1",
            "test_large_node_rot_270,1",
            "test_large_node_rot_315,1,1",
        ]
    },
    test_rotated_large3: {
        color: current_color_theme.line_colors[3],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[3]
            },
        },
        stops: [
            [
                "test_large_node_center,5,1",
                "test_large_node_rot_0,0,0",
            ],
            [
                "test_large_node_center,0,1",
                "test_large_node_rot_180,0,1",
            ],
            [
                "test_large_node_center,2,0",
                "test_large_node_rot_90,1,1",
            ],
            [
                "test_large_node_center,2,3",
                "test_large_node_rot_270,0,2",
            ],
            [
                "test_large_node_center,4,0",
                "test_large_node_rot_90,1,3",
            ],
            [
                "test_large_node_center,4,1",
                "test_large_node_rot_270,0,0",
            ],
        ]
    },
    test_rotated_large4: {
        color: current_color_theme.line_colors[6],
        width: 0.4,
        attributes: {
            style: {
                "box-shadow": "0 0 5px 2px " + current_color_theme.line_colors[6]
            },
        },
        stops: [
            [
                "test_large_node_center,5,2",
                "test_large_node_rot_0,1,1",
            ],
            [
                "test_large_node_center,0,2",
                "test_large_node_rot_180,1,0",
            ],
            [
                "test_large_node_center,1,0",
                "test_large_node_rot_90,1,0",
            ],
            [
                "test_large_node_center,1,3",
                "test_large_node_rot_270,0,3",
            ],
            [
                "test_large_node_center,3,0",
                "test_large_node_rot_90,0,2",
            ],
            [
                "test_large_node_center,3,3",
                "test_large_node_rot_270,0,1",
            ],
        ]
    },
}
let node_types = {}

let rotations = [0, 45, 90, 135, 180, 225, 270, 315]

nodes["test_large_node_center"] = {
    name: "",
    width: 6,
    height: 4,
    location: [
        13, 14
    ],
}

rotations.forEach(element => {
    let node_name = "test_rotation_" + element
    nodes[node_name] = {
        name: "",
        width: 2,
        factor: {
            45: Math.SQRT2,
            135: Math.SQRT2,
            225: Math.SQRT2,
            315: Math.SQRT2,
        }[element],
        rotation: element,
        location: {
            0: [30, 4],
            45: [30, -3],
            90: [28, 3],
            135: [30, 3],
            180: [29, 4],
            225: [29, -2],
            270: [29, -4],
            315: [30, -2],
        }[element],
    }


    node_name = "test_large_node_rot_" + element
    nodes[node_name] = {
        name: "",
        width: {
            0: 2,
            45: 2,
            90: 2,
            135: 2,
            180: 2,
            225: 2,
            270: 2,
            315: 2,
        }[element],
        height: {
            0: 2,
            45: 2,
            90: 4,
            135: 2,
            180: 2,
            225: 2,
            270: 4,
            315: 2,
        }[element],
        rotation: element,
        factor: {
            0: 1,
            45: Math.SQRT2,
            90: 1,
            135: Math.SQRT2,
            180: 1,
            225: Math.SQRT2,
            270: 1,
            315: Math.SQRT2,
        }[element],
        location: {
            0: [20, 15],
            45: [19, 12],
            90: [14, 12],
            135: [11, 13],
            180: [11, 16],
            225: [12, 19],
            270: [17, 19],
            315: [20, 18],
        }[element],
    }

    let x = 13
    let y = 6
    let dx = 4
    let dy = 0

    let locations = {
        0: [1, 0],
        45: [1, -1],
        90: [0, -1],
        135: [-1, -1],
        180: [-1, 0],
        225: [-1, 1],
        270: [0, 1],
        315: [1, 1],
    }

    node_name = "test_width_multiplicator_" + element
    nodes[node_name] = {
        name: "",
        width: 4,
        rotation: element,
        factor: (locations[element][0] ** 2 === 1 && locations[element][1] ** 2 === 1) ? Math.sqrt(2) : 1,
        location: [locations[element][0] * x + dx, locations[element][1] * y + dy]
    }
    console.log(node_name, nodes[node_name].factor)
    lines.test_factor.stops.push(node_name)
    lines.test_factor2.stops.push(node_name + ",1")
    lines.test_factor3.stops.push(node_name + ",2")
    lines.test_factor4.stops.push(node_name + ",3")
})


let a = [-1, 0, 1]
let gx = 27
let gy = 0
let gmul = 5

a.forEach(x => {
    lines.grid.stops.push(
        [
            [x * gmul + gx, gy + gmul],
            [x * gmul + gx, gy - gmul]
        ]
    )
})
a.forEach(y => {
    lines.grid.stops.push(
        [
            [gx + gmul, gy + y * gmul],
            [gx - gmul, gy + y * gmul]
        ]
    )
})
