import plotly.graph_objects as go
import numpy as np
import h5py
import os


def faddeev_leverrier(m, grade=1):
    assert grade > 0
    step = 1
    B = m.copy()
    p = np.trace(B)
    while step != grade:
        step += 1
        B = np.matmul(m, B - np.identity(B.shape[-1]) * p)
        p = np.trace(B) * (1 / step)
    return p * ((-1) ** (grade + 1))


v_faddeev_leverrier = np.vectorize(
    faddeev_leverrier, signature="(n,m),(1)->(1)")


class data_handler(object):
    def __init__(self, datapath_dict, param_dict, f_data, f_plot):
        self.datapath_dict = datapath_dict
        self.param_dict = param_dict
        self.f_data = f_data
        self.f_plot = f_plot

    def get_param_list(self):
        return list(self.param_dict.keys())

    def get_param_options(self, param):
        if param not in self.param_dict:
            raise ValueError("param not in dictionary")
        else:
            return self.param_dict[param]

    def get_data(self, parameters):
        return self.f_data(parameters)

    def get_plot(self, parameters, log_scale=False):
        return self.f_plot(parameters, log_scale)

data_path = "../data"

#### STABILITY ####

stability_param_dict = {
    "kick": ["no_kick", 1e-8, 1e-12],
    "mu": [0.0, 0.2, -0.2, 1.0, -1.0],
    "epsilon": [0.0, 1.0, 16.0, 64.0]
}

stability_data_filenames = {
    "no_kick" : {
        0.0: {
            0.0: "henon_4d_long_track_eps_0_0_mu_0_0_id_basic_view.hdf5",
            1.0: "henon_4d_long_track_eps_1_0_mu_0_0_id_basic_view.hdf5",
            16.0: "henon_4d_long_track_eps_1_6e+01_mu_0_0_id_basic_view.hdf5",
            64.0: "henon_4d_long_track_eps_6_4e+01_mu_0_0_id_basic_view.hdf5",
        },

        0.2: {
            0.0: "henon_4d_long_track_eps_0_0_mu_0_2_id_basic_view.hdf5",
            1.0: "henon_4d_long_track_eps_1_0_mu_0_2_id_basic_view.hdf5",
            16.0: "henon_4d_long_track_eps_1_6e+01_mu_0_2_id_basic_view.hdf5",
            64.0: "henon_4d_long_track_eps_6_4e+01_mu_0_2_id_basic_view.hdf5",
        },

        -0.2: {
            0.0: "henon_4d_long_track_eps_0_0_mu_-0_2_id_basic_view.hdf5",
            1.0: "henon_4d_long_track_eps_1_0_mu_-0_2_id_basic_view.hdf5",
            16.0: "henon_4d_long_track_eps_1_6e+01_mu_-0_2_id_basic_view.hdf5",
            64.0: "henon_4d_long_track_eps_6_4e+01_mu_-0_2_id_basic_view.hdf5",
        },

        1.0: {
            0.0: "henon_4d_long_track_eps_0_0_mu_1_0_id_basic_view.hdf5",
            1.0: "henon_4d_long_track_eps_1_0_mu_1_0_id_basic_view.hdf5",
            16.0: "henon_4d_long_track_eps_1_6e+01_mu_1_0_id_basic_view.hdf5",
            64.0: "henon_4d_long_track_eps_6_4e+01_mu_1_0_id_basic_view.hdf5",
        },

        -1.0: {
            0.0: "henon_4d_long_track_eps_0_0_mu_-1_0_id_basic_view.hdf5",
            1.0: "henon_4d_long_track_eps_1_0_mu_-1_0_id_basic_view.hdf5",
            16.0: "henon_4d_long_track_eps_1_6e+01_mu_-1_0_id_basic_view.hdf5",
            64.0: "henon_4d_long_track_eps_6_4e+01_mu_-1_0_id_basic_view.hdf5",
        }
    },

    1e-8: {
        0.0: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_0_0_id_basic_view_subid_1e-8.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_0_0_id_basic_view_subid_1e-8.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_0_0_id_basic_view_subid_1e-8.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_0_0_id_basic_view_subid_1e-8.hdf5",
        },

        0.2: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_0_2_id_basic_view_subid_1e-8.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_0_2_id_basic_view_subid_1e-8.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_0_2_id_basic_view_subid_1e-8.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_0_2_id_basic_view_subid_1e-8.hdf5",
        },

        -0.2: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_-0_2_id_basic_view_subid_1e-8.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_-0_2_id_basic_view_subid_1e-8.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_-0_2_id_basic_view_subid_1e-8.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_-0_2_id_basic_view_subid_1e-8.hdf5",
        },

        1.0: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_1_0_id_basic_view_subid_1e-8.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_1_0_id_basic_view_subid_1e-8.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_1_0_id_basic_view_subid_1e-8.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_1_0_id_basic_view_subid_1e-8.hdf5",
        },

        -1.0: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_-1_0_id_basic_view_subid_1e-8.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_-1_0_id_basic_view_subid_1e-8.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_-1_0_id_basic_view_subid_1e-8.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_-1_0_id_basic_view_subid_1e-8.hdf5",
        }
    },

    1e-12: {
        0.0: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_0_0_id_basic_view_subid_1e-12.hdf5",
        },

        0.2: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_0_2_id_basic_view_subid_1e-12.hdf5",
        },

        -0.2: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
        },

        1.0: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_1_0_id_basic_view_subid_1e-12.hdf5",
        },

        -1.0: {
            0.0: "henon_4d_long_track_wkick_eps_0_0_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_long_track_wkick_eps_1_0_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_long_track_wkick_eps_1_6e+01_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_long_track_wkick_eps_6_4e+01_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
        }
    },
} 

