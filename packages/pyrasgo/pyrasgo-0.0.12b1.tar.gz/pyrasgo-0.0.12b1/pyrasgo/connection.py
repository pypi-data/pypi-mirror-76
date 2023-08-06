import os
import requests
import amplitude
import pandas as pd
from snowflake import connector as snowflake
from snowflake.connector import SnowflakeConnection
from typing import List, Optional, Dict

from pyrasgo.feature_list import FeatureList


class RasgoConnection(object):
    """
    Base connection object to handle interactions with the Rasgo API.

    Defaults to using the production Rasgo instance, which can be overwritten
    by specifying the `RASGO_DOMAIN` environment variable, eg:

    &> RASGO_DOMAIN=custom.rasgoml.com python
    >>> from pyrasgo import RasgoConnection
    >>> rasgo = RasgoConnection(api_key='not_a_key')
    >>> rasgo._hostname == 'custom.rasgoml.com'
    True

    """

    def __init__(self, api_key):
        self._production_domain = "api.rasgoml.com"
        self._amplitude_key = "08836b1e33763119e01fc62c604a7ea8"
        self._user_id = None

        self._api_key = api_key
        self._hostname = os.environ.get("RAGSO_DOMAIN", self._production_domain)
        self._event_logger = amplitude.AmplitudeLogger(api_key=self._amplitude_key)
        if self._hostname != self._production_domain:
            self._event_logger.turn_off_logging()

    # TODO - Is this more appropriately called get_models?
    def get_lists(self) -> List[FeatureList]:
        """
        Retrieves the list of features list from Rasgo within the account specified by the API key.
        """
        self._note({'event_type': 'get_lists'})
        response = self._get("/models", {"join": ["features", "author"]})
        lists = response.json()
        return [FeatureList(entry) for entry in lists]

    def get_feature_list(self, list_id) -> FeatureList:
        """
        Retrieves the specified feature list from Rasgo within account specified by the API key.
        """
        self._note({'event_type': 'get_feature_list'})
        response = self._get("/models/{}".format(list_id), {"join": ["features", "author"]})
        entry = response.json()
        return FeatureList(entry)

    def get_feature_data(self, feature_list_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs the pandas dataframe for the specified feature list.

        :param feature_list_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        self._note({'event_type': 'get_feature_data'})
        feature_list = self.get_feature_list(feature_list_id)

        conn, creds = self._snowflake_connection(feature_list.author())

        table_metadata = feature_list.snowflake_table_metadata(creds)
        query, values = self._make_select_statement(table_metadata, filters, limit)

        result_set = self._run_query(conn, query, values)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    def get_user_id(self):
        """
        Gets the user id for the API key provided, or None if not available.
        NOTE: This is used for monitoring/logging purposes.
        """
        if self._user_id:
            return self._user_id
        else:
            response = self._get("/users")
            try:
                response_body = response.json()
                user = response_body['data']
                self._user_id = user.get('id')
                return self._user_id
            except Exception:
                # TODO: Split out Exceptions for error-handling?
                return None

    def _get(self, resource, params=None) -> requests.Response:
        """
        Performs GET request to Rasgo API as defined within the class instance.

        :param resource: Target resource to GET from API.
        :param params: Additional parameters to specify for GET request.
        :return: Response object containing content returned.
        """
        response = requests.get(self._url(resource),
                                headers=self._headers(self._api_key),
                                params=params or {})
        response.raise_for_status()
        return response

    def _note(self, event_dict: dict) -> None:
        """
        Emit event to monitoring service.
        :param event_dict: Dictionary containing desired attributes to emit.
        :return:
        """
        event_dict['user_id'] = self.get_user_id()  # TODO: move user_id call to __init__ to cache the user id.
        event_dict['source'] = 'pyrasgo'
        event = self._event_logger.create_event(**event_dict)
        self._event_logger.log_event(event)

    def _url(self, resource):
        if '/' == resource[0]:
            resource = resource[1:]
        return f'https://{self._hostname}/{resource}'

    @staticmethod
    def _snowflake_connection(member) -> (SnowflakeConnection, dict):
        """
        Constructs connection object for Snowflake data platform
        :param member: credentials for Snowflake data platform

        :return: Connection object to use for query execution
        """
        creds = member.snowflake_creds()
        conn = snowflake.connect(**creds)
        return conn, creds

    @staticmethod
    def _make_select_statement(table_metadata, filters, limit) -> tuple:
        """
        Constructs select * query for table
        """
        query = "SELECT * FROM {database}.{schema}.{table}".format(**table_metadata)
        values = []
        if filters:
            comparisons = []
            for k, v in filters.items():
                comparisons.append("{}=%s".format(k))
                values.append(v)
            query += " WHERE " + " and ".join(comparisons)
        if limit:
            query += " limit {}".format(limit)
        return query, values

    @staticmethod
    def _run_query(conn, query: str, params):
        """
        Execute a query on the [cloud] data platform.

        :param conn: TODO -> abstract the cloud data platform connection
        :param query: String to be executed on the data platform
        :return:
        """
        return conn.cursor().execute(query, params)

    @staticmethod
    def _headers(api_key) -> dict:
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
