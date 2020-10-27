# encoding: utf-8

from pytube import YouTube
from datetime import datetime

class YoutubeDownloader:
    def __init__(self):
        self.y = None  # Instância do Youtube
        self.resolucoes = None

    def criar_instancia(self, url):
        try:
            self.y = YouTube(url)
        except Exception as e:
            pass
            #self.mensagem(e)

    def analisar_videos(self, url):
        self.criar_instancia(url)

        resolucoes = []

        try:
            d_video = self.y.streams.filter(progressive=True)

            for resolucao in d_video:
                a = str(resolucao)
                a = a.split('res="')[1]
                a = a.split('"')[0]
                #print('Resoluções para {}:\t{}'.format(url, a))
                resolucoes.append(a)
        except Exception as e:
            self.mensagem('NOK: {}:\t{} '.format(url, e))

        if len(resolucoes) > 0:
            resolucoes.sort(reverse=True)
            return resolucoes
        else:
            return False

    def baixar(self, url, resolucao):
        '''
        Método que, de fato, baixa o vídeo.

        :param url:
        :param resolucao:
        :return:
        '''

        try:
            self.mensagem('Vídeo {} [{}]'.format(url, resolucao))
            self.criar_instancia(url)
            file_name = self.y.title
            d_video = self.y.streams.filter(progressive=True, resolution=resolucao)
            d = d_video.get_highest_resolution()
            d.download()
            self.mensagem('OK  {}\t{} : {}'.format(url, file_name, resolucao))
            return True
        except Exception as e:
            self.mensagem('NOK {}\t: {}, {}'.format(url, resolucao, e))
            return False

    def baixar_videos(self):
        '''
        Baixa os vídeos que estão com o link salvo no arquivo lista_de_videos.txt.
        Procura baixar o arquivo na melhor resolução possível.

        :return:
        '''
        videos = open('lista_de_videos.txt')
        for video in videos:
            video = self.tratar_url(video)
            resolucoes = self.analisar_videos(video)
            if not resolucoes:
                self.mensagem('O link {} não tem resoluções disponíveis.'.format(video[:-1]))
            else:
                for res in resolucoes:
                    if self.baixar(video, res):
                        if len(resolucoes) > 1:
                            break

        videos.close()

    def tratar_url(self, url):
        '''
        Remove os dados referentes a playlists e retorna a URL sem qualquer parâmetro de GET.

        :param url: string
        :return: string
        '''

        n = url.split('&')
        return n[0]

    def mensagem(self, mensagem):
        hora = datetime.now()
        h = str(hora.hour).zfill(2)
        m = str(hora.minute).zfill(2)
        s = str(hora.second).zfill(2)

        print('{}:{}:{}\t{}'.format(h, m, s, mensagem))

downloader = YoutubeDownloader()
downloader.baixar_videos()