def stability_get_data(parameters):
    filename = stability_data_filenames[parameters["kick"]][parameters["mu"]][parameters["epsilon"]]
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = f["stability_time"][...]
    return data


def stability_get_plot(parameters, log_scale=False):
    data = stability_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False
        )
    )
    fig.update_layout(
        title="Stability time " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


stability_data_handler = data_handler(
    stability_data_filenames,
    stability_param_dict,
    stability_get_data,
    stability_get_plot
)


#### LI ####

# Get turns
with h5py.File(os.path.join(data_path, "henon_4d_displacement_eps_0_0_mu_0_0_id_basic_view_subid_1e-14.hdf5"), mode='r') as f:
    turn_samples = np.logspace(np.log10(f.attrs["min_turns"]), np.log10(
        f.attrs["max_turns"]), f.attrs["samples"], dtype=int)

LI_param_dict = {
    "turns": list(turn_samples),
    "displacement": [1e-12],
    "mu": [0.0, 0.2, -0.2, 1.0, -1.0],
    "epsilon": [0.0, 1.0, 16.0, 64.0]
}

LI_data_filenames = {
    1e-12: {
        0.0: {
            0.0: "henon_4d_displacement_eps_0_0_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_displacement_eps_1_0_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_displacement_eps_1_6e+01_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_displacement_eps_6_4e+01_mu_0_0_id_basic_view_subid_1e-12.hdf5",
        },

        0.2: {
            0.0: "henon_4d_displacement_eps_0_0_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_displacement_eps_1_0_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_displacement_eps_1_6e+01_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_displacement_eps_6_4e+01_mu_0_2_id_basic_view_subid_1e-12.hdf5",
        },

        -0.2: {
            0.0: "henon_4d_displacement_eps_0_0_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_displacement_eps_1_0_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_displacement_eps_1_6e+01_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_displacement_eps_6_4e+01_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
        },

        1.0: {
            0.0: "henon_4d_displacement_eps_0_0_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_displacement_eps_1_0_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_displacement_eps_1_6e+01_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_displacement_eps_6_4e+01_mu_1_0_id_basic_view_subid_1e-12.hdf5",
        },

        -1.0: {
            0.0: "henon_4d_displacement_eps_0_0_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_displacement_eps_1_0_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_displacement_eps_1_6e+01_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_displacement_eps_6_4e+01_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
        }
    },
}

def LI_get_data(parameters):
    filename = LI_data_filenames[parameters["displacement"]][parameters["mu"]][parameters["epsilon"]]
    idx = str(parameters["turns"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        sample = f[idx]
        data = np.log10(np.sqrt(
            np.power(sample["x"][0] - sample["x"][1], 2) +
            np.power(sample["px"][0] - sample["px"][1], 2) +
            np.power(sample["y"][0] - sample["y"][1], 2) +
            np.power(sample["py"][0] - sample["py"][1], 2)
        ) / f.attrs["displacement"]) / parameters["turns"]
    return data


def LI_get_plot(parameters, log_scale=False):
    data = LI_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False
        )
    )
    fig.update_layout(
        title="LI (Fast Lyapunov Indicator) " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


LI_data_handler = data_handler(
    LI_data_filenames,
    LI_param_dict,
    LI_get_data,
    LI_get_plot
)


#### LEI ####

# Get turns
with h5py.File(os.path.join(data_path, "henon_4d_orto_displacement_eps_0_0_mu_0_0_id_basic_view_subid_1e-14.hdf5"), mode='r') as f:
    turn_samples = np.logspace(np.log10(f.attrs["min_turns"]), np.log10(
        f.attrs["max_turns"]), f.attrs["samples"], dtype=int)

LEI_param_dict = {
    "grade": [1,2,3,4,5,6],
    "turns": list(turn_samples),
    "displacement": [1e-12],
    "mu": [0.0, 0.2, -0.2, 1.0, -1.0],
    "epsilon": [0.0, 1.0, 16.0, 64.0]
}

LEI_data_filenames = {
    1e-12: {
        0.0: {
            0.0: "henon_4d_orto_displacement_eps_0_0_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_orto_displacement_eps_1_0_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_orto_displacement_eps_1_6e+01_mu_0_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_orto_displacement_eps_6_4e+01_mu_0_0_id_basic_view_subid_1e-12.hdf5",
        },

        0.2: {
            0.0: "henon_4d_orto_displacement_eps_0_0_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_orto_displacement_eps_1_0_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_orto_displacement_eps_1_6e+01_mu_0_2_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_orto_displacement_eps_6_4e+01_mu_0_2_id_basic_view_subid_1e-12.hdf5",
        },

        -0.2: {
            0.0: "henon_4d_orto_displacement_eps_0_0_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_orto_displacement_eps_1_0_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_orto_displacement_eps_1_6e+01_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_orto_displacement_eps_6_4e+01_mu_-0_2_id_basic_view_subid_1e-12.hdf5",
        },

        1.0: {
            0.0: "henon_4d_orto_displacement_eps_0_0_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_orto_displacement_eps_1_0_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_orto_displacement_eps_1_6e+01_mu_1_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_orto_displacement_eps_6_4e+01_mu_1_0_id_basic_view_subid_1e-12.hdf5",
        },

        -1.0: {
            0.0: "henon_4d_orto_displacement_eps_0_0_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            1.0: "henon_4d_orto_displacement_eps_1_0_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            16.0: "henon_4d_orto_displacement_eps_1_6e+01_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
            64.0: "henon_4d_orto_displacement_eps_6_4e+01_mu_-1_0_id_basic_view_subid_1e-12.hdf5",
        }
    },
}


def LEI_get_data(parameters):
    filename = LEI_data_filenames[parameters["displacement"]
                                 ][parameters["mu"]][parameters["epsilon"]]
    idx = str(parameters["turns"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        sample = f[idx]

        t11 = sample["x"][1] - sample["x"][0]
        t12 = sample["px"][1] - sample["px"][0]
        t13 = sample["y"][1] - sample["y"][0]
        t14 = sample["py"][1] - sample["py"][0]

        t21 = sample["x"][2] - sample["x"][0]
        t22 = sample["px"][2] - sample["px"][0]
        t23 = sample["y"][2] - sample["y"][0]
        t24 = sample["py"][2] - sample["py"][0]

        t31 = sample["x"][3] - sample["x"][0]
        t32 = sample["px"][3] - sample["px"][0]
        t33 = sample["y"][3] - sample["y"][0]
        t34 = sample["py"][3] - sample["py"][0]

        t41 = sample["x"][4] - sample["x"][0]
        t42 = sample["px"][4] - sample["px"][0]
        t43 = sample["y"][4] - sample["y"][0]
        t44 = sample["py"][4] - sample["py"][0]

        tm = np.transpose(np.array([
            [t11, t12, t13, t14],
            [t21, t22, t23, t24],
            [t31, t32, t33, t34],
            [t41, t42, t43, t44]
        ]), axes=(2, 3, 0, 1))
        tmt = np.transpose(tm, axes=(0, 1, 3, 2))
        data = v_faddeev_leverrier(np.matmul(tmt, tm), [parameters["grade"]])[:,:,0]
    return data


def LEI_get_plot(parameters, log_scale=False):
    data = LEI_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False
        )
    )
    fig.update_layout(
        title="LEI (Invariant Lyapunov Indicatr) " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


LEI_data_handler = data_handler(
    LEI_data_filenames,
    LEI_param_dict,
    LEI_get_data,
    LEI_get_plot
)
