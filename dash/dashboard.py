import numpy as np
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import json

import data_handler as dh

##### Preliminary setup ########################################################
data_options = [
    {'label':'Stability Time', 'value':0},
    {'label': 'LI', 'value': 1},
    {'label': 'LEI', 'value': 2}
]
handler_list = [
    dh.stability_data_handler,
    dh.LI_data_handler,
    dh.LEI_data_handler
]
################################################################################


##### DASH Framework ###########################################################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
################################################################################


##### TAB1 LAYOUT ##############################################################
blocks = [
    dbc.Col([
        dbc.Row(
            dcc.Graph(
                id={
                    'type': 'figure',
                    'index': i
                },
                figure=go.Figure()
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="Plot options",
                            ),
                            dcc.Checklist(
                                id={
                                    'type': 'plot_options',
                                    'index': i
                                },
                                options=[
                                    {'label': ' Log10 scale', 'value': 'log10'},
                                ],
                                value=[]
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'data_picker',
                                            'index': i
                                },
                                children="Data visualizer {}".format(i),
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'main_dropdown',
                                            'index': i
                                },
                                options=data_options,
                                value=0,
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_0',
                                    'index': i
                                },
                                children="parameter_0",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_0',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_1',
                                    'index': i
                                },
                                children="parameter_1",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_1',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_2',
                                    'index': i
                                },
                                children="parameter_2",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_2',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
            ],
            form=True,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_3',
                                    'index': i
                                },
                                children="parameter_3",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_3',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_4',
                                    'index': i
                                },
                                children="parameter_4",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_4',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_5',
                                    'index': i
                                },
                                children="parameter_5",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_5',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
            ],
        ),
    ])
for i in range(6)
]

################################################################################

##### TAB2 LAYOUT ##############################################################
tab_2_content = [
    dbc.Col([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'corr_figure',
                    'index': i
                },
                figure=go.Figure()
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'corr_figure_bis',
                    'index': i
                },
                figure=go.Figure()
            )
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Data options X axis",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'plot_options',
                                        'index': i
                                    },
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'data_picker',
                                        'index': i
                                    },
                                    children="Data to place on X axis",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'main_dropdown',
                                        'index': i
                                    },
                                    options=data_options,
                                    value=0,
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_0',
                                        'index': i
                                    },
                                    children="parameter_0",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_0',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_1',
                                        'index': i
                                    },
                                    children="parameter_1",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_1',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_2',
                                        'index': i
                                    },
                                    children="parameter_2",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_2',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
                form=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_3',
                                        'index': i
                                    },
                                    children="parameter_3",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_3',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_4',
                                        'index': i
                                    },
                                    children="parameter_4",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_4',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_5',
                                        'index': i
                                    },
                                    children="parameter_5",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_5',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
            ) ]),
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Data options Y Axis",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'plot_options',
                                        'index': i + 1
                                    },
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'data_picker',
                                        'index': i + 1
                                    },
                                    children="Data to place on Y axis",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'main_dropdown',
                                        'index': i + 1
                                    },
                                    options=data_options,
                                    value=0,
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_0',
                                        'index': i + 1
                                    },
                                    children="parameter_0",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_0',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_1',
                                        'index': i + 1
                                    },
                                    children="parameter_1",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_1',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_2',
                                        'index': i + 1
                                    },
                                    children="parameter_2",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_2',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
                form=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_3',
                                        'index': i + 1
                                    },
                                    children="parameter_3",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_3',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_4',
                                        'index': i + 1
                                    },
                                    children="parameter_4",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_4',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_5',
                                        'index': i + 1
                                    },
                                    children="parameter_5",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_5',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
            ), ]),
    ])
    ])
for i in range(6,8,2)]
################################################################################


##### FINAL LAYOUT #############################################################
app.layout = html.Div(dbc.Tabs([
    dbc.Tab(
        [
            dbc.Row(blocks[0:3]),
            dbc.Row(blocks[3:6])
        ],
        label="Heatmaps",
    ),
    dbc.Tab(
        [
            dbc.Row(tab_2_content[0])
        ],
        label="Correlation plot",
    )
]))
################################################################################


##### CALLBACKS ################################################################

#### Options update ####

