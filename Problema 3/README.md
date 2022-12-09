<div id="titulo">
    <h1 id="titulo" align="center"> Problema 3 - Serviço de Marketplace Distribuído</h1>	
    <h2 id="titulo" align="center"> Saldão dos Computadores.</h1>
	<p id="descricao" align="justify">
 A loja Saldão dos Computadores está enfrentando problemas em suas vendas. Cada marketplace possui 
sua própria base de dados, e a loja tem de informar a cada marketplace os produtos disponíveis e a quantidade 
total deles em seus estoques. Para a resolução deste problema, foi exigido um sistema distribuído visando atender as lojas 
e facilitar o gerenciamento dos estoques.
Como requisitos para a solução distribuída, o consórcio decidiu que as lojas precisam cadastrar o produto 
apenas em um dos marketplaces. Também, a partir de qualquer servidor de marketplace, os clientes podem 
realizar  transações  atômicas  sobre  os  itens  selecionados  no  carrinho  de  compras,  e  que  podem  ter  sido 
cadastrados em qualquer servidor que faz parte do consórcio. Para atender as lojas, a comunicação entre os 
servidores de marketplace deve ser estabelecida de forma que as lojas não vendam mais produtos do que a 
quantidade existente em seu estoque ou que uma mesma unidade seja vendida para clientes distintos 
    </p>

</div>

<div id="sumario">
    <h1>Sumário</h1>
	<ul>
		<li><a href="#inicio"> <b>Início</b></li>
        <li><a href="#equipe"> <b>Equipe de Desenvolvimento</b></li>
        <li><a href="#requisitos"> <b>Requisitos Atendidos</b> </a> </li>
		<li><a href="#tecnologias"> <b>Tecnologias</b> </a></li>
		<li><a href="#implementacao"> <b>Implementação</b> </a> </li>
		<li><a href="#pre-requisitos"> <b>Pré-requísitos</b> </a> </li>
        <li><a href="#metodologia"> <b>Metodologia</b> </a> </li>
        <li><a href="#conclusao"> <b>Conclusão</b> </a> </li>
	</ul>	

<div id="inicio">
    <h1>Inicio</h1>
    <p id="descricao" align="justify">
    ADICIONAR TEXTO.     
    </p>
</div>

<div id="equipe">
    <h1>Equipe de Desenvolvimento</h1>
    <ul>
		<li><a href="https://github.com/danrleiaraujo"> Danrlei Almeida Araujo</a></li>
        <li><a href="https://github.com/Evelynsuzarte"> Evelyn Suzarte Fernandes</a></li>
	</ul>
</div>

<div id="tutor">
    <h1>Tutor</h1>
    <ul>
		<li><a>José Amancio Macedo Santos</a></li>
	</ul>
</div>


<div id="requisitos">
    <h1>Requisitos do sistema</h1>
	<ul>
		<li>Sicronização de banco de dados com uso de algoritmo de sincronização :heavy_multiplication_x:</li>
		<li>Atualização automática dos bancos de dados :heavy_multiplication_x:</li>
		<li>Uso do protocolo baseado em uma API REST :heavy_check_mark:</li>
		<li>Transações atômicas sobre os itens do carrinho de compras :heavy_multiplication_x:</li>
        <h3><b>Interfaces do cliente:</b></h3>
		<li>Visualização dos produtos:heavy_check_mark:</li>
		<li>Ação de compra aos produtos:heavy_check_mark:</li>		
		<li>Ação de adicionar produtos ao carrinho :heavy_check_mark:</li>
        <h3><b>Interfaces do administrador:</b></h3>
		<li>Adicionar/remover produtos :heavy_check_mark:</li>
		<li>Verificação de produtos cadastrados :heavy_check_mark:</li>
		<li>Adicionar/remover ADMs :heavy_check_mark:</li>
		<li>Verificação de ADMs cadastrados :heavy_check_mark:</li>
	</ul>
</div>

<div id="tecnologias">
    <h1>Tecnologias</h1>
    <ul>
		<li><a href="https://github.com/danrleiaraujo"> Python </a></li>
        <li><a href="https://flask.palletsprojects.com/en/2.2.x/"> Flask</a></li>
		<li><a href="https://mqtt.org/"> MQTT </a></li>
	</ul>
</div>

<div id="implementacao">
    <h1>Implementação</h1>
    <p id="descricao" align="justify">
    	<li> Para implementação do código foi utilizado a linguagem de programação python e suas bibliotecas.</li>
		<li> Para a comunicação entre lojas, foi utilizado o MQTT.</li>
		<li> Para a comunicação entre repositório e usuario foi necessário a inclusão de uma API Rest - com o uso de Flask.</li>   
    </p>  
    <h1>Restrições</h1>  
    <p> 
        <ul><p align="justify"> 
        <li> O produto deve ser desenvolvido através de contêineres Docker.</li>
        <li> A comunicação entre os servidores dos marketplaces deve ser implementada através de um protocolo baseado em uma API REST.</li>
    </p> 
</div>
<div id="pre-requesitos">
    <h1>Pré-requisitos</h1>
    <h2>Antes de começar, você vai precisar ter instalado:</h32>
    <li>Flask</li>
    <li>Paho.MQTT</li>
    <li>mosquitto</li>
</div>
<div id="metodologia">
    <h1>Metodologia</h1>
    <h2><p><b>Interação com usuário:</b></p></h2>
    <p align="justify"> 
        O usuário deve se comunicar através de uma interface web, onde uma API faz a requisição dos dados.
        Na interface, o usuário tem a possibilidade de:
        <li>Acrescentar produto no carrinho</li>
        <li>Finalizar compra</li>
        Caso o usuário seja um administrador, o leque de coisas que ele pode fazer se extende, sendo elas:
        <li>Acrescentar produto no estoque</li>
        <li>Acrescentar um novo administrador</li>
        <li>Verificar os produtos no estoque</li>
        <li>Verificar os administradores do sistema</li>
        <li>Remover um produto, ou uma quantidade do estoque</li>
        <li>Remover um administrador</li>
    </p>    
    <h2><p><b>API REST:</b></p></h2>
    <p align="justify"> 
        A API é responsável por passar e receber informações vindas da página web ao processamento de dados, sendo assim ela:
        <li>Recebe informações através do método GET</li>
        <li>Envia informações através do método POST</li>
    </p>    
    <h2><p><b>MQTT:</b></p></h2>
    <p align="justify"> 
        O MQTT é responsável para sincronizar as lojas, ele faz um publish no tópico "/lojas/online/"
        com a mensagem "lojasOnline", que é um dicionário "lojasOnline = {MATRICULA : client_id}" convertido em string. 
        Caso quem receba o dicionário, tenha um dicionário menor, ela atualiza o dicionário local pelo recebido.
        <h3>Exemplo:</h3>
    	<img src= "https://github.com/danrleiaraujo/MI_Concorrencia_e_Conectividade/blob/main/Problema%203/static/exemploMqtt.png"/>
        <li>Iniciei 3 lojas, cada um com uma matricula diferente, assim que iniciava, o dicionário se atualizava</li>
    </p>      
</div>

<div id="conclusao">
    <h1>Conclusão</h1>
    <p id="descricao" align="justify">
    ADICIONAR TEXTO.     
    </p>
</div>
