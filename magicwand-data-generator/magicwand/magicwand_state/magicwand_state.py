# mypy: ignore-errors
"""
    Purpose:
        The MagicwandState is responsible for holding state information for the CLI
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from magicwand.magicwand_utils import magicwand_utils
from magicwand.magicwand_config.config import Config


class MagicwandState:
    """
    Purpose:
        The MagicwandState is responsible for holding state information for the CLI
    """

    ###
    # Attributes
    ###

    # Base Config Option
    config = None

    ###
    # Lifecycle Methods
    ###

    def __init__(self) -> None:
        """
        Purpose:
            Initialize the MagicwandState object.
        Args:
            N/A
        Returns:
            magicwand_state_obj (MagicwandState Obj): State object
        """

        self.config = magicwand_utils.load_configs()

    def __repr__(self) -> str:
        """
        Purpose:
            Representation of the MagicwandState object.
        Args:
            N/A
        Returns:
            str_MagicwandState: String representation of MagicwandState
        """

        return f"<MagicwandState (version {Config.VERSION})>"
