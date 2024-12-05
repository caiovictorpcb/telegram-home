# Canais Telegram + HomeBroker Bot  

Este projeto é um script automatizado para processar mensagens do Telegram relacionadas a oportunidades de trade e executar operações automaticamente na plataforma **Home Broker**. Ele é ideal para automatizar a entrada em operações com base em sinais enviados por grupos de Telegram.  

---

## 🛠️ Funcionalidades  
- 📥 **Monitoramento de Mensagens**: Escuta mensagens de grupos específicos no Telegram e identifica sinais de trade.  
- 🤖 **Automação de Trades**: Realiza operações de compra ou venda automaticamente com base nas informações extraídas.  
- 🔄 **Reagendamento Inteligente**: Reagenda operações falhas até 3 tentativas.  
- 🔐 **Atualização de Credenciais**: Garante que as credenciais da API do Home Broker estejam sempre atualizadas.  

---

## 🗂️ Estrutura do Projeto  

### Arquivos principais  
- **`main.py`**  
  - Script principal que conecta ao Telegram, escuta mensagens e agenda operações automaticamente com base em sinais recebidos.  
  - Gerencia tentativas e resultados de trades, reagendando em caso de falha.  

- **`home_broker.py`**  
  - Integração com a API do Home Broker para autenticação, execução e monitoramento de operações.  
  - Inclui o uso de **Google Gemini** para processar mensagens e extrair informações relevantes.  

---

## ✅ Pré-requisitos  

### Dependências  
Certifique-se de instalar as seguintes bibliotecas antes de executar o projeto:  
- [Telethon](https://github.com/LonamiWebs/Telethon)  
- [LangChain](https://github.com/hwchase17/langchain)  
- [Requests](https://docs.python-requests.org/en/latest/)  
- [Python-dotenv](https://github.com/theskumar/python-dotenv)  

Instale-as com o seguinte comando:  
```bash
pip install telethon langchain requests python-dotenv
```  

### Variáveis de Ambiente  
Crie um arquivo `.env` no diretório do projeto e adicione as seguintes variáveis:  
```env
TELEGRAM_API_ID=<seu_telegram_api_id>
TELEGRAM_API_HASH=<seu_telegram_api_hash>
HOME_BROKER_EMAIL=<seu_email>
HOME_BROKER_PASSWORD=<sua_senha>
```  

---

## 🚀 Como Executar  

Siga os passos abaixo para configurar e executar o bot:  

1. **Clone o repositório**:  
   ```bash
   git clone https://github.com/seu-usuario/telegram-trade-bot.git
   cd telegram-trade-bot
   ```  

2. **Configure as variáveis de ambiente**:  
   Crie o arquivo `.env` no diretório do projeto e adicione suas credenciais conforme mostrado acima.  

3. **Execute o bot**:  
   ```bash
   python main.py
   ```  

O bot conectará ao Telegram, começará a monitorar mensagens e executará operações automaticamente.  

---

## 📃 Licença  
Este projeto está licenciado sob a [MIT License](LICENSE).  

---

## 🤝 Contribuições  
Contribuições são sempre bem-vindas! Se você encontrou um problema ou tem uma ideia para melhorar o projeto, abra uma issue ou envie um pull request.  

---

## 🙋‍♂️ Autor  
Desenvolvido por **[Caio Victor]**.  

---

## ⚠️ Aviso Legal  
Este projeto é fornecido "como está" e deve ser utilizado com responsabilidade. **O autor não se responsabiliza por perdas financeiras decorrentes do uso deste software.** Teste rigorosamente antes de utilizá-lo em ambientes reais.  
