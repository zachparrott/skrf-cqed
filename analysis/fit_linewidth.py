from resonator_tools.circuit import notch_port, reflection_port


# to add later, for removing a provided background
def background_subtraction():
    pass


# S21 transmission fit
def fit_notch_resonator():
    """
    Fits a notch resonator to the transmission data.

    Assumes network is a skrf.Network object with the measured S-parameters.
    Assumes only a two port network.
    """

    port = notch_port(f_data=freqs, z_data_raw=network.z)

    pass


# S11 reflection fit
def fit_reflection_resonator():
    """
    Fits a reflection resonator to the reflection data.

    Assumes network is a skrf.Network object with the measured S-parameters.
    Assumes only a one port network.
    """

    port = reflection_port(f_data=freqs, z_data_raw=network.z)

    pass
