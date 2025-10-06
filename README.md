# Projeto de Gestão de Estoques - API

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
    O servidor estará rodando em `http://127.0.0.1:8000`. O arquivo de banco de dados (`banco_de_dados.db`) será criado automaticamente no primeiro acesso.

5.  **Acesse a Documentação Interativa (Swagger UI):**
    Para ver e testar todos os endpoints, acesse `http://127.0.0.1:8000/docs` no seu navegador.

## Exemplos de Chamadas da API

A seguir estão exemplos de como usar os principais endpoints da API com a ferramenta `curl`.

### 1. Preparação (Crie a categoria e os produtos)

```sh
# Criar Categoria "Eletrônicos" (retorna id: 1)
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/categoria/](http://127.0.0.1:8000/api/v1/categoria/)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"nome": "Eletrônicos"}'

# Criar Produto "Televisão 50 polegadas" (retorna id: 1)
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/produtos](http://127.0.0.1:8000/api/v1/produtos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"nome": "Televisão 50 polegadas", "preco": 2500.00, "categoria_id": 1, "estoque_minimo": 5}'

# Dar entrada inicial de 20 unidades da Televisão no estoque
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/estoque/movimentos](http://127.0.0.1:8000/api/v1/estoque/movimentos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"produto_id": 1, "quantidade": 20, "tipo": "ENTRADA", "motivo": "Compra fornecedor"}'

# Criar Produto "Celular 256GB" (retorna id: 2)
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/produtos](http://127.0.0.1:8000/api/v1/produtos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"nome": "Celular 256GB", "preco": 1800.00, "categoria_id": 1, "estoque_minimo": 10}'

# Dar entrada inicial de 50 unidades do Celular no estoque
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/estoque/movimentos](http://127.0.0.1:8000/api/v1/estoque/movimentos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"produto_id": 2, "quantidade": 50, "tipo": "ENTRADA", "motivo": "Compra fornecedor"}'

# Criar Produto "Microondas 20L" (retorna id: 3)
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/produtos](http://127.0.0.1:8000/api/v1/produtos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"nome": "Microondas 20L", "preco": 450.00, "categoria_id": 1, "estoque_minimo": 8}'

# Dar entrada inicial de 30 unidades do Microondas no estoque
curl -X 'POST' '[http://127.0.0.1:8000/api/v1/estoque/movimentos](http://127.0.0.1:8000/api/v1/estoque/movimentos)' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"produto_id": 3, "quantidade": 30, "tipo": "ENTRADA", "motivo": "Compra fornecedor"}'
