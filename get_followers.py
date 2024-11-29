import instaloader

# Inicializando o instaloader
loader = instaloader.Instaloader()

# Login na conta (necessário para acessar seguidores de contas privadas)
USERNAME = "seu_usuario"
PASSWORD = "sua_senha"
loader.login(USERNAME, PASSWORD)

# Nome da conta que você quer obter os seguidores
target_account = "nome_da_conta"

# Obter perfil
profile = instaloader.Profile.from_username(loader.context, target_account)

# Listar seguidores
print(f"Seguidores de {target_account}:")
for follower in profile.get_followers():
    print(follower.username)
