Por favor, primeiro leia o arquivo Relatório de Análise e ações toamdas.txt

Este README fornece os comandos básicos para executar o projeto utilizando Docker Compose.

## Pré-requisitos

* Docker instalado na sua máquina.
* Docker Compose instalado na sua máquina.

## Execução

1.  **Navegue até o diretório raiz do projeto (onde o arquivo `docker-compose.yml` está localizado).**

    ```bash
    cd /caminho/para/o/seu/projeto/docker
    ```

2.  **Construa e inicie os containers Docker:**

    ```bash
    docker-compose up -d
    ```

    O parâmetro `-d` executa os containers em segundo plano.

3.  **Acesse a API:**

    A API estará disponível em `http://localhost:8000`.

4.  **Verificar os logs da API (opcional):**

    Para acompanhar os logs da API, você pode usar o seguinte comando:

    ```bash
    docker logs -f $(docker ps --filter name=api --format "{{.Names}}")
    ```

5.  **Parar e remover os containers:**

    Para parar e remover os containers quando terminar, execute:

    ```bash
    docker-compose down
    ```

## Próximos Passos (Para Desenvolvimento)

* Para reconstruir a imagem da API após alterações no código:

    ```bash
    docker-compose build --no-cache api
    ```

* Lembre-se de reiniciar os containers (`docker-compose up -d`) após reconstruir a imagem.
