# OCR Router Pipeline 🏛️

Um sistema completo de processamento de imagens que integra OCR, LLM e persistência em base de dados.

## Arquitetura Global: O Pipeline de Dados

Equivalente a um fluxo UNIX: **Imagem → OCR → LLM → Filtro → Base de Dados**

Em vez de passarmos bytes brutos por pipes anónimos, usamos Python para passar objetos estruturados na memória RAM entre módulos isolados.

### Módulo 1: Isolamento do Sistema
- **Virtual Environment (.venv)**: Ambiente isolado onde o pip instala pacotes apenas para este projeto
- Sem poluição do sistema operativo base

### Módulo 2: Extrator OCR
- **Pillow**: Carrega a imagem para um buffer de memória
- **pytesseract**: Wrapper para o motor C++ do Tesseract
- Tratamento de exceções: `UnidentifiedImageError`, falhas de executável

### Módulo 3: Parser Semântico
- **OpenAI API**: Lê o texto sujo do OCR
- **Pydantic**: Estrutura os dados de forma determinística
- Validação de tipos em tempo de execução

### Módulo 4: Persistência de Dados
- **SQLite3**: Base de dados In-Process
- **Queries Parametrizadas**: Protecção contra SQL Injection

## Estrutura do Projeto

```
ocr_router_pipeline/
├── .venv/                    # Virtual Environment
├── inputs/                   
│   ├── sample1.png           # Imagens para processar
│   ├── sample2.png
│   └── ...
├── ocr_extractor.py          # Módulo OCR
├── llm_parser.py             # Módulo LLM + Pydantic
├── db_writer.py              # Módulo SQLite
└── main.py                   # Orquestrador
```

## Setup Inicial

```bash
# Clonar o repositório
git clone https://github.com/spaderale/ocr_router_pipeline.git
cd ocr_router_pipeline

# Criar e ativar Virtual Environment
python3 -m venv .venv
source .venv/bin/activate  # no Windows: .venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Executar o Pipeline

```bash
python main.py
```

## Dependências

- `Pillow`: Processamento de imagens
- `pytesseract`: OCR
- `openai`: API do LLM
- `pydantic`: Validação de dados
- `python-dotenv`: Variáveis de ambiente

---

**Transição de C para Python**: Este projeto demonstra abstrações de alto nível sem perder noção do que está a acontecer na memória e no disco. 🚀
