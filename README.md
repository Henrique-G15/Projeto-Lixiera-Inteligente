Repositorio destinado a lixeira inteligente.
lembre se de: 
rodar a main, depois rodar o broker e depois rodar o projeto fisico. 

Arrumar para na tabela lixeira o estado da lixera ser atuaizado (update na tabela) toda vez que a tampa for aberto |(comando remoto e infravermelho) 

Implementar o recebimento da mensagm no topico 'test/publish' para fazer o udpate na tabela lixeira no campo capacidade (atualizar o tipo de dado que a tabela acieta no campo, acho que esta int. arrume o banco no codigo tb) no caso as mesagem recebidas no topico para vc ter uma ideia são 'cheio', 'metade da capacidade', 'vazio'. Dados que devem ser aramzendado no campo 'capacidade' da lixeira especifica

cadastro de usuario, ter a dropbox das lixeiras disponiveis no cadastro do suuario, conforme o professor pediu