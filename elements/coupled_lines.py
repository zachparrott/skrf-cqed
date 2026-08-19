import numpy as np
import skrf as rf


def coupled_lines(
    frequency,
    length,
    vph,
    z0=50,
    name="CoupledLines",
    *,
    ZoPlus=None,
    ZoMinus=None,
    zetaC=None,
    zetaL=None,
):
    """
    Calculate the coupled-line response using either:
    - the odd/even mode impedances: (ZoPlus, ZoMinus), or
    - the coupling coefficients: (zetaC, zetaL)

    frequency: skrf.Frequency object
    length: length of the coupled lines (in meters)
    vph: phase velocity (in m/s)
    z0: characteristic impedance (in Ohms)
    name: name of the network

    returns: skrf.Network object representing the coupled lines

    Port labelling matches AWR:
         ____________
    1 - [____________] - 3
         ____________
    2 - [____________] - 4
    """
    # validate the two possible argument groups
    has_impedance_pair = ZoPlus is not None or ZoMinus is not None
    has_zeta_pair = zetaC is not None or zetaL is not None

    if has_impedance_pair and has_zeta_pair:
        raise ValueError(
            "Provide either (ZoPlus, ZoMinus) or (zetaC, zetaL), not both."
        )

    if (ZoPlus is None) ^ (ZoMinus is None):
        raise ValueError("Provide both ZoPlus and ZoMinus together.")

    if (zetaC is None) ^ (zetaL is None):
        raise ValueError("Provide both zetaC and zetaL together.")

    if not has_impedance_pair and not has_zeta_pair:
        raise ValueError(
            "Provide one complete parameter set: (ZoPlus, ZoMinus) or (zetaC, zetaL)."
        )

    # branch 1: use the explicit impedances
    if has_impedance_pair:
        if ZoPlus is None or ZoMinus is None:
            raise ValueError("ZoPlus and ZoMinus must both be provided.")
        # use the provided values directly
        Zo_plus = ZoPlus
        Zo_minus = ZoMinus

    # branch 2: derive the impedances from the coupling coefficients
    else:
        if zetaC is None or zetaL is None:
            raise ValueError("zetaC and zetaL must both be provided.")
        Zo_plus = z0 * np.sqrt((1 + zetaL) / (1 - zetaC))
        Zo_minus = z0 * np.sqrt((1 - zetaL) / (1 + zetaC))

    # now continue with the rest of the calculation
    beta = frequency.w / vph

    if has_zeta_pair:
        beta_plus = beta * np.sqrt((1 - zetaC) * (1 + zetaL))
        beta_minus = beta * np.sqrt((1 + zetaC) * (1 - zetaL))
        theta_plus = beta_plus * length
        theta_minus = beta_minus * length
    else:
        # if you only provide ZoPlus/ZoMinus, you would need thetaPlus/thetaMinus
        # assume it is equal zetas
        zeta = (z0**2 - Zo_minus**2) / (Zo_plus**2 + Zo_minus**2)
        beta_plus = beta * np.sqrt((1 - zeta) * (1 + zeta))
        beta_minus = beta * np.sqrt((1 + zeta) * (1 - zeta))
        theta_plus = beta_plus * length
        theta_minus = beta_minus * length

    z_matrix = np.zeros((len(frequency), 4, 4), dtype=complex)

    z_matrix[:, 0, 0] = z_matrix[:, 1, 1] = z_matrix[:, 2, 2] = z_matrix[:, 3, 3] = (
        -1 / 2 * 1j * (Zo_plus / np.tan(theta_plus) + Zo_minus / np.tan(theta_minus))
    )
    z_matrix[:, 0, 3] = z_matrix[:, 3, 0] = z_matrix[:, 1, 2] = z_matrix[:, 2, 1] = (
        -1 / 2 * 1j * (Zo_plus / np.sin(theta_plus) - Zo_minus / np.sin(theta_minus))
    )
    z_matrix[:, 0, 2] = z_matrix[:, 2, 0] = z_matrix[:, 1, 3] = z_matrix[:, 3, 1] = (
        -1 / 2 * 1j * (Zo_plus / np.sin(theta_plus) + Zo_minus / np.sin(theta_minus))
    )
    z_matrix[:, 0, 1] = z_matrix[:, 1, 0] = z_matrix[:, 2, 3] = z_matrix[:, 3, 2] = (
        -1 / 2 * 1j * (Zo_plus / np.tan(theta_plus) - Zo_minus / np.tan(theta_minus))
    )

    return rf.Network(frequency=frequency, z=z_matrix, name=name)
