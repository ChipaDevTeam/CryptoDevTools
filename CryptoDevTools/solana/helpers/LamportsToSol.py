

class LamportsToSol:
    @staticmethod
    def convert(lamports: int) -> float:
        """
        Convert lamports to SOL.

        Args:
            lamports (int): The amount in lamports.

        Returns:
            float: The equivalent amount in SOL.
        """
        return lamports / 1_000_000_000