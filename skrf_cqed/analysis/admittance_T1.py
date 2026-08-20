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
