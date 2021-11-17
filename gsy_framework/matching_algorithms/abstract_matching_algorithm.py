from abc import ABC, abstractmethod
from typing import Dict, List

from gsy_framework.data_classes import OrdersMatch


class BaseMatchingAlgorithm(ABC):

    @classmethod
    @abstractmethod
    def get_matches_recommendations(
            cls, matching_data: Dict) -> List[OrdersMatch.serializable_dict]:
        """Calculate and return matches recommendations.

        Args:
            matching_data: {market_uuid: {"offers": [...], "bids": [...], "current_time":"",...}}

        Returns: List[OrdersMatch.serializable_dict()]
        """
