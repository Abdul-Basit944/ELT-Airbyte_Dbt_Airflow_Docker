FROM  apache/airflow:latest

RUN pip install apache-airflow-providers-docker \
    && pip install apache-airflow-providers-http \
    && pip install apache-airflow-providers-airbyte 

RUN pip install dbt-postgres==1.4.7

USER root

  # webserver:
  #   build:
  #     context: .
  #     dockerfile: Dockerfile
  #   user: root
  #   depends_on:
  #     - postgres
  #   networks:
  #     - elt_network
  #   extra_hosts:
  #     - "host.docker.internal:host-gateway"
  #   volumes:
  #     - ./airflow/dags:/opt/airflow/dags
  #     - ./elt:/opt/airflow/elt
  #     - ./custom_postgres:/opt/dbt
  #     - ~/.dbt:/root/.dbt
  #     - /var/run/docker.sock:/var/run/docker.sock

  #   environment:
  #     - LOAD_EX=n
  #     - EXECUTOR=Local
  #     - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
  #     - AIRFLOW__CORE__FERNET_KEY=A7sz--6ajX3McQUNMIMusf_TOnkEAun2R0Zg9N8aW6U=
  #     - AIRFLOW__WEB_SERVER__DEFAULT__USER=airflow
  #     - AIRFLOW__WEB_SERVER__DEFAULT__PASSWORD=password
  #     - AIRFLOW_WWW_USER_USERNAME=airflow
  #     - AIRFLOW_WWW_USER_PASSWORD=password
  #     - AIRFLOW__API_SERVER__SECRET_KEY=secret
  #   ports:
  #     - "8080:8080"
  #   command: ["airflow", "api-server"]
