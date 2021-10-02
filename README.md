# edc-airflow-spark-on-k8s-gke
Engenharia de Dados em Cloud - ETL - Airflow e Spark Operator no Kubernetes - Google Kubernetes Engine
## Objetivo:
Este projeto tem como objetivo documentar de forma didática as etapas necessárias para criar de um Cluster Kubernetes ("**k8s**") e realizar o *deploy* do *Airflow* e *Spark-Operator* neste mesmo cluster. Disponibilizando assim uma ambiente escalavel para processamento de dados e orquestração de pipelines, sendo plenamente aplicavél em um contexto de *Big Data*. 

<br>

Links de referência deste projeto:
- "edc-igti-terraform-ias-mod1"
    - https://github.com/smedina1304/edc-igti-terraform-ias-mod1
        <br>
        *Forked from:* [neylsoncrepalde/edc-mod1-exercise-igti](https://github.com/neylsoncrepalde/edc-mod1-exercise-igti)<br>
        ![GitHub forks](https://img.shields.io/github/forks/neylsoncrepalde/edc-mod1-exercise-igti?style=social)
        <br>
- "edc-igti-kafka-k8s-mod2"
    - https://github.com/smedina1304/edc-igti-kafka-k8s-mod2
        <br>
        *Forked from:* [carlosbpy/igti-k8s-exercise](https://github.com/carlosbpy/igti-k8s-exercise)<br>
        ![GitHub forks](https://img.shields.io/github/forks/carlosbpy/igti-k8s-exercise?style=social)
        <br>
- "edc-igti-spark-mod3"
    - https://github.com/smedina1304/edc-igti-spark-mod3
        <br>
        *Forked from:* [pltoledo/dad-mod2-igti](https://github.com/pltoledo/dad-mod2-igti)<br>
        ![GitHub forks](https://img.shields.io/github/forks/pltoledo/dad-mod2-igti?style=social)
        <br>
- "edc-igti-kubernetes-mod4"
    - https://github.com/smedina1304/edc-igti-kubernetes-mod4
        <br>
        *Forked from:* [neylsoncrepalde/edc_mod4_exercise_igti](https://github.com/neylsoncrepalde/edc_mod4_exercise_igti)<br>
        ![GitHub forks](https://img.shields.io/github/forks/neylsoncrepalde/edc_mod4_exercise_igti?style=social)
        <br>
- "edc-etl-dags-prefect-io"
    - https://github.com/smedina1304/edc-etl-dags-prefect-io
        <br>
        ![GitHub stars](https://img.shields.io/github/stars/smedina1304/edc-etl-dags-prefect-io?style=social)
<br>




## Preparação do ambiente Python de desenvolvimento:

- Versão da Linguagem Python 3.8 ou superior deve estar instalada.
    <br>
    ```shell
    > python --version
        Python 3.8.2
    ```
    <br>

    :point_right: *Atenção: verificar se o seu python versão 3 está respondendo com o comando **python** ou **python3**.*
    <br>

- Clonar o repositório deste projeto na sua máquina de desenvolvimento, para esta ação via linha de comando selecione a pasta que recebera o projeto e execute o comando `git`, caso prefeira outro procedimento esta ação é livre:
    <br>

    ```shell
    > git clone https://github.com/smedina1304/edc-airflow-spark-on-k8s.git
    ```
    <br>

    :point_right: *Verificar se após o comando a criação da pasta `edc-airflow-spark-on-k8s` foi realizada corretamente.*


- Criando o ambiente virtual Python **`venv`**, para isolar e controlar o versionamento de pacotes a ser utilizado. A criação do ambiente virtual deve ser realizado na pasta *root* do projeto.
    <br>

    ```shell
    > python -m venv venv
    ```
    <br>

- Para ativar o ambiente **`venv`**:
    <br>

    - Linux e Mac:
    ```shell
    > source .venv/bin/activate
    ```    
    <br>

    - Windows:
        <br>

        - No Windows via Powershell utilizar "`activate.bat`".
        <br>

        ```shell
        > .\venv\Scripts\Activate.ps1
        ```
        <br>

        - No Windows via CMD utilizar "`activate.bat`".
        <br>

        ```shell
        > .\venv\Scripts\activate.bat
        ```
    <br>
        
    :point_right: *Atenção: Para verificar que está funcionando e o ambiente foi ativado, deve aparecer o nome do ambiente destacado com prefixo do seu prompt de comandos.*
    <br>
    - Conforme abaixo:
    <br>

    ```shell
    (venv)
    ```
    <br>


- Para desativar o ambiente **`venv`**:
    <br>

    ```shell
    > deactivate
    ```
    <br>

    :point_right: *Atenção: Este comando deve ser usado apenas quando não mais for necessário execução de códigos python no ambiente virtual.*
    <br>

- Instalação de pacotes requeridos para o projeto, para isso pode ser verificado o arquivo `requirements.txt` na pasta `root` do projeto.
    <br>

    Passo opcional para atualização do `pip` no ambiente **`venv`**:

    ```shell
    > pip install --upgrade pip
    ```
    <br>

    Passo de instalação dos pacotes via arquivo *`requirements.txt`*:
    ```shell
    > pip install -r requirements.txt
    ```
    <br>

    :point_right: *Obervação: todos os pacotes necessário para executar os pipelines (DAGs) deste projeto estão contidas  no arquivo em `requirements.txt`.*
    <br>
    <br>

## Criação do Cluster Kubernetes (k8s) em Cloud:

- Google Cloud.

    - Instalar o Google Cloud SDK Command Line (CLI), seguir as instruções da página conforme o sistema operaiconal desejado:
        <br>
        https://cloud.google.com/sdk/docs/quickstart
        <br>
        :point_right: *Importante: realize todos os passos de preparação do ambiente Google Cloud SDK conforme a pagina Quickstart.*
        <br> 

    - Após instalação verificar a versão do `gcloud`, conforme instruções e o instalador que foi baixado:
        <br>
        ```shell
        > gcloud --version
        Google Cloud SDK 358.0.0
        bq 2.0.71
        core 2021.09.17
        gsutil 4.68
        ```

    