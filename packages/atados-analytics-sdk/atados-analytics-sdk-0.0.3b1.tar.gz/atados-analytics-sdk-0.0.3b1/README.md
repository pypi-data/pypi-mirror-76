[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/leojaimesson/typescript-package-boilerplate/blob/master/LICENSE.md)
[![python badge](https://img.shields.io/badge/type-python-green.svg)](https://python.org/en/)

# SDK Oficial para Python

Está SDK é utilizada para enviar eventos à API de Analytics da Atados

## Instalando

```
pip install @atados/analytics-sdk
```

## Antes de começar, entenda a função track

```typescript
track(
  /**
   * Tipo: String
   * Use para categorizar esta acao
   * Ex.:
   *   category = 'Apply',
   *   category = 'Notification',
   */
  category: string,
  /**
   * Tipo: String
   * Use para identificar esta ação dentro da categoria
   * Ex.:
   *   label = 'Cancel Apply',
   *   label = 'View Notification',
   */
  label: string,
  /**
   * Use para enriquecer esta ação dentro da categoria
   * Ex.:
   *   action = ID de inscricao
   *   action = { notificationId, notificationKind }
   */
  action: any,
  /**
   * Use este argumento para sobrepor as configurações de userId
   * ou meta
   */
  user_id?: number,
  /**
   * Use este argumento para sobrepor as configurações de meta
   */
  override_meta?: {}
): Promise<void>
```

## Iniciando

```python
from Analytics from analytics

def report_error(error):
  print(error.message)

analytics = Analytics(
  api_url=API_URL,
  api_token=API_TOKEN,
  meta=mock_meta,
  on_error=report_error,
  meta={ 'channelId': 1 }
)
track_result = analytics.track(
  category='Category',
  label='Label',
  action={ 'data': 1 },
  # (Opcional)
  user_id=1,
  # (Opcional)
  sessoin_id=1
)
```

## Utilizando

```typescript
analytics.track('Category', 'Label', 'Action')
```
