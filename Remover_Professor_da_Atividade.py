import requests

AMBIENTE = "uat"   # "uat" ou "prod"

BASE_URLS = {
    "uat":  "https://api-uat.grupomarista.org.br/public/es/docente/v1",
    "prod": "https://api.grupomarista.org.br/public/es/docente/v1",
}

TOKEN = "SEU_TOKEN_AQUI"

def removeAtividade():

    BD_Remocao = [
        {"P": "645", "A": "124"},
        {"P": "816", "A": "124"},
        # ... adicione aqui os pares professor/atividade a serem removidos
    ]

    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {TOKEN}",
        "cache-control": "no-cache",
        "dnt": "1",
        "expires": "0",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://agendadocente.pucpr.br/",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Content-Type": "application/json"
    }

    ultimo_processado = {"P": None, "A": None}
    erros = []

    for professor in BD_Remocao:
        id_professor = professor["P"]
        id_atividades = professor["A"]
        ultimo_processado["P"] = id_professor
        ultimo_processado["A"] = id_atividades

        try:
            url = f'{BASE_URLS[AMBIENTE]}/atividades-docentes/{id_atividades}/vinculo-docente'
            response = requests.put(
                url,
                headers=HEADERS,
                json={"adicionados": [], "removidos": [id_professor]},
                timeout=15
            )
            if response.status_code in (200, 204):
                print(f"Sucesso: Professor {id_professor} removido da atividade {id_atividades}.")
            else:
                print(f"Erro ao remover Professor {id_professor} da atividade {id_atividades}: status={response.status_code}")
                erros.append({"P": id_professor, "A": id_atividades, "status": response.status_code, "erro": response.content})
        except Exception as e:
            print(f"Erro ao remover Professor {id_professor} da atividade {id_atividades}: {e}")
            erros.append({"P": id_professor, "A": id_atividades, "status": None, "erro": str(e)})

    print(f"\nProcessamento concluído. Último processado: {ultimo_processado}")
    if erros:
        print(f"\nTotal de erros: {len(erros)}")
        for e in erros:
            print(e)

# Chame a função
removeAtividade()