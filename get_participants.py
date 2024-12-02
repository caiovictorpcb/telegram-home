from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from collections import Counter

# Função para pegar os seguidores de uma conta
def get_following(driver, username, password, target_account):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    # Login
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
    time.sleep(5)

    # Acessar o perfil da conta
    driver.get(f"https://www.instagram.com/{target_account}/")
    time.sleep(3)

    # Clicar na lista de pessoas seguidas
    following_button = driver.find_element(By.PARTIAL_LINK_TEXT, "seguindo")
    following_button.click()
    time.sleep(3)

    # Rolar a lista de seguidos
    modal = driver.find_element(By.XPATH, "//div[@role='dialog']")
    following_accounts = set()
    for _ in range(10):  # Ajuste o número de rolagens
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
        time.sleep(2)

    # Coletar os nomes de usuários das contas seguidas
    following_elements = modal.find_elements(By.XPATH, "//a[contains(@href, '/')]")
    for elem in following_elements:
        following_accounts.add(elem.text)

    return following_accounts

# Configurar o WebDriver
driver = webdriver.Chrome(executable_path="caminho/para/chromedriver")

# Informações do login
username = "seu_username"
password = "sua_senha"

# Lista de contas para verificar
accounts = ["account1", "account2", "account3"]

# Dicionário para contar as contas seguidas
followed_accounts = []

for account in accounts:
    followed_accounts.extend(get_following(driver, username, password, account))

# Contabilizar as contas seguidas
account_counts = Counter(followed_accounts)

# Ordenar e exibir as contas mais seguidas
most_followed = account_counts.most_common()
print("Contas mais seguidas:")
for account, count in most_followed:
    print(f"{account}: {count} vezes")

driver.quit()
