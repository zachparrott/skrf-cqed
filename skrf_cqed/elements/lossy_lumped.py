# scikit rf capacitor_q does not have adjustable frequency dependence
from numpy import zeros
from skrf.constants import NumberLike
from skrf.frequency import Frequency
from skrf.network import Network


def capacitorQ(
    frequency: Frequency,
    C: NumberLike,
    Q: NumberLike,
    alpha: float = 0.0,
    ref_freq: float = 0.0,
    name=None,
) -> Network:
    """
    Create a capacitor with a specified quality factor (Q).

    Defaults to a frequency-independent Q if alpha is not specified.
    The Q can be made frequency-dependent by specifying a non-zero alpha.

    Parameters
    ----------
    frequency : skrf.Frequency
        The frequency object defining the frequency points.
    C : float
        Capacitance in Farads.
    Q : float
        Quality factor of the capacitor at the reference frequency.
    alpha : float
        Frequency dependence exponent.
    ref_freq : float
        Reference frequency at which the Q is defined.
    name : str, optional
        Name of the network.

    Returns
    -------
    skrf.Network
        A network representing the lossy capacitor.
    """

    Q_list = Q * (frequency.f / ref_freq) ** alpha

    Y = frequency.w * C * (1j + 1 / Q_list)

    Y_matrix = zeros((len(frequency), 2, 2), dtype=complex)
    Y_matrix[:, 0, 0] = Y
    Y_matrix[:, 1, 1] = Y
    Y_matrix[:, 0, 1] = -Y
    Y_matrix[:, 1, 0] = -Y

    return Network(frequency=frequency, y=Y_matrix, name=name)


def inductorQ(
    frequency: Frequency,
    L: NumberLike,
    Q: NumberLike,
    alpha: float = 0.0,
    ref_freq: float = 0.0,
    name=None,
) -> Network:
    """
    Create an inductor with a specified quality factor (Q).

    Defaults to a frequency-independent Q if alpha is not specified.
    The Q can be made frequency-dependent by specifying a non-zero alpha.

    Parameters
    ----------
    frequency : skrf.Frequency
        The frequency object defining the frequency points.
    L : float
        Inductance in Henrys.
    Q : float
        Quality factor of the inductor at the reference frequency.
    alpha : float
        Frequency dependence exponent.
    ref_freq : float
        Reference frequency at which the Q is defined.
    name : str, optional
        Name of the network.

    Returns
    -------
    skrf.Network
        A network representing the lossy inductor.
    """

    Q_list = Q * (frequency.f / ref_freq) ** alpha

    Z = frequency.w * L * (1j + 1 / Q_list)

    Z_matrix = zeros((len(frequency), 2, 2), dtype=complex)
    Z_matrix[:, 0, 0] = Z
    Z_matrix[:, 1, 1] = Z
    Z_matrix[:, 0, 1] = -Z
    Z_matrix[:, 1, 0] = -Z

    return Network(frequency=frequency, z=Z_matrix, name=name)
