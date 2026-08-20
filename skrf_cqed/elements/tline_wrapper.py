from numpy import deg2rad
from skrf.frequency import Frequency
from skrf.media.media import DefinedGammaZ0


class DefinedBetaZ0(DefinedGammaZ0):
    """
    A media class that defines a transmission line with a specified beta and z0.
    This is useful for creating transmission lines with specific phase velocities.

    Parameters
    ----------
    frequency : skrf.Frequency
        The frequency object defining the frequency points.
    z0 : float
        Characteristic impedance in Ohms.
    vph : float
        Phase velocity in meters per second.

    Returns
    -------
    skrf.Media
        A media object representing the transmission line with the specified beta and z0.
    """

    def __init__(self, frequency: Frequency, z0: float, vph: float):
        beta = frequency.w / vph  # phase constant
        gamma = 1j * beta  # assuming lossless line, alpha = 0
        super().__init__(frequency=frequency, z0=z0, gamma=gamma)

    def line_electrical_length(
        self, angle: float, f0: float, unit: str = "deg", **kwargs
    ) -> float:
        """
        Calculate the electrical length of the transmission line.

        Parameters
        ----------
        angle : float
            The electrical length in degrees or radians.
        unit : str, optional
            The unit of the angle ('deg' for degrees, 'rad' for radians). Default is 'deg'.

        Returns
        -------
        float
            The physical length of the transmission line in meters.
        """
        if unit == "deg":
            angle_rad = deg2rad(angle)
        elif unit == "rad":
            angle_rad = angle
        else:
            raise ValueError("Unit must be 'deg' or 'rad'.")

        # Calculate the physical length using the phase constant
        length = angle_rad / self.beta
        # return length

        length = angle_rad * self.frequency.f / f0 / self.beta

        line = self.line(d=length, unit="m", **kwargs)

        return line
