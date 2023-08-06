import requests
import json
from .errors import AnalyticsGraphQLError, AnalyticsError

GQL_TRACK_QUERY = """
	mutation js_sdk_track(
		$category: String!
		$label: String!
		$action: jsonb!
		$meta: jsonb!
		$userId: String
		$sessionId: bigint
	) {
		insert_Event(
			objects: {
				category: $category
				label: $label
				action: $action
				meta: $meta
				userId: $userId
				sessionId: $sessionId
			}
		) {
			affected_rows
		}
	}
"""


class Analytics:
  """SDK de Analytics para trackear eventos

    Args:
        api_url (String): A URL de API que o está hospedado servidor GraphQL de Analytics
        api_token (String): O Token de API gerado para acessar a API
        meta (Dict): Os metadados enviados para API
        on_error ((error: AnalyticsError | AnalyticsGraphQLError) -> void): Callback para
          acessar os erros
        log_events (Boolean): Use para categorizar o evento
        session_id (Int): Use para categorizar o evento
  """
  def __init__(self,
               api_url,
               api_token,
               meta,
               on_error=None,
               log_events=False,
               session_id=None):
    self.api_url = api_url
    self.api_token = api_token
    self.meta = meta
    self.on_error = on_error
    self.log_events = log_events
    self.session_id = session_id

  def track(self,
            category,
            label,
            action,
            override_meta=None,
            user_id=None,
            session_id=None):
    """Envie um evento para a API de analytics

    Args:
        category (String): Use para categorizar o evento
        label (String): Use para identificar o evento
        action (any): Use para enriquecer o evento
    """
    userId = user_id

    # Sobrepõe os dados metada enviados à API para esta request
    meta = {} if override_meta else self.meta
    if override_meta:
      meta.update(self.meta).update(override_meta)

    payload = {
        "query": GQL_TRACK_QUERY,
        "variables": {
            "category": category,
            "label": label,
            "action": action,
            "meta": meta,
            "userId": userId,
            "sessionId": session_id
        }
    }
    headers = {
        'content-type': 'application/json',
        "authorization": "Bearer " + self.api_token
    }
    res = requests.post(self.api_url, data=json.dumps(payload), headers=headers)
    res_json = res.json()

    if 'errors' in res_json:
      if self.on_error is not None:
        self.on_error(AnalyticsGraphQLError(res_json['errors'][0]['message']))

      # Vamos retornar False para mostrar que o evento não foi trackeado
      return False

    if not 'data' in res_json:
      if self.on_error is not None:
        self.on_error(AnalyticsError('No data was returned'))

      # Vamos retornar False para mostrar que o evento não foi trackeado
      return False

    return True
