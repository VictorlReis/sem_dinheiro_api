# Use a imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências Python
RUN pip install -r requirements.txt

# Copie o restante do aplicativo para o contêiner
COPY . .

# Exponha a porta em que a aplicação FastAPI estará em execução
EXPOSE 8000

# Comando para executar o aplicativo FastAPI
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
