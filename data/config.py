from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
CHANNEL = env.str("CHANNEL")
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

QIWI_TOKEN = env.str('qiwi')
WALLET_QIWI = env.str('wallet')
QIWI_PUBKEY = env.str('qiwi_p_pub')



PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASSWORD")
DB_NAME = env.str("DATABASE")
DB_HOST = env.str("DB_HOST")


POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{IP}/{DB_NAME}"
