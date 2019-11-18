# Redes

Trabalho - Protocolos de rede em camada de transporte (Peer to Peer e Cliente-Servidor) baseados na biblioteca Python 'socket'.

Feito por Felipe Costa, Gabriel Viana Thomaz, Mateus Nascimento Barbosa, Pedro Dionísio, Rodrigo Ferreira Bostrom, Victor De Luca S. N. Silva - Universidade Federal do Rio de Janeiro (UFRJ) - Rio de Janeiro – RJ – Brasil.
Professor Claudio Miceli.

INSTRUÇÕES:
  *Abrir um Server:* 
    1-Instancie um objeto da classe "Server"
    2-Chame a função "Server.run()"
    3-Digite o número da porta quando for solicitado. O IP será o local da máquina.
    4-O servidor irá aguardar a conexão de algum cliente.
    5-Quando houver conexão, o servidor irá começar a receber mensagens e armazenar para encaminhar ao destinatário das mesmas. Este processo é feito em outra thread, em paralelo com a conexão de novos clientes simultaneamente.
    6-Caso haja mensagens para o cliente conectado, estas serão encaminhadas. Caso não haja, será avisado que não há.
    7-O processo se repete a partir da etapa 4.
    
    
  *Abrir um Client:*
    1-Instancie um objeto da classe "Client"
    2-Chame a função "Client.run()"
    3-Digite o IP do servidor e o número da porta quando for solicitado.
    4-Digite o destino da mensagem quando for solicitado. Insira "0" para fehar a conexão e sair.
    5-Caso não tenha digitado "0" anteriormente, digite o texto da mensagem.
    6-Após isto, serão encaminhadas as mensagens enviadas pelos outros Client para você.
    7-Repita o processo a partir da etapa 4.

Referência da biblioteca 'socket' (py3): https://docs.python.org/3/library/socket.html
Referência da biblioteca 'thread' (py3): https://docs.python.org/3/library/_thread.html
