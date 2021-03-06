# edc-airflow-spark-on-k8s
Engenharia de Dados em Cloud - ETL - Airflow e Spark Operator no Kubernetes - Google Kubernetes Engine
## Objetivo:
Este projeto tem como objetivo documentar de forma didática as etapas necessárias para criar de um Cluster Kubernetes ("**k8s**") e realizar o *deploy* do *Airflow* e *Spark-Operator* neste mesmo cluster. Disponibilizando assim um ambiente escalavel para processamento de dados e orquestração de pipelines, sendo plenamente aplicavél em um contexto de *Big Data*. 
<br>
Este tutorial foi gerado com base no ambiente do GCP, porem nos links abaixo existem várias referências de uso na AWS. Alguns pontos deste projeto também será referenciado o ações para o ambiente AWS.

<br>

Links de referência deste projeto:

- "GoogleCloudPlatform/spark-on-k8s-operator"
    - https://github.com/GoogleCloudPlatform/spark-on-k8s-operator
        <br>
        *Officially supported Google product:*<br>
        ![GitHub forks](https://img.shields.io/github/forks/GoogleCloudPlatform/spark-on-k8s-operator?style=social)        
        <br>

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




## Preparação do ambiente Python:

- Versão da Linguagem Python 3.8 ou superior deve estar instalada.
    
    ```shell
    python --version
    ```

    *Output:*
    ```console
    Python 3.8.2
    ```
    <br>

    :point_right: *Atenção: verificar se o seu python versão 3 está respondendo com o comando **python** ou **python3**.*
    <br>

- Clonar o repositório deste projeto na sua máquina de desenvolvimento, para esta ação via linha de comando selecione a pasta que recebera o projeto e execute o comando `git`, caso prefeira outro procedimento esta ação é livre:

    ```shell
    git clone https://github.com/smedina1304/edc-airflow-spark-on-k8s.git
    ```
    <br>

    :point_right: *Verificar se após o comando a criação da pasta `edc-airflow-spark-on-k8s` foi realizada corretamente.*


- Criando o ambiente virtual Python **`venv`**, para isolar e controlar o versionamento de pacotes a ser utilizado. A criação do ambiente virtual deve ser realizado na pasta *root* do projeto.

    ```shell
    python -m venv venv
    ```
    <br>

- Para ativar o ambiente **`venv`**:

    - Linux e Mac:
    ```shell
    source ./venv/bin/activate
    ```    
    <br>

    - Windows:
        <br>

        - No Windows via Powershell utilizar "`activate.bat`".

        ```shell
        .\venv\Scripts\Activate.ps1
        ```
        <br>

        - No Windows via CMD utilizar "`activate.bat`".

        ```shell
        .\venv\Scripts\activate.bat
        ```
    <br>
        
    :point_right: *Atenção: Para verificar que está funcionando e o ambiente foi ativado, deve aparecer o nome do ambiente destacado com prefixo do seu prompt de comandos.*
    <br>
    - Conforme abaixo:

    ```shell
    (venv)
    ```
    <br>


- Para desativar o ambiente **`venv`**:

    ```shell
    deactivate
    ```
    <br>

    :point_right: *Atenção: Este comando deve ser usado apenas quando não mais for necessário execução de códigos python no ambiente virtual.*
    <br>

- Instalação de pacotes requeridos para o projeto, para isso pode ser verificado o arquivo `requirements.txt` na pasta `root` do projeto.
    <br>

    Passo opcional para atualização do `pip` no ambiente **`venv`**:

    ```shell
    pip install --upgrade pip
    ```
    <br>

    Passo de instalação dos pacotes via arquivo *`requirements.txt`*:

    ```shell
    pip install -r requirements.txt
    ```
    <br>

    :point_right: *Obervação: todos os pacotes necessário para executar os pipelines (DAGs) deste projeto estão contidas  no arquivo em `requirements.txt`.*
    <br>

    :point_right: *Atenção: Para ambientes MacOS e para algumas distribuições Linux, mediante a plataforma de Hardware como processador Intel 64bits, pode ser necessário a definição da variavel de ambiente `ARCHFLAGS="-arch x86_64"`. Caso durante a instalação de Pacotes no Python e retornando algum erro, verifique a necessidade de declarar a variavel de ambiente para definição da arquitetura do processador.*

    Definir a variável de ambiente para Mac ou Linux:

    ```shell
    export ARCHFLAGS="-arch x86_64"
    ```

    Para fazer a instalação do airflow de forma isolada execute o comando:

    ```shell
    pip install apache-airflow
    ```

    ou pela documentação do pip (https://pypi.org/project/apache-airflow/).

    ```shell
    pip install apache-airflow==2.1.4 \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.1.4/constraints-3.7.txt"
    ```
    <br>

## Requisitos de ferramentas CLI (Command line):
<br>

A utilização de ferramentas via CLI (*"command line"*) é importante pois podemos definir os scripts de criação, preparação de deploy em nosso ambiente k8s, deixando o mesmo facilmente de ser replicavel em outra estrutura se necessário, e até mesmo em um caso de um acelerador para um "disaster recovery".
<br>

- Recursos indicados:
    <br>

    - Ambiente AWS, seguir as instruções da página conforme o sistema operaiconal desejado:
        - AWS CLI version 2 - https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html 
        <br>

    - Ambiente GCP, seguir as instruções da página conforme o sistema operaiconal desejado:
        - Google Cloud SDK Command Line (CLI) - https://cloud.google.com/sdk/docs/quickstart
        <br>
        :point_right: *Importante: realize todos os passos de preparação do ambiente Google Cloud SDK conforme a página Quickstart.*
        <br>     

   - EKS para interação com o cluster Kubernetes - eksctl - https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html
      - Também deve ser verificado de juntamente com o eksctl foi instalando kubectl, caso contrário verificar o procedimento em: https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
      <br>

   - HELM - repositório de pacotes para deploy no k8s - https://helm.sh/docs/intro/install/
    <br>

   - kubectx - para alterar o contexto o cluster k8s, em caso de haver mais de uma referência na máquina utilizada para operação - https://github.com/ahmetb/kubectx
    <br>

- Verificar as instalações AWS CLI:

    ``` shell
    aws --version
    ```

    *Output:*
    ```console
    aws-cli/2.2.31 Python/3.8.8 Darwin/19.6.0 exe/x86_64 prompt/off
    ```
    <br>

- Verificar as instalações GCP CLI:

    ```shell
    gcloud --version
    ```

    *Output:*
    ```console
    Google Cloud SDK 358.0.0
    bq 2.0.71
    core 2021.09.17
    gsutil 4.68
    ```
    <br>

- Verificar as instalações EKSCTL:

    ```shell
    eksctl version
    ```

    *Output:*
    ```console
    0.63.0
    ```
    <br>

- Verificar as instalações EKSCTL:

    ```shell
    kubectl version
    ```

    *Output:*
    ```console    
    Client Version: version.Info{Major:"1", Minor:"22", GitVersion:"v1.22.1", GitCommit:"632ed300f2c34f6d6d15ca4cef3d3c7073412212", GitTreeState:"clean", BuildDate:"2021-08-19T15:38:26Z", GoVersion:"go1.16.6", Compiler:"gc", Platform:"darwin/amd64"}
    ```
    <br>

- Verificar as instalações HELM:

    ```shell
    helm version
    ```

    *Output:*
    ```console    
    version.BuildInfo{Version:"v3.6.3", GitCommit:"d506314abfb5d21419df8c7e7e68012379db2354", GitTreeState:"dirty", GoVersion:"go1.16.6"}
   ```

<br>

:point_right: *Importante: verifique todos os passos de configuração das ferramentas CLI referentes a interação com a AWS e GCP, pois cada uma tem seu padrão de autenticação.*
<br>
<br>


## Criação do Cluster Kubernetes (k8s) em Cloud:

- Google Cloud - GCP.

    - Após instalação do `gcloud`, conforme instruções e o instalador que foi baixado verifique as informações de configuração antes de iniciar a criação do cluster:

        ```shell
        gcloud config list             
        ```

        *Output:*
        ```console
        [compute]
        region = us-east1
        zone = us-east1-c
        [core]
        account = sergio.medina
        disable_usage_reporting = True
        project = edc-igti-smedina
        ```

    - Criação do Cluster, antes realize as verificações e configurações, estando *"ok"* pode ser executado o exemplo abaixo:
        <br>

        *Sintaxe: `https://cloud.google.com/sdk/gcloud/reference/beta/container/clusters/create`*
        <br>
        Para os testes deste projeto foi utilizado o parametro `--preemptible` para alocação de instâncias do Compute Engine que duram até 24 horas e não oferecem garantias de disponibilidade, mas são mais baratas.
        <br>
        Também foram utilizadas durante os testes dois tipos de maquinas `e2-standard-2` e `e2-standard-4`, é necessário avalidar durante o processo mediante ao volume de dados e capacidade de processamento a configuração mais adequada.
        <br>

        ```shell

        gcloud /
        beta container --project "edc-igti-smedina" /
        clusters create "cluster-smedina-k8s" --zone "us-east1-c" /
        --no-enable-basic-auth --cluster-version "1.20.9-gke.1001" /
        --release-channel "regular" --machine-type "e2-standard-2" /
        --image-type "COS_CONTAINERD" --disk-type "pd-standard" /
        --disk-size "100" --node-labels ies=igti,curso=edc /
        --metadata disable-legacy-endpoints=true /
        --scopes "https://www.googleapis.com/auth/compute",/
        "https://www.googleapis.com/auth/devstorage.full_control",/
        "https://www.googleapis.com/auth/taskqueue",/
        "https://www.googleapis.com/auth/bigquery",/
        "https://www.googleapis.com/auth/logging.write",/
        "https://www.googleapis.com/auth/monitoring",/
        "https://www.googleapis.com/auth/servicecontrol",/
        "https://www.googleapis.com/auth/service.management.readonly",/
        "https://www.googleapis.com/auth/trace.append" /
        --max-pods-per-node "110" --preemptible --num-nodes "4" /
        --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM /
        --enable-ip-alias --network "projects/edc-igti-smedina/global/networks/default" /
        --subnetwork "projects/edc-igti-smedina/regions/us-east1/subnetworks/default" /
        --no-enable-intra-node-visibility --default-max-pods-per-node "110" /
        --enable-autoscaling --min-nodes "4" --max-nodes "6" /
        --no-enable-master-authorized-networks /
        --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver /
        --enable-autoupgrade --enable-autorepair /
        --max-surge-upgrade 1 /
        --max-unavailable-upgrade 0 /
        --enable-shielded-nodes /
        --node-locations "us-east1-c"

        ```
        *Script: `step-1-cluster/cluster_create.sh`*
        <br>

        Abaixo as telas do Console do GPC com as mesmas configurações do comando acima:
        <br>
        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-01.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-02.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-03.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-04.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-05.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-06.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-07.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-08.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-09.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-10.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-11.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-12.png" width="600" style="max-width: 600px;">
        </p>
        <br>

        <p align="left">
            <img src="docs/images/cluster-k8s-gke-config-13.png" width="600" style="max-width: 600px;">
        </p>
        <br>
        <br>

    - Após a confirmação de termino e criação do cluster k8s, verifique o registro do contexto de acesso e realize uma verificação nos nodes do cluster.
    <br>
    
    Verificando o contexto de acesso.

    ```shell
    kubectx
    ```

    *Output:*
    ```console
    gke_edc-igti-smedina_us-east1-c_cluster-smedina-k8s
    ```

    <br>
    Listando nos Nodes dos Cluster.

    ```shell
    kubectl get nodes
    ```

    *Output:*
    ```console
    NAME                                                 STATUS   ROLES    AGE    VERSION
    gke-cluster-smedina-k8s-default-pool-0bde709b-0vq6   Ready    <none>   5m8s   v1.20.9-gke.1001
    gke-cluster-smedina-k8s-default-pool-0bde709b-2fb6   Ready    <none>   5m8s   v1.20.9-gke.1001
    gke-cluster-smedina-k8s-default-pool-0bde709b-dzt2   Ready    <none>   5m9s   v1.20.9-gke.1001
    gke-cluster-smedina-k8s-default-pool-0bde709b-ksgh   Ready    <none>   5m9s   v1.20.9-gke.1001
    gke-cluster-smedina-k8s-default-pool-0bde709b-vfvh   Ready    <none>   5m8s   v1.20.9-gke.1001
    gke-cluster-smedina-k8s-default-pool-0bde709b-vtvk   Ready    <none>   5m9s   v1.20.9-gke.1001
    ```

    <br>
    
    :point_right: *Atenção: se for necessário deletar o cluster utilize comando abaixo, ou busque uma referência na sintaxe para atender a necessidade.*
    <br>

    *Sintaxe: `https://cloud.google.com/sdk/gcloud/reference/container/clusters/delete`*
    <br>

    ```shell
    gcloud container clusters delete "cluster-smedina-k8s"
    ```

    *Output:*
    ```console
    gcloud container clusters delete "cluster-smedina-k8s"
    The following clusters will be deleted.
    - [cluster-smedina-k8s] in [us-east1-c]

    Do you want to continue (Y/n)?  Y

    Deleting cluster cluster-smedina-k8s...done. 
    ```
    :point_right: *Importante: Confirme a DELEÇÃO com [Enter] ou [Y].*

    <br>
    <br>

## Preparação e Deploy do Spark Operator no k8s:

Para executar jobs spark no k8s estaremos utilizando uma imagem do Spark (base gcr.io/spark-operator/spark-py:v3.0.0), e para definir os cada job spark com recursos `sparkapplication` no k8s iremos utilizar uma imagem `Helm` que pode ser localizada no link abaixo:
<br>
Helm Chart for Spark Operator:
https://googlecloudplatform.github.io/spark-on-k8s-operator
<br>

1. Criação do namespace `sparkoperator`,caso não exista em seu cluster k8s.
    <br>
    Para verificar os namespaces existentes utilize o comando abaixo e verifique na lista retornada:

    ```shell
    kubectl get namespaces
    ```
    
    <br>

    Para criar o namespace *`sparkoperator`*:

    ```shell
    kubectl create namespace sparkoperator
    ```
    <br>

2. Atualização a imagem chart do *`spark-operator`* no repositório *`helm repo`* local antes do deploy no k8s.
    <br>
    Para incluir a imagem chart do `spark-operator` localmente, execute este comando:

    ```shell
    helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
    ```

    <br>
    Se já houver a imagem do chart do `spark-operator` baixada anteriormente, execute a atualização do repositório para garantir que está com a versão mais atualizada.
    
    ```shell
    helm repo update
    ```

    <br>

3. Criação Service Account `spark` no `k8s` como requisito de deploy `spark-operator`.
    <br>
    Para gerar o Service Account executar o comando abaixo:
    
    ```shell
    kubectl create serviceaccount spark -n sparkoperator
    ```
    <br>

4. Criação Role Binding `spark` no `k8s` como requisito de deploy `spark-operator`.
    <br>
    Para gerar o Service Account executar o comando abaixo:
    
    ```shell
    kubectl create clusterrolebinding spark-role-binding --clusterrole=edit --serviceaccount=sparkoperator:spark -n sparkoperator
    ```
    <br>

5. Delpoy do Spark Operator no Cluster k8s.

    Após as preparações anteriores finalizadas executar o seguinte comando:

    ```shell
    helm install spark spark-operator/spark-operator -n sparkoperator --debug
    ```
    <br>

    :point_right: *Atenção: Sendo necessário desistalar o airflow por qualquer motivos, utilize o comando abaixo ou busque uma referência do mesmo para atendimento da necessidade:*

    ```shell
    helm uninstall spark -n sparkoperator --debug
    ```

    Após uma soliciatação de desinstalação sempre verifique se os recursos foram liberados.
    <br>
    <br>

6. Preparação da imagem Docker para executar os jobs spark como recurso do tipo `sparkapplication`.
    <br>
    Na pasta `step-2-spark` existem dois arquivos *Dockerfile*, um que copia arquivos *jars* compativeis com a versão do spark e recursos dos provedores com a GCP e AWS.
    <br>
    Basicamente para gerar o build das imagens foi utilizado os comandos abaixo:
    <br>

    GCP - Spark 3.1.1

    ```shell
    docker build -t smedina1304/spark-operator:3.1.1-gcp -f Dockerfile_gcp .
    ```

    AWS - Spark 3.0.0
    
    ```shell
    docker build -t smedina1304/spark-operator:3.0.0-aws -f Dockerfile_aws .
    ```


    Ambas as imagems estão disponiveis no Docker Hub:
    https://hub.docker.com/r/smedina1304/spark-operator

    <br>

    Caso tenha a preferência de buscar mais detalhes para gerar uma image spark paro o k8s, utilize o link como referência: https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/user-guide.md#writing-a-sparkapplication-spec

    <br>

6. Criando uma `Secret` com as credenciais para acesso aos buckets do Data Lake.

    GCP - Credenciais de acesso via Arquivo JSON:
    <br>

    Carregando o conteúdo o arquivo com as chaves de acesso na `Secret`:
    
    ```shell
    kubectl create secret generic gcp-credentials-key --from-file=key.json=/path-file-service-account-gcp.json -n sparkoperator
    ```
    <br>

    Para verificar se a `Secret` foi criada corretamente, utilize o comando abaixo:
    <br>

    ```shell
    kubectl describe secret gcp-credentials -n sparkoperator
    ```

    *Output:*<br>
    *Observe que o conteúdo não será exposto*.
    ```console
    Name:         gcp-credentials-key
    Namespace:    sparkoperator
    Labels:       <none>
    Annotations:  <none>

    Type:  Opaque

    Data
    ====
    key.json:  2323 bytes        
    ```
    <br>

7. Executando uma Job com o recurso do Spark Operator no `k8s` para validação do ambiente.
    <br>
    Existe uma job-spark na pasta `./step-2-spark/job-spark-test`, então nesta pasta executar o comando abaixo para criar o `POD` para executar o processo.
    <br>
    ```shell
    kubectl apply -f job-spark-processing-titanic.yaml -n sparkoperator
    ```

    *Output:*
    ```console
    sparkapplication.sparkoperator.k8s.io/job-pyspark-processing-titanic created
    ```

    Esta mensagem indica que o `POD` driver foi criado, e irá disparar os executores de processamento spark conforme a configuração do arquivo `yaml`. Para detalhamento dos parametros utilizados consultar no link da documentação:<br>
    https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/user-guide.md


    <br>

    Para acompanhar o processoamento é necessário verificar os status dos `PODs`.

    ```shell
    kubectl get pods -n sparkoperator
    ```

    Após o comando `apply` e em caso de erro no processamento.

    *Output: [simulação de erro]*
    ```console
    NAME                                    READY   STATUS    RESTARTS   AGE
    job-pyspark-processing-titanic-driver   0/1     Error     0          83s
    spark-spark-operator-59c685545-84nq9    1/1     Running   0          23m
    ```

    :point_right: *Atenção: No caso assima temos uma exemplo de erro que pode ser verificado via a `log`, e consultar o log deve ser utilizado o comando abaixo.*

    ```shell
    kubectl logs job-pyspark-processing-titanic-driver -n sparkoperator
    ```

    *O Erro deve ser verificado e direcionado para seguir com o teste e validação do ambiente.*

    <br>

    :point_right: *Atenção: Para executar novamente o `job-spark-processing-titanic` após o erro ou execução anterior é necessário excluir o `POD`, pois não é prossível reprocessar ou reexecutar `PODs` com o mesmo nome, mesmos que já finalizados.*

    ```shell
    kubectl delete sparkapplication/job-pyspark-processing-titanic -n sparkoperator
    ```
    <br>

    Após o comando `apply` e em caso de sucesso no processamento.
    
    *Output: [simulação de sucesso]*
    ```console
    NAME                                                     READY   STATUS    RESTARTS   AGE
    job-pyspark-processing-titanic-6c16db7c8a756eca-exec-1   1/1     Running   0          24s
    job-pyspark-processing-titanic-driver                    1/1     Running   0          31s
    spark-spark-operator-59c685545-84nq9                     1/1     Running   0          53m
    ```

    :point_right: *Observação: Veja que foi criado um `POD` **driver** e outro **exec-1** conforme a definição do arquivo `yaml`.*

    Com a finalização do processo será visualizado da seguinte forma.
    *Output:*
    ```console
    NAME                                    READY   STATUS      RESTARTS   AGE
    job-pyspark-processing-titanic-driver   0/1     Completed   0          3m3s
    spark-spark-operator-59c685545-84nq9    1/1     Running     0          56m
    ```

    :point_right: *Observação: Veja que o `POD` **driver** ' mantido para histórico e verificação da conclusão do processo, porem o `POD` **exec-1** com a sua finalização o mesmo é removido da lista de `PODs` automaticamente.

    <br>
    Neste ponto e com a finalização do Job de teste com sucesso podemos concluir que o ambiente está *OK* para seguirmos para próximas etapas.

    <br>
## Preparação e Deploy do Airflow no k8s:

Para a orquestração dos pipelines de processamento de dados estaremos utilizando o Apache Airflow, e para fazer o deploy no cluster k8s iremos utilizar uma imagem `Helm` que pode ser localizada no link abaixo:
<br>
Helm Chart for Apache Airflow:
https://airflow.apache.org/docs/helm-chart
<br>

Verifique as instruções e siga as etapas de instalação:


1. Criação do namespace `ariflow`,caso não exista em seu cluster k8s.
    <br>
    Para verificar os namespaces existentes utilize o comando abaixo e verifique na lista retornada:

    ```shell
    kubectl get namespaces
    ```
    
    <br>

    Para criar o namespace *`airflow`*:

    ```shell
    kubectl create namespace airflow
    ```

    <br>

    Apenas como verificação você pode utilizar o comando para listar todos os namespaces e verificar se o *`airflow`* foi criado devidamente, e/ou também pode utilizar o comando abaixo para verificar todos os recursos disponíveis em um namespace, no caso *`airflow`* quando acabar de ser criado não deve apresentar nenhum item.

    ```shell
    kubectl get all -n airflow
    ```
    <br>

2. Atualização a imagem chart do *`airflow`* no repositório *`helm repo`* local antes do deploy no k8s.
    <br>
    Para incluir a imagem chart do `airflow` localmente, execute este comando:

    ```shell
    helm repo add apache-airflow https://airflow.apache.org
    ```

    <br>
    Se já houver a imagem do chart do `airflow` baixada anteriormente, execute a atualização do repositório para garantir que está com a versão mais atualizada.
    
    ```shell
    helm repo update
    ```

    <br>

3. Preparação do arquivo `values` que contém as instuções para deploy no `k8s` via `helm`.
    <br>
    Para gerar o arquivo `values` para o deploy, executar o comando abaixo:
    
    ```shell
    helm show values apache-airflow/airflow > step-3-airflow/my-airflow-values.yaml
    ```

    Onde:
    - Sintaxe - `helm show values [CHART] [flags]`
    - `[CHART]` - identificação do chart que foi feito o download no passo acima.
    - `[flags]` - parametros adicionais não utilizados neste exemplo.

    <br>

    Output: (operador `>`)
    - `step-3-airflow` - pasta do projeto para armazenar as instruções ou configurações de deploy para k8s via helm.
    - `my-airflow-values.yaml` - nome do arquivo que irá armazenar as alterações das configurações originais.

    <br>

    Alterações realizadas no arquivo `my-airflow-values.yaml`:

    - Version:

        ```yaml

            # Airflow home directory
            # Used for mount paths
            airflowHome: /opt/airflow

            # Default airflow repository -- overrides all the specific images below
            defaultAirflowRepository: apache/airflow

            # Default airflow tag to deploy
            defaultAirflowTag: "2.1.2"

            # Airflow version (Used to make some decisions based on Airflow Version being deployed)
            airflowVersion: "2.1.2"
        ```

        :point_right: *Atenção: é muito importante que seja verificado a versão do airflow, pois algumas variáveis de ambiente são diretamente ligadas as versão do airflow. Para este caso indica-se manter a `versão 2.1.2`.*
        <br>

    - Executor:

        ```yaml
            # Airflow executor
            # Options: LocalExecutor, CeleryExecutor, KubernetesExecutor, CeleryKubernetesExecutor
            # executor: "CeleryExecutor"
            executor: "KubernetesExecutor"
        ```

    - Environment variables:

        ```yaml
            # Environment variables for all airflow containers
            env:
            - name: AIRFLOW__CORE__REMOTE_LOGGING
                value: 'True'
            - name: AIRFLOW__CORE__REMOTE_BASE_LOG_FOLDER
                value: 'gs://dl-techinical-apps/airflow-logs/'
            - name: AIRFLOW__CORE__REMOTE_LOG_CONN_ID
                value: 'my_gcp'
        ```

    - Create initial user:

        ```yaml
            # Create initial user.
            defaultUser:
                enabled: true
                role: Admin
                username: smedina
                email: smedina1304@gmail.com
                firstName: Sergio
                lastName: Medina
                password: admin
        ```

    - Service type.

        ```yaml
            service:
                #type: ClusterIP
                type: loadBalancer
        ```

    - Redis disable.

        ```yaml
            # Configuration for the redis provisioned by the chart
            redis:
                enabled: false
        ```

    - DAGs\Gitsync enable

        ```yaml
            gitSync:
                enabled: true

                # git repo clone url
                # ssh examples ssh://git@github.com/apache/airflow.git
                # git@github.com:apache/airflow.git
                # https example: https://github.com/apache/airflow.git
                repo: https://github.com/smedina1304/edc-airflow-spark-on-k8s.git
                branch: main
                rev: HEAD
                depth: 1
                # the number of consecutive failures allowed before aborting
                maxFailures: 0
                # subpath within the repo where dags are located
                # should be "" if dags are at repo root
                subPath: "dags"
        ```

    <br>


4. Airflow DAGs, criando uma pasta para armazenar as dags e um exemplo para teste de funcionalidade do airflow.
    <br>
    Na pasta raiz do projeto foi criada uma pasta com o Nome `dags`.
    <br>
    Foi adicionado uma código de exemplo para testes de funcionamento do `airflow` com o nome `example_taskflow_api_etl.py`
    <br>
    <br>

5. Delpoy do Airflow no Cluster k8s.

    Após as preparações anteriores finalizadas executar o seguinte comando:

    ```shell
    helm install airflow apache-airflow/airflow -f step-3-airflow/my-airflow-values.yaml -n airflow --debug
    ```
    <br>

    :point_right: *Atenção: Sendo necessário desistalar o airflow por qualquer motivos, utilize o comando abaixo ou busque uma referência do mesmo para atendimento da necessidade:*

    ```shell
    helm uninstall airflow -n airflow --debug
    ```

    Após uma soliciatação de desinstalação sempre verifique se os recursos foram liberados.
    <br>
    <br>

6. Recuperar a `Fernet Key value`.

    Caso não tenha sido definido a `Fernet Key value` no arquivo `yaml`, como no caso deste tutorial, a mesma é gerada automaticamente e sendo necessário a sua utilização, é possível buscar o valor desta chave utilizando o comando abaixo:

    ```shell
    kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode
    ``` 

    <br>
    <br>

    