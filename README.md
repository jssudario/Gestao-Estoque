# Projeto de Gestão de Estoques - API

**Sistemas de Informação – Desenvolvimento de Sistemas Web I**  

[VÍDEO EM FUNCIONAMENTO](https://www.youtube.com/watch?v=AhR_AQO6P4w)

**Aluno(a):** Julia Sudário Silva  
**RA:** 007217  

**Aluno(a):** Adryan Ryan Santos  
**RA:** 007194  

API desenvolvida em FastAPI para a gestão de produtos, categorias e controle de estoque, como parte da disciplina de Desenvolvimento de Sistemas WEB I. A aplicação permite o registro de movimentações de estoque, cálculo de saldo em tempo real e a implementação de operações de negócio como vendas e devoluções.

## Funcionalidades

* **Gestão de Produtos e Categorias:** CRUD completo para produtos e categorias.
* **Controle de Estoque:** Registro de movimentações de ENTRADA e SAÍDA.
* **Operações de Negócio:** Endpoints específicos para Venda, Devolução e Ajuste de estoque.
* **Cálculo de Saldo:** O saldo dos produtos é sempre calculado em tempo real a partir das movimentações, garantindo a consistência dos dados.
* **Relatórios:** Geração de extrato de movimentações por produto e um resumo geral do estado do estoque.
* **Validação de Estoque Mínimo:** Rota para listar produtos que estão com o saldo abaixo do estoque mínimo definido.

## Decisão sobre Saldo Negativo

Para garantir a integridade dos dados e simular um ambiente de negócio real, a decisão tomada para este projeto foi **não permitir saldo negativo em estoque**. Qualquer operação de SAÍDA (venda, ajuste, etc.) que resultaria em um saldo menor que zero é bloqueada pela API, que retorna uma mensagem de erro informando "Saldo insuficiente".

## Como Executar a Aplicação

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

* Python 3.8 ou superior
* Pip (gerenciador de pacotes do Python)

### Passos para Instalação

1.  **Clone o repositório** (ou baixe os arquivos para uma pasta em seu computador).

2.  **Crie e ative um ambiente virtual:**
    ```sh
    # Cria o ambiente virtual
    python -m venv venv

    # Ativa o ambiente (no Linux/macOS)
    source venv/bin/activate

    # Ativa o ambiente (no Windows)
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    Crie um arquivo chamado `requirements.txt` na raiz do projeto com o seguinte conteúdo:
    ```txt
    fastapi[all]
    sqlalchemy
    ```
    Em seguida, instale as dependências com o comando:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Execute o servidor:**
    A partir da pasta raiz do projeto (`projeto_02`), execute o Uvicorn:
    ```sh
    uvicorn app.main:app --reload
    ```
    O servidor estará rodando em `http://1227.0.0.1:8000`. O arquivo de banco de dados (`banco_de_dados.db`) será criado automaticamente no primeiro acesso.

5.  **Acesse a Documentação Interativa (Swagger UI):**
    Para ver e testar todos os endpoints, acesse `http://127.0.0.1:8000/docs` no seu navegador.

## Exemplos de Chamadas (venda, devolução, extrato, resumo)

A seguir estão exemplos de como usar os principais endpoints da API com a ferramenta `curl`.

### 1. Preparação (Crie uma categoria e um produto)

```sh
# Criar Categoria "Eletrônicos" (retorna id: 1)
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/categoria/](http://127.0.0.1:8000/api/v1/categoria/)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"nome": "Eletrônicos"}'

# Criar Produto "Celular" (retorna id: 1)
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/produtos](http://127.0.0.1:8000/api/v1/produtos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"nome": "Celular", "preco": 1800, "categoria_id": 1, "estoque_minimo": 10}'

# Dar entrada inicial de 50 unidades no estoque
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/estoque/movimentos](http://127.0.0.1:8000/api/v1/estoque/movimentos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"produto_id": 1, "quantidade": 50, "tipo": "ENTRADA", "motivo": "Pedido inicial"}'
```

### 2. Exemplos Solicitados

**• Registrar uma Venda (SAÍDA de 5 unidades)**
```sh
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/estoque/venda](http://127.0.0.1:8000/api/v1/estoque/venda)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"produto_id": 1, "quantidade": 5, "motivo": "Cliente 1"}'
```

**• Registrar uma Devolução (ENTRADA de 2 unidades)**
```sh
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/estoque/devolucao](http://127.0.0.1:8000/api/v1/estoque/devolucao)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"produto_id": 1, "quantidade": 2, "motivo": "Cliente devolveu produto"}'
```

**• Consultar o Extrato do produto**
```sh
curl -X 'GET' '[http://127.0.0.1:8000/api/v1/estoque/extrato/1](http://127.0.0.1:8000/api/v1/estoque/extrato/1)' \
-H 'accept: application/json'
```

**• Obter o Resumo do Estoque**
```sh
curl -X 'GET' '[http://127.0.0.1:8000/api/v1/estoque/resumo](http://127.0.0.1:8000/api/v1/estoque/resumo)' \
-H 'accept: application/json'
```
