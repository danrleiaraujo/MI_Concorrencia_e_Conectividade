<div id="inicio">
    <h1 id="titulo" align="center"> Problema 2 da disciplina MI - Concorrência e conectividade.</h1>
	<h2 id="titulo" align="center"> Consumo inteligente.</h1>
	<p id="descricao" align="justify">
    Foi requisitado um hidrometro Diante do sucesso da primeira implementação do protótipo, a prefeitura da cidade ficou interessada 
    em  ampliar  o  projeto  visando  não  apenas  encontrar  vazamentos  nas  tubulações,  mas  também  gerenciar  o 
    consumo de água dos usuários. O volume de água do reservatório que abastece a cidade já alcançou níveis 
    críticos, e uma comissão formada por representantes de diferentes setores da sociedade foi estabelecida para 
    determinar  regras  justas  de  racionamento.  Dessa  forma,  ficou  estabelecido  que  <b>nenhum  usuário  deve 
    ultrapassar a média do consumo de todos os usuários</b>, <b>nem ultrapassar um valor máximo em metros cúbicos 
    durante um certo período estabelecido</b>, <b>com risco de corte instantâneo e controlado em seu abastecimento</b>.     
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
        <li><a href="#metodologia"> <b>Metodologia</b> </a> </li>
        <li><a href="#conclusao"> <b>Conclusão</b> </a> </li>
	</ul>	
</div>

<div id="equipe">
    <h1>Equipe de Desenvolvimento</h1>
    <ul>
		<li><a href="https://github.com/danrleiaraujo"> Danrlei Almeida Araujo</li>
	</ul>
    <h1>Tutor</h1>
    <ul>
        <li><a>José Amancio Macedo Santos</a></li>
    </ul>
</div>

<div id="requisitos">
    <h1>Requisitos Atendidos</h1>
	<ul>
		<li>Emprego da arquitetura distribuida edge/nevoa ou p2p :heavy_check_mark:</li>
		<li>Protocolo da comunicação MQTT :heavy_check_mark:</li>
		<li>Protocolo da comunicação Rest :heavy_multiplication_x:</li>
		<li>Calculo distribuido da media entre os hidrometros :heavy_check_mark:</li>
		<li>Tratamento do atraso e quantidade de dados enviados a nuvem :heavy_check_mark:</li>
		<li>Implementação dos sensores e geração de dados aleatória :heavy_check_mark:</li>		
		<li>Bloqueio automatizado dos hidrometros :heavy_check_mark:</li>
		<li>Monitoramento dos dados dos "n" hidrometros consulta :heavy_multiplication_x:</li>
		<li>Monitoramento hidrometro selecionado (ver os dados) :heavy_multiplication_x:</li>
		<li>Documentação do código :heavy_check_mark:</li>
	</ul>
</div>

<div id="tecnologias">
	<h1> Tecnologias </h1>
	<ul>
        <li><a href="https://www.python.org/">Python</a></li>
		<li><a href="https://mqtt.org/">MQTT</a></li>
		<li><a href="https://flask.palletsprojects.com/en/2.2.x/">Flask</a></li>
	</ul>	


<div id="implementacao">
	<h1>Implementação</h1>
	<ul><p align="justify"> 
    	<li> Para implementação do código foi utilizado a linguagem de programação python e suas bibliotecas.</li>
		<li> Para a comunicação entre hidrometro e névoa, foi utilizado o MQTT.</li>
		<li> Para a comunicação entre nuvem e usuario foi necessário a inclusão de uma API Rest - com o uso de Flask.</li>
    <p> 
	<h1>Restrições</h1>
		<ul><p align="justify"> 
    	<li> A interface do gerente deve permitir selecionar N hidrômetros de maior consumo.</li>
		<li> Entre os hidrômetros listados deve permitir selecionar um deles para visualizar os dados com o menor tempo de latência possível.</li>
		<li> O produto deve ser desenvolvido através de contêineres Docker.</li>
    <p> 
</div>	
	
<h2>Pré-requisitos</h2>
<h3>Antes de começar, você vai precisar ter instalado:</h3>
<li>Flask</li>
<li>Paho.MQTT</li>
<li>mosquitto</li>

