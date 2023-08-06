class AnalyticsError(Exception):
  """Classe base para erros de analyitcs
  """
  pass


class AnalyticsGraphQLError(AnalyticsError):
  """É usado quando algum erro de resposta do servidor GraphQL é encontrado
  """
  pass
