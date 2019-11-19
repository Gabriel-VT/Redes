# Redes

Trabalho - Protocolos de rede em camada de transporte (Peer to Peer e Cliente-Servidor) baseados na biblioteca Python 'socket'.

Feito por Felipe Costa, Gabriel Viana Thomaz, Mateus Nascimento Barbosa, Pedro Dionísio, Rodrigo Ferreira Bostrom, Victor De Luca S. N. Silva - Universidade Federal do Rio de Janeiro (UFRJ) - Rio de Janeiro – RJ – Brasil.
Professor Claudio Miceli.

INSTRUÇÕES:
  *Abrir um Server:* 
    1-Instancie um objeto da classe "Server"
    2-Chame a função "Server.run()"
    3-O servidor irá abrir para os clientes se conectarem. Os clientes podem se conectar ou desconectar a qualquer momento.
    4-O servidor irá receber mensagens e encaminhá-las a todos os clientes conectados.    
    
  *Abrir um Client:*
    1-Instancie um objeto da classe "Client"
    2-Chame a função "Client.run()"
    3-Digite o IP do servidor e o seu apelido quando for solicitado.
    4-Digite a mensagem a ser enviada. As mensagens enviadas pelos demais clientes serão mostradas conforme forem sendo recebidas.

Referência da biblioteca 'socket' (py3): https://docs.python.org/3/library/socket.html
Referência da biblioteca 'thread' (py3): https://docs.python.org/3/library/_thread.html
