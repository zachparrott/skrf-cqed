# Emulation of AWR model object


from skrf.circuit import Circuit
from skrf.frequency import Frequency
from skrf.network import Network

from skrf_cqed.elements.coupled_lines import coupled_lines
from skrf_cqed.elements.tline_wrapper import DefinedBetaZ0


def halfwave(
    frequency: Frequency, f0: float, position: float, coupleAngle: float, **kwargs
) -> Network:
    """
    Create a halfwave cell consisting of a coupled line and two transmission lines.

    Parameters:
    - frequency: skrf.Frequency object
    - f0: resonant frequency
    - position: position of the coupled line
    - coupleAngle: coupling angle

    Either provide (ZoPlus, ZoMinus) or (zetaC, zetaL) in kwargs for the coupled line.
    Additional kwargs:
    - z0: characteristic impedance (default 50 Ohms)
    - vph: phase velocity (in m/s)
    """

    coupler = coupled_lines(
        frequency=kwargs["frequency"],
        length=position,
        vph=kwargs["vph"],
        z0=kwargs.get("z0", 50),
        name=kwargs.get("name", "CoupledLines"),
        ZoPlus=kwargs.get("ZoPlus"),
        ZoMinus=kwargs.get("ZoMinus"),
        zetaC=kwargs.get("zetaC"),
        zetaL=kwargs.get("zetaL"),
    )

    line = DefinedBetaZ0(frequency, z0=kwargs.get("z0", 50), vph=kwargs["vph"])

    loadingPort1 = 3
    loadingPort3 = 4

    rollAngle = position * 180

    length1 = 180 * rollAngle - 0.5 * coupleAngle - loadingPort1
    length3 = rollAngle - 0.5 * coupleAngle - loadingPort3

    line1 = line.line_electrical_length(length1, f0, unit="deg")
    line3 = line.line_electrical_length(length3, f0, unit="deg")

    connections = [
        [(line1, 0), (coupler, 0)],
        [(line3, 0), (coupler, 2)],
    ]

    circuit = Circuit(connections, name=kwargs.get("name", "HalfwaveCell"))

    return circuit.network
