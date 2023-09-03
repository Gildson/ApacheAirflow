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