# 0
@app.callback(
    Output({'type': 'dropdown_0', 'index': MATCH}, 'options'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_dropdown_0(value):
    value = handler_list[value]
    if len(value.get_param_list()) == 0:
        return []

    option_list = value.get_param_options(value.get_param_list()[0])
    return [{'label': str(s), 'value': s} for s in option_list]


@app.callback(
    Output({'type': 'dropdown_0', 'index': MATCH}, 'value'),
    Input({'type': 'dropdown_0', 'index': MATCH}, 'options')
)
def update_default_dropdown_value_0(value):
    if len(value) == 0:
        raise PreventUpdate
    else:
        return value[0]['value']


@app.callback(
    Output({'type': 'label_0', 'index': MATCH}, 'children'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_label_0(value):
    value = handler_list[value]
    if len(value.get_param_list()) == 0:
        return "parameter_0"

    return value.get_param_list()[0]


# 1
@app.callback(
    Output({'type': 'dropdown_1', 'index': MATCH}, 'options'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_dropdown_1(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 1:
        return []

    option_list = value.get_param_options(value.get_param_list()[1])
    return [{'label': str(s), 'value': s} for s in option_list]


@app.callback(
    Output({'type': 'dropdown_1', 'index': MATCH}, 'value'),
    Input({'type': 'dropdown_1', 'index': MATCH}, 'options')
)
def update_default_dropdown_value_1(value):
    if len(value) == 0:
        raise PreventUpdate
    else:
        return value[0]['value']


@app.callback(
    Output({'type': 'label_1', 'index': MATCH}, 'children'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_label_1(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 1:
        return "parameter_1"

    return value.get_param_list()[1]


# 2
@app.callback(
    Output({'type': 'dropdown_2', 'index': MATCH}, 'options'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_dropdown_2(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 2:
        return []

    option_list = value.get_param_options(value.get_param_list()[2])
    return [{'label': str(s), 'value': s} for s in option_list]


@app.callback(
    Output({'type': 'dropdown_2', 'index': MATCH}, 'value'),
    Input({'type': 'dropdown_2', 'index': MATCH}, 'options')
)
def update_default_dropdown_value_2(value):
    if len(value) == 0:
        raise PreventUpdate
    else:
        return value[0]['value']


@app.callback(
    Output({'type': 'label_2', 'index': MATCH}, 'children'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_label_2(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 2:
        return "parameter_2"

    return value.get_param_list()[2]


# 3
@app.callback(
    Output({'type': 'dropdown_3', 'index': MATCH}, 'options'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_dropdown_3(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 3:
        return []

    option_list = value.get_param_options(value.get_param_list()[3])
    return [{'label': str(s), 'value': s} for s in option_list]


@app.callback(
    Output({'type': 'dropdown_3', 'index': MATCH}, 'value'),
    Input({'type': 'dropdown_3', 'index': MATCH}, 'options')
)
def update_default_dropdown_value_3(value):
    if len(value) == 0:
        raise PreventUpdate
    else:
        return value[0]['value']


@app.callback(
    Output({'type': 'label_3', 'index': MATCH}, 'children'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_label_3(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 3:
        return "parameter_3"

    return value.get_param_list()[3]


# 4
@app.callback(
    Output({'type': 'dropdown_4', 'index': MATCH}, 'options'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_dropdown_4(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 4:
        return []

    option_list = value.get_param_options(value.get_param_list()[4])
    return [{'label': str(s), 'value': s} for s in option_list]


@app.callback(
    Output({'type': 'dropdown_4', 'index': MATCH}, 'value'),
    Input({'type': 'dropdown_4', 'index': MATCH}, 'options')
)
def update_default_dropdown_value_4(value):
    if len(value) == 0:
        raise PreventUpdate
    else:
        return value[0]['value']


@app.callback(
    Output({'type': 'label_4', 'index': MATCH}, 'children'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_label_4(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 4:
        return "parameter_4"

    return value.get_param_list()[4]


# 5
@app.callback(
    Output({'type': 'dropdown_5', 'index': MATCH}, 'options'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_dropdown_5(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 5:
        return []

    option_list = value.get_param_options(value.get_param_list()[5])
    return [{'label': str(s), 'value': s} for s in option_list]


@app.callback(
    Output({'type': 'dropdown_5', 'index': MATCH}, 'value'),
    Input({'type': 'dropdown_5', 'index': MATCH}, 'options')
)
def update_default_dropdown_value_5(value):
    if len(value) == 0:
        raise PreventUpdate
    else:
        return value[0]['value']


@app.callback(
    Output({'type': 'label_5', 'index': MATCH}, 'children'),
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_label_5(value):
    value = handler_list[value]
    if len(value.get_param_list()) <= 5:
        return "parameter_5"

    return value.get_param_list()[5]


#### Grab data and create figure ####

@app.callback(
    Output({'type': 'figure', 'index': MATCH}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_1', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_2', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_3', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_4', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_5', 'index': MATCH}, 'value'),
        Input({'type': 'plot_options', 'index': MATCH}, 'value'),
    ],
    State({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
def update_figure(*args):
    handler = handler_list[args[7]]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = args[i]
    log_scale = True if 'log10' in args[6] else False
    return handler.get_plot(param_dict, log_scale)


#### Same thing but for the correlation plot ###
@app.callback(
    Output({'type': 'corr_figure', 'index': 6}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': 6}, 'value'),    # 0
        Input({'type': 'dropdown_1', 'index': 6}, 'value'),    # 1
        Input({'type': 'dropdown_2', 'index': 6}, 'value'),    # 2
        Input({'type': 'dropdown_3', 'index': 6}, 'value'),    # 3
        Input({'type': 'dropdown_4', 'index': 6}, 'value'),    # 4
        Input({'type': 'dropdown_5', 'index': 6}, 'value'),    # 5
        Input({'type': 'plot_options', 'index': 6}, 'value'),  # 6
        Input({'type': 'dropdown_0', 'index': 7}, 'value'),    # 7
        Input({'type': 'dropdown_1', 'index': 7}, 'value'),    # 8
        Input({'type': 'dropdown_2', 'index': 7}, 'value'),    # 9
        Input({'type': 'dropdown_3', 'index': 7}, 'value'),    # 10
        Input({'type': 'dropdown_4', 'index': 7}, 'value'),    # 11
        Input({'type': 'dropdown_5', 'index': 7}, 'value'),    # 12
        Input({'type': 'plot_options', 'index': 7}, 'value')   # 13
    ],
    [
        State({'type': 'main_dropdown', 'index': 6}, 'value'),  # 14
        State({'type': 'main_dropdown', 'index': 7}, 'value')  # 15
    ]
)
def update_correlation_plot(*args):
    handler_1 = handler_list[args[14]]
    handler_2 = handler_list[args[15]]

    param_list_1 = handler_1.get_param_list()
    param_dict_1 = {}
    for i in range(len(param_list_1)):
        param_dict_1[param_list_1[i]] = args[i]
    print(param_list_1)
    data_1 = handler_1.get_data(param_dict_1)
    if 'log10' in args[6]:
        data_1 = np.log10(data_1)

    param_list_2 = handler_2.get_param_list()
    param_dict_2 = {}
    for i in range(len(param_list_2)):
        param_dict_2[param_list_2[i]] = args[i + 7]
    data_2 = handler_2.get_data(param_dict_2)
    if 'log10' in args[13]:
        data_2 = np.log10(data_2)

    # make plot
    data_1 = data_1.flatten()
    data_2 = data_2.flatten()

    fig = go.Figure(
        data=go.Scattergl(
            x=data_1,
            y=data_2,
            mode='markers'
        )
    )

    fig.update_layout(
        title="Correlation Scatter Plot [DEMO]"
    )

    return fig


@app.callback(
    Output({'type': 'corr_figure_bis', 'index': 6}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': 6}, 'value'),    # 0
        Input({'type': 'dropdown_1', 'index': 6}, 'value'),    # 1
        Input({'type': 'dropdown_2', 'index': 6}, 'value'),    # 2
        Input({'type': 'dropdown_3', 'index': 6}, 'value'),    # 3
        Input({'type': 'dropdown_4', 'index': 6}, 'value'),    # 4
        Input({'type': 'dropdown_5', 'index': 6}, 'value'),    # 5
        Input({'type': 'plot_options', 'index': 6}, 'value'),  # 6
        Input({'type': 'dropdown_0', 'index': 7}, 'value'),    # 7
        Input({'type': 'dropdown_1', 'index': 7}, 'value'),    # 8
        Input({'type': 'dropdown_2', 'index': 7}, 'value'),    # 9
        Input({'type': 'dropdown_3', 'index': 7}, 'value'),    # 10
        Input({'type': 'dropdown_4', 'index': 7}, 'value'),    # 11
        Input({'type': 'dropdown_5', 'index': 7}, 'value'),    # 12
        Input({'type': 'plot_options', 'index': 7}, 'value')   # 13
    ],
    [
        State({'type': 'main_dropdown', 'index': 6}, 'value'),  # 14
        State({'type': 'main_dropdown', 'index': 7}, 'value')  # 15
    ]
)
def update_correlation_plot_bis(*args):
    handler_1 = handler_list[args[14]]
    handler_2 = handler_list[args[15]]

    param_list_1 = handler_1.get_param_list()
    param_dict_1 = {}
    for i in range(len(param_list_1)):
        param_dict_1[param_list_1[i]] = args[i]
    print(param_list_1)
    data_1 = handler_1.get_data(param_dict_1)
    if 'log10' in args[6]:
        data_1 = np.log10(data_1)

    param_list_2 = handler_2.get_param_list()
    param_dict_2 = {}
    for i in range(len(param_list_2)):
        param_dict_2[param_list_2[i]] = args[i + 7]
    data_2 = handler_2.get_data(param_dict_2)
    if 'log10' in args[13]:
        data_2 = np.log10(data_2)

    # make plot
    data_1 = data_1.flatten()
    data_2 = data_2.flatten()

    fig = go.Figure(
        go.Histogram2dContour(
            x=data_1,
            y=data_2,
        )
    )

    fig.update_layout(
        title="Correlation Density Plot [DEMO]"
    )

    return fig


################################################################################


##### RUN THE SERVER ###########################################################
app.run_server(debug=True)
################################################################################
