Calculadora Financeira com Interface Tkinter e Ícone na Bandeja
Este projeto implementa uma calculadora gráfica usando tkinter com recursos adicionais como suporte a operações matemáticas avançadas, substituição de operadores ao inserir símbolos consecutivos, e um ícone na bandeja do sistema.

Funcionalidades principais

Interface moderna com personalizado de barra superior (com botões de fechar, maximizar/restaurar e minimizar)

Entrada de expressões através de botões ou teclado

Ajuda na entrada de operações ao substituir operadores duplicados

Avaliação de expressões, incluindo raiz quadrada e operadores com precedência

Ícone na bandeja do sistema para restaurar ou sair com menu de opções

Capacidade de maximizar ou restaurar a janela

Como funciona o código
Variáveis globais

resultado_exibido: controla se o resultado recente foi exibido, para reiniciar a entrada ao digitar novos números

current_text: armazena a expressão atualmente digitada

WINDOW_WIDTH e WINDOW_HEIGHT: tamanho inicial da janela

maximized, normal_geometry: controle de estado de maximização

icon: referência à instância do ícone na bandeja

Funções principais
Gerenciamento de Janela

center_window(win, width, height): centraliza a janela na tela

move_window(event), start_move(event): movimenta a janela ao arrastar a barra superior

maximize_restore_app(): maximiza ou restaura a janela

Entrada de números e operadores

button_click(valor): adiciona o valor ao texto, substituindo operador se necessário

is_operator(char): verifica se um caractere é operador matemático

No button_click, ao inserir um operador, se o último caractere for operador, ele será substituído pelo novo (evitando múltiplos operadores consecutivos)

Avaliação de expressões

equals(): avalia a expressão, convertendo raízes quadradas e operadores, e exibe o resultado

Utiliza eval() com tratamento de substituição de ^ por ** e √( por math.sqrt(

Eventos do teclado

tecla_pressionada(event): trata entrada de teclas, incluindo entradas numéricas, operadores, backspace, enter e escape

Gerenciamento do ícone na bandeja

create_image(): cria uma imagem para o ícone

setup_tray_icon(): inicia o ícone com menu de restaurar e sair

close_app(), minimize_app(), restore_app(): ações ao interagir com o ícone

Widget e layout

Janela Customizada: usa overrideredirect para remoção da barra padrão

Barra superior: com botões que ativam ações de fechar, maximizar/restaurar e minimizar

Display: campo de entrada de expressões, alinhado à direita

Botões numéricos e operadores: organizados em grade

Botões especiais: raiz quadrada (√), parênteses e expoente (^)

Execução
Para rodar o programa, basta executar o arquivo Python. A interface aparecerá, e a interação acontece via botões ou teclado. O ícone na bandeja fica acessível para restaurar ou fechar a aplicação.

Notas finais

Certifique-se de instalar as dependências: pystray e Pillow.

Para uma melhor experiência, podem ser feitas melhorias na estética ou acrescentar suporte a outros recursos matemáticos.