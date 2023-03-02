import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials



#   Rodar no terminal gitbash 
# export SPOTIPY_CLIENT_ID='seu-client-id'
# export SPOTIPY_CLIENT_SECRET='seu-client-secret'
# export SPOTIPY_REDIRECT_URI='seu-localhost-callback'



options = Options()
options.add_experimental_option("detach", True)

CHAVE_API = "sua-chave-API"

bot = telebot.TeleBot(CHAVE_API)


username = 'Luan Torres'
scope = 'playlist-modify-public', 'user-library-modify', ''
playlist_id = 'url-da-sua-playlist'
linkedin_url = 'https://www.linkedin.com/in/luan-h-torres/'



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id='-seu-client-id',
                                   client_secret='seu-client-secret',
                                   redirect_uri='seu-localhost-callback')




@bot.message_handler(commands=["criar_playlist_nome"])
def criar_playlist_nome(mensagem):    
    enviar = bot.send_message(mensagem.chat.id, 'Qual nome do artista?')
    bot.register_next_step_handler(enviar, hello)
    



@bot.message_handler(commands=["qtd_musicas"])
def qtd_musicas_limit(mensagem):    
    enviar2 = bot.send_message(mensagem.chat.id, 'Quantas músicas deseja adicionar?')
    bot.register_next_step_handler(enviar2, criar_limits)

 

def hello(mensagem):
    open('artistas.txt', 'w').write(mensagem.text)
    bot.send_message(mensagem.chat.id, 'Obrigado pelo nome do artista!')
    texto = """
    /qtd_musicas
    """
    bot.send_message(mensagem.chat.id, texto)
    
    
    
def criar_limits(mensagem):
    open('limits.txt', 'w').write(mensagem.text)
    bot.send_message(mensagem.chat.id, 'Obrigado pela quantidade de músicas!')
    bot.send_message(mensagem.chat.id, 'Criando playlist...')
    bot.send_message(mensagem.chat.id, 'Link da playlist: ' + playlist_id)
    criar_playlist()



def criar_playlist():
    limitsFile = open('limits.txt', 'r')
    limit = [y for y in limitsFile.readlines()]

    artistasFile = open('artistas.txt', 'r')
    artista = [x for x in artistasFile.readlines()]
    tracks = []
    numeroArtistas = len(artista)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False

        for x in range(0, numeroArtistas):
            result = sp.search(artista[x], limit=tuple(limit))
            for i, t in enumerate(result['tracks']['items']):
                tracks.append(str(t['id'].strip( 'u' )))
                print("adicionando a track", t['id'], t['name'])
        while tracks:
            try:
                result = sp.user_playlist_add_tracks(username, playlist_id, tracks[:1])
            except:
                print("erro")
            tracks = tracks[1:]
        
    else:
        print("Can't get token for", username)


@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    texto = """
    O que você quer? (Clique em uma opção)
    /criar_playlist_nome Criar uma playlist com um nome de artista
    """
    bot.send_message(mensagem.chat.id, texto)


@bot.message_handler(commands=["opcao2"])
def opcao1(mensagem):
    texto = """
    O bot está sempre a sua disposição!
    """
    bot.send_message(mensagem.chat.id, texto)


@bot.message_handler(commands=["opcao3"])
def opcao1(mensagem):
    bot.send_message(mensagem.chat.id, 'Link do linkedin: ' + linkedin_url)
    


def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
     /opcao1 Fazer uma playlist
     /opcao2 Agradecer o bot!
     /opcao3 Me siga no Linkedin
     """
    bot.reply_to(mensagem, texto)

bot.polling()   