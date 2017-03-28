#PYGLB

Projeto feito com:
    python 3.6
    Tornado
    MongoDB
    Memcached
    Docker

Recursos
    Criar usuario e fazer login
    Autenticar com token de acesso
    Verificar noticias da globo/noticias

##pre-requisitos
    docker > https://docs.docker.com/installation/mac/

    $ docker-machine --version
    docker-machine version 0.10.0, build 76ed2a6
    $ docker-compose --version
    docker-compose 1.11.2

##Clonando um projeto de exemplo
    mkdir tmp && cd tmp && git clone https://github.com/tgonzales/pyglb

##Criando uma VM para dev
    Durante a instalação do docker pelo toolbox será criado uma VM default,
    para conferir execute no terminal
    $ docker-machine ls
    NAME      ACTIVE   DRIVER       STATE     URL   SWARM
    default   -        virtualbox   Stopped

    Para ativar
    $ docker-machine start default
    Ativar as variaveis de ambiente no console dessa VM no terminal atual.
    $ eval "$(docker-machine env default)"
    Para saber o IP da VM,
    $ docker-machine ip default
    Outros Comandos
    $ docker-machine help
    Para criar uma nova VM
    $ docker-machine create -d virtualbox dev
    Ao criar uma nova a mesma será ativada automaticamente. Basta chamar a ENV
    $ eval "$(docker-machine env dev)"

##Imagens Padrão
### Mongodb
Container do mongoDB - sem opção de volume, quando o container é stopado os dados são perdidos, esse container é usado para desenvolvimento. Para persistir dados deve ser criado um script de dump na aplicação.

### Memcached
Container padrao do memcached

##Imagens Personalizadas
###Dockerfile
É o arquivo de configuração para a criação da imagem do projeto. Pyglb possui uma imagem Dockerfile que herda da imagem python3.6 que por sua vez herda de ubuntu:16.04, faz a instalação dos pacotes necessários (requirements.txt), e copia o codigo fonte para dentro da imagem
    
##Containers
###docker-compose.yml
Possui a receita para a criação dos containers do projeto.
  
###Ativando, fazendo o Build e executando o compose
    $ docker-machine start default
    $ eval "$(docker-machine env default)"
    $ docker-compose up -d
    $ docker-compose ps # status sobre os container ativos
    # exemplo port: 0.0.0.0:32769->8001/tcp
    $ docker-machine ip default
    http://192.168.99.100/
    No browser: http://192.168.99.100:32769/
    para acompanhar o log
    $ docker-compose logs pyglb

### Run
    ver docker hostname ex.
    curl pyglb/hello

    Acesso não autorizado
    $ curl -X GET \
    -H "X-Version: 1" \
    -H "Authorization: Bearer ThisTokenNotExist" \
    http://localhost:8001/hello
    $ "Vc nao esta autenticado" 

    Criando um Usuario
    $ curl -X POST -v \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{"email":"teste@teste.com","password":"1234"}' \
    http://localhost:8001/api/users/
    $ {"response": "Usuario criado com sucesso"}

    Fazendo o Login
    $ curl -X GET \
    -d "email=teste@teste.com&password=1234" \
    http://localhost:8001/api/users/
    $ {"msg": "Usuario autenticado com sucesso","user": {"email": "teste@teste.com"},"token": "85e5d2c1c422422ebab29dab9a39ae1c"}

    Testando o acesso autorizado
    $ curl -X GET \
    -H "X-Version: 1" \
    -H "Authorization: Bearer 85e5d2c1c422422ebab29dab9a39ae1c" \
    http://localhost:8001/hello
    $ {"msg": "Autenticado", "user": {"email":"teste@teste.com"}}

    Acessando o Crawler PYGLB
    $ curl -X GET \
    -H "X-Version: 1" \
    -H "Authorization: Bearer 85e5d2c1c422422ebab29dab9a39ae1c" \
    http://localhost:8001/api/noticias/
    $ json com noticias

    Parametros
    limit, quantidade de noticias que de resposta, ex
    http://localhost:8001/api/noticias/?limit=2
    
    OBS
    Nao e recomendável enviar senha como esta nesse teste básico, é recomendável que a senha seja criptografada antes do envio (frontend) e que o mesmo seja por https.


###Deploy
##Criando maquina de PreProd na DigitalOcean
    $ docker-machine create \
                  -d digitalocean \
                  --digitalocean-access-token=ADD_YOUR_TOKEN_HERE \
                  preprod

    $ docker-machine start preprod
    $ docker-compose build
    $ docker-compose up -d
    $ docker ps


##Criando maquina de produção na AWS
    $ docker-machine create \
            	-d amazonec2 \
            	--amazonec2-access-key ADD_YOUR_TOKEN_HERE \
            	--amazonec2-secret-key ADD_YOUR_TOKEN_HERE \
            	--amazonec2-zone a \
            	--amazonec2-region us-west-2a \
            	—-amazonec2-instance-type t1.micro \
            	--amazonec2-vpc-id 38cdbb5d \
              production

    $ docker-machine start production
    $ docker-compose build
    $ docker-compose up -d 
    $ docker ps
