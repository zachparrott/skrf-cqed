from skrf.network import Network

# Return the Purcell T1 of a qubit coupled to the provided lossy network.


def differential_admittance(network: Network) -> Network:
    """
    Given a two port network to opposite sides of a junction return the differential admittance of the network as seen by the junction.
    """

    numerator = (
        network.y[:, 0, 0] * network.y[:, 1, 1]
        - network.y[:, 0, 1] * network.y[:, 1, 0]
    )
    denominator = (
        network.y[:, 0, 0]
        + network.y[:, 1, 1]
        + network.y[:, 0, 1]
        + network.y[:, 1, 0]
    )
    Y_diff = numerator / denominator

    diff_network = Network(
        frequency=network.frequency, y=Y_diff, name=f"{network.name}_diff"
    )

    return diff_network


def purcell_t1(network: Network, capShunt: float) -> float:
    """
    Assuming a single port network, return the Purcell T1 versus frequency of a qubit coupled to the provided lossy network.
    """
    if network.number_of_ports != 1:
        raise ValueError("Network must be a single port network.")

    GammaP = network.y_re[:, 0, 0] / capShunt

    return 1 / GammaP
