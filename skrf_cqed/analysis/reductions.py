from __future__ import annotations

from numpy import arctan2, pi
from skrf.frequency import Frequency
from skrf.network import Network

# skrf
"""
skrf provides a number of methods that may be helpful in speeding things up when
running sweeps.

circuit.update_networks
    - can update some sub network without regenerating reused parts

circuit's auto_reduce
    -

auto_reduce : bool, optional
If True, the circuit will be automatically reduced using :func:`reduce_circuit`.
This will change the circuit connections description, affecting inner current and voltage distributions.
Suitable for cases where only the S-parameters of the final circuit ports are of interest. Default is False.
If `check_duplication`, `split_ground` or `max_nports` are provided as kwargs, `auto_reduce` will be
automatically set to True, as this indicates an intent to use the `reduce_circuit` method.


Optional parameters passed to `reduce_circuit`.

Attributes
----------
check_duplication : bool, optional.
        If True, check if the connections have duplicate names. Default is True.
split_ground : bool, optional.
        If True, split the global ground connection to independent ground connections. Default is True.
split_multi : bool, optional.
        If True, use a splitter to handle connections involving more than two components. This approach
        increases the computational load for individual computations. However, it proves advantageous for
        batch processing by enabling a more comprehensive reduction of circuits, leading to more efficiency
        in batch computations. Default is False.
max_nports : int, optional.
        The maximum number of ports of a Network that can be reduced in circuit. If a Network in the
        circuit has a number of ports (nports), using the Network.connect() method to reduce the circuit's
        dimensions becomes less efficient compared to directly calculating it with Circuit.s_external.
        This value depends on the performance of the computer and the scale of the circuit. Default is 20.
dynamic_networks : Sequence[Network], optional.
        A sequence of Networks to ignore in the reduction process. Default is an empty tuple.


"""


# load ports for T1
# def load_ports(network: Network, ports: list[int]) -> Network:
#     """
#     Given a network and a list of ports, return a new network with only those ports loaded.
#     """
#     # if not all(port < network.number_of_ports for port in ports):
#     #     raise ValueError("All ports must be valid ports of the network.")

#     # Create a new network with only the specified ports
#     new_network = Network(
#         frequency=network.frequency,
#         s=network.s[:, ports, :][:, :, ports],
#         name=f"{network.name}_loaded_ports",
#     )

#     return new_network


def line_loading(load_network: Network, z0: float, f0: float | None = None) -> float:
    """
    Given a load network, return the extra electrical length in degrees the line would see.

    Parameters
    ----------
    load_network : Network
        The load network to evaluate. By default is a single frequency network.
        If the load network has more than one frequency point, the user must provide f0 to evaluate the load network at that frequency.
    z0 : float
        The characteristic impedance of the line.
    f0 : float, optional
        The frequency at which to evaluate the load network. If None, the frequency of the load network is used.

    Returns
    -------
    float
        The extra electrical length in degrees.
    """

    if load_network.number_of_ports != 1:
        raise ValueError("Load network must be a single port network.")

    if load_network.frequency.npoints != 1:
        if f0 is None:
            raise ValueError(
                "Eval. frequency must be provided if load network has more than one frequency point."
            )
        else:
            freq = Frequency(start=f0, stop=f0, npoints=1, unit="Hz")
            # resample
            load_network.resample(freq)

    # load_network is a single frequency network at this point

    Zl = load_network.z[0, 0, 0]
    Gamma = (Zl - z0) / (Zl + z0)

    load_angle = -0.5 * arctan2(Gamma.imag, Gamma.real) * 180 / pi

    return load_angle
