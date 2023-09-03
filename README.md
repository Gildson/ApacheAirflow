## ApacheAirflow
Scripts feitos no curso de Apache Airflow do Fernando Amaral disponível na Udemy

Para executar os Apache Airflow é preciso ter o docker instalado no computador, inicie o docker e em seguida abra um cmd ou powershell e aponte para a pasta onde os arquivos foram inseridos e roda o comando abaixo:
## docker-compose up -d

Isso pode demorar um pouco, após o container está rodando no docker abra um navegador e digite:
## localhost:8080

Assim o Airflow abrir a página de login, digite:
## senha: airflow 
## password: airflow

Você irá ver todas as dags criadas no cursos, algumas eu alterei para testas coisas que o professor ia ensinando.

Para encerrar o docker, digite:
## docker-compose down

Requisitos para entender os códigos
<img align="center" height="90" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" />

OBS importante:
Caso precise mudar qualquer configuração no Airflow faça no docher-compose.yaml, assim toda vez que você feichar e reabrir o container as alterações estarão disponível, se quiser fazer no airflow.cfg, quando parar o container e iniciar novamente as alterações terão sido perdidas, pois o arquivo yaml sobrescreve as informações do airflow.cfg
