from logging import getLogger

from cumplo_common.database.firestore.subcollections import UserSubcollection
from cumplo_common.models.filter_configuration import FilterConfiguration
from cumplo_common.utils.constants import FILTERS_COLLECTION

logger = getLogger(__name__)


class FilterCollection(UserSubcollection):
    __id__ = FILTERS_COLLECTION

    def get(self, id_user: str, id_document: str) -> FilterConfiguration:
        """
        Gets a specific Filter of a given user

        Args:
            id_user (str): The user ID which owns the filter
            id_document (str): The filter ID to be retrieved

        Raises:
            KeyError: When the filter does not exist

        Returns:
            FilterConfiguration: The filter configuration data
        """
        logger.info(f"Getting user {id_user} configurations from Firestore")
        document = self._collection(id_user).document(id_document).get()
        if document.exists and (data := document.to_dict()):
            return FilterConfiguration(id=document.id, **data)

        raise KeyError(f"Filter with ID {id_document} does not exist")

    def get_all(self, id_user: str) -> dict[str, FilterConfiguration]:
        """
        Gets the user configurations data

        Args:
            id_user (str): The user ID which owns the filters

        Returns:
            dict[int, FilterConfiguration]: A dictionary containing the user configurations
        """
        logger.info(f"Getting user {id_user} configurations from Firestore")
        stream = self._collection(id_user).stream()
        return {
            document.id: FilterConfiguration(id=document.id, **data)
            for document in stream
            if (data := document.to_dict())
        }

    def put(self, id_user: str, data: FilterConfiguration) -> None:
        """
        Creates or updates a configuration of a given user

        Args:
            id_user (str): The user ID which owns the configuration
            data (FilterConfiguration): The filter configuration to be upserted
        """
        logger.info(f"Upserting configuration {data.id} of user {id_user} into Firestore")
        document = self._collection(id_user).document(str(data.id))
        document.set(data.json())

    def delete(self, id_user: str, id_document: str) -> None:
        """
        Deletes a configuration for a given user and configuration ID

        Args:
            id_user (str): The user ID which owns the configuration
            id_document (int): The filter ID to be deleted
        """
        logger.info(f"Deleting filter {id_document} from Firestore")
        document = self._collection(id_user).document(id_document)
        document.delete()