<div id="metodologia">
	<h1>Metodologia</h1>
	<h2><p><b>Interação com usuário:</b></p></h2>
	<p align="justify"> 
        O usuário deveria se comunicar através de uma interface onde uma API, que por sua vez faria a requisição dos dados.
    <p> 
	<h2><p><b>Funcionamento:</b></p></h2>
	<h3><p><b>Diagrama da Arquitetura da distribuida:</b></p></h3>
	<div align="center"> 
	<img src= "https://github.com/danrleiaraujo/MI_Concorrencia_e_Conectividade/blob/main/Problema%202/static/DiagramaConcorrenciaP2.png">
	<div>
	<h3><p><b>Hidrometro:</b></p></h3>
	<p align="justify"> 
        O hidrometro seria um gerador de dados, além disso seria identificado com qual região esse hidrometro estaria, sendo ela <b>Norte, Sul, Leste, Oeste.</b> Eles enviam além de seus identificadores, o consumo da residência em m³, a hora exata de sua medição e o estado de funcionamento.
    <p>
	<h3><p><b>Névoa:</b></p></h3>
	<p align="justify"> 
		As névoas, seriam o intermediário entre o hidrometro e a "Nuvem" (servidor), sendo uma forma de diminuir e fitrar a quantidade de dados. Ela é responsável por conhecer todos os hidrometros, mandar o bloqueio/desbloqueio para o mesmo, realizar o cálculo da média de consumo, porém apenas da região.
    <p>
	<h3><p><b>Nuvem:</b></p></h3>
	<p align="justify"> 
		A Nuvem estabelece conexão com todas as "Névoas", escutando e enviando requisições, além disso são repassadas informações e ouvidas requisições da API Rest.  Os identificadores das névoas são mantidos armazenados de forma a permitir o acesso rápido à região do hidrômetro solicitado pelo usuário, evitando que todas as névoas recebam a mesma requisição em que apenas uma deve responder.
    <p>	
	<h3><p><b>Comunicação MQTT:</b></p></h3>
	<p align="justify"> 
		O protocolo de comunicação utilizado foi o MQTT, por conta da sua extensa aplicação em Internet das Coisas, além de sua capacidade de estabelecer uma comunicação rápida e facilitada.
		O sistema de comunicação é baseado em 2 pontos de Broker MQTT, sendo um dedicado a Nuvem com as Névoas e o outro para as Névoas com os Hidrometros. Com isso a padronização dos tópicos ficaram da seguinte forma:
		<h4>Broker Nuvem e Névoas: nuvem/ </h4>
		<li>nuvem/media/[idNevoa] : </li>
		Tópico onde são publicadas as médias de consumo de cada névoa.
		<li>nuvem/consumo/[idNevoa] : </li>		
		A nuvem solicita N hidrômetros e cada névoa envia sua lista com N hidrômetros que mais consomem por este subtópico. Caso seja um número inválido, a lista conterá 30% dos hidrômetros do nó solicitado.
		<h4>Brokers Nevoas e Hidrômetros: hidrometros/local/ </h4>
		<li>hidrometros/local/consumo/:</li>	
		Onde cada hidrômetro publica seu log de consumo.
		<li>hidrometros/local/status/:</li>
		Tópico em que a névoa transmite a mensagem de bloqueio para determinado hidrômetro, após verificar se o consumo se encontra dentro do permitido.
    <p>
</div>

<div id="conclusao">
	<h1>Conclusão</h1>
	<p align="justify"> 
	Apesar de ter tempo suficiente para a solução do problema, de muitas discussões em tutoriais, por conta da complexidade e da quantidade de requisitos, o problema encontra-se <b>incompleto.</b> A parte da API não conversa com a Núvem que é o servidor central, sendo assim mantendo a impossibilidade de requisições de usuário sobre o hidrometro. Além disso não foi possível a implementação total da núvem, onde a mesma apenas escuta as informações repassadas pelas névoas. Porém, o aprendizado sobre o protocolo de comunicação MQTT foi um êxito, tendo sua implementação completa, os hidrômetros geram dados, bloqueam e desbloqueam de modo autônomo, é realizado um cálculo de média dos hidrometros, porém só em região da névoa, o monitoramemento dos dados estão sendo através de terminal mas não é possível a seleção de "n" Hidrometros para consulta. 
    <p>
</div>
