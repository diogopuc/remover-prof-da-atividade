# remove_atividade.py

Script para remover professores de atividades docentes na plataforma **Agenda Docente**, via chamada direta à API do Grupo Marista.

## O que o script faz

Para cada par professor/atividade informado, envia uma requisição `PUT` ao endpoint de vínculo, removendo o professor da atividade. O endpoint usado é o mesmo disparado pela interface ao clicar em "Salvar" na tela de Associação de Atividade — o script apenas reproduz essa chamada diretamente, sem passar pela UI.

## Endpoint

```
PUT {BASE_URL}/atividades-docentes/{id_atividades}/vinculo-docente
```

Body enviado (formato diff, não a lista completa):

```json
{
  "adicionados": [],
  "removidos": ["<id_professor>"]
}
```

## Configuração

Antes de rodar, edite as constantes no topo do arquivo:

| Variável | Descrição |
|---|---|
| `BD_Remocao` | Lista de dicionários `{"P": id_professor, "A": id_atividade}` a serem removidos. `P` e `A` usam os IDs internos da API, não os IDs exibidos na UI. |
| `AMBIENTE` | `"uat"` ou `"prod"` — define qual URL base será usada. |
| `TOKEN` | Token JWT (Bearer) do usuário autenticado no ambiente escolhido. |

`BASE_URLS` mapeia cada ambiente para sua respectiva URL da API e normalmente não precisa ser alterado.

## Como obter o TOKEN

O token é o JWT usado pela sessão autenticada no Agenda Docente. Pode ser capturado inspecionando o header `Authorization` de uma requisição autenticada feita pela própria aplicação (DevTools → aba Network).

⚠️ O token expira periodicamente — se o script retornar erro 401, gere um novo.

## Execução

```bash
python remove_atividade.py
```

O script roda de forma **sequencial** (uma requisição por vez). Para cada item de `BD_Remocao`:

1. Monta a URL com o `id_atividades`.
2. Envia o `PUT` com o `id_professor` em `removidos`.
3. Imprime sucesso (`200`/`204`) ou erro no console.

Ao final, exibe:
- O último par processado (`ultimo_processado`), útil para saber de onde retomar em caso de interrupção.
- Um resumo com todos os erros ocorridos, se houver.

## Tratamento de erros

Cada requisição é isolada em um `try/except`: se uma falhar (erro de rede, timeout, status diferente de 200/204), o script registra o erro e **continua** para o próximo item da lista, em vez de interromper toda a execução.

## Observações importantes

- **IDs da UI ≠ IDs da API.** Os IDs exibidos na tela do Agenda Docente não são os mesmos usados pela API — sempre confirme os IDs internos antes de popular `BD_Remocao`.
- **Não versionar o token.** Nunca commitar o `TOKEN` preenchido no controle de versão; mantenha o placeholder no repositório e preencha localmente antes de rodar.
- **Teste em UAT antes de rodar em produção.** Recomenda-se validar a lista completa em `AMBIENTE = "uat"` antes de trocar para `"prod"`.