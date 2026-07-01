# La Cantina Cheff 🍽️

Sistema de gerenciamento de cantina universitária desenvolvido para a disciplina de Projeto Integrador ADS A.

---

## Pré-requisitos

- Python 3.11 ou superior
- Navegador (Chrome, Edge, etc.)

---

## Instalação e execução

### Passo 1 — Abrir o terminal na pasta correta

1. Abra a pasta `la-cantina-cheff` no explorador de arquivos
2. Entre na pasta `backend`
3. Clique na barra de endereço do explorador, digite `cmd` e aperte **Enter**

### Passo 2 — Instalar o Flask (só na primeira vez)

```
pip install flask flask-cors
```

### Passo 3 — Criar o banco de dados (só na primeira vez)

```
python banco.py
```

Deve aparecer a mensagem:
```
Banco de dados criado com sucesso!
```

### Passo 4 — Iniciar o servidor

```
python servidor.py
```

Deve aparecer a mensagem:
```
Servidor rodando em http://localhost:5000
```

### Passo 5 — Abrir o sistema

Abra o arquivo `index.html` no navegador.

---

## Como usar no dia a dia

1. Abre o terminal na pasta `backend`
2. Digita `python servidor.py`
3. Abre o `index.html` no navegador
4. Usa o sistema normalmente

> ⚠️ O servidor precisa estar rodando **sempre** que for usar o sistema. Se fechar o terminal, o sistema para de funcionar.

**Para parar o servidor:** aperta `CTRL+C` no terminal.

---

## Estrutura do projeto

```
la-cantina-cheff/
├── index.html              ← Dashboard principal
├── pages/
│   ├── login.html          ← Tela de login
│   ├── produtos.html       ← Gerenciamento de produtos
│   ├── pedidos.html        ← Registro de pedidos
│   ├── estoque.html        ← Controle de estoque
│   ├── relatorios.html     ← Relatórios
│   ├── perfil.html         ← Perfil do administrador
│   ├── configuracoes.html  ← Configurações
│   └── faq.html            ← Perguntas frequentes
├── css/                    ← Estilos
├── js/                     ← Scripts do AdminLTE
├── img/                    ← Imagens
└── backend/
    ├── banco.py            ← Cria o banco de dados
    ├── servidor.py         ← Servidor Flask
    └── cantina.db          ← Banco de dados (gerado automaticamente)
```

---

## Rotas da API

| Método | Endereço | O que faz |
|--------|----------|-----------|
| GET | /produtos | Lista todos os produtos |
| POST | /produtos | Cadastra um produto |
| PUT | /produtos/1 | Edita o produto de ID 1 |
| DELETE | /produtos/1 | Exclui o produto de ID 1 |
| GET | /pedidos | Lista todos os pedidos |
| POST | /pedidos | Registra um pedido |
| DELETE | /pedidos/1 | Cancela o pedido de ID 1 |
| POST | /estoque/entrada | Registra entrada de produtos |
| POST | /estoque/saida | Registra saída de produtos |
| GET | /estoque | lista o estoque atual |
| GET | /relatorios/estoque | Relatório de estoque atual |
| GET | /relatorios/vendas | Relatório de vendas |
| GET | /relatorios/dashboard | Resumo do dashboard |

---

## Tecnologias utilizadas

- **Python 3.11** — linguagem de programação
- **Flask** — servidor web
- **SQLite** — banco de dados
- **HTML + Bootstrap 5** — interface do usuário
- **AdminLTE** — template de administração

---

Desenvolvido por Matheus Aurelio Canaparro da Silva
Faculdade Dom Bosco — Porto Alegre/RS
