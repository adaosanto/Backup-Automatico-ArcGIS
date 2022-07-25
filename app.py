from time import strftime
from arcgis.gis import GIS
import os


class Backup:
    def __init__(self, usuario, senha, item_id, nome, portal_url):
        self.usuario = usuario
        self.senha = senha
        self.item_id = item_id
        self.nome = nome
        self.gis_portal_url = portal_url

    @property
    def format_name(self):
        return self.nome.title().strip()

    @property
    def nome_backup(self):
        return strftime(f"{self.format_name}_%m_%d_%y")

    # Criar o arquivo de Backup
    def criar_backup(self):
        self.__gis = GIS(
            self.gis_portal_url,  # https://url_portal/home/item.html?id=
            self.usuario,
            self.senha,
        )
        print(f"Iniciando dowload de {self.format_name}")
        self.__dataItem = self.__gis.content.get(self.item_id)
        self.__dataItem.export(
            self.nome_backup,
            "File Geodatabase",  # Saida do arquivo [Shape File, File Geodatabase, Excel ...]
            parameters=None,
            wait=True,
        )
        self.__myexport = self.__gis.content.search(
            self.nome_backup, item_type="File Geodatabase"
        )  # Procuar o arquivo de backup dentro do servidor web
        self.__fgdb = self.__gis.content.get(self.__myexport[0].itemid)

    def download(self):
        self.saida = r"E:\Servidor Web - BKP\SMPC - Planejamento e Cidade\Backups Automaticos"  # Seta o local de saida
        self.__fgdb.download(
            save_path=self.saida
        )  # Faz o download do arquivo o servidor
        print(f"Download concluido de {self.format_name} em {strftime('%c')}")

    def delete_backup(
        self,
    ):  # Após o download, deletamos o arquivo de dowloando dentro do servidor web (MUITO CUIDADO)
        self.__fgdb.delete()


app = Backup(
    usuario=os.environ["ARCGIS_USUARIO_ROOT"],
    senha=os.environ["ARCGIS_SENHA_ROOT"],
    item_id="67f721d6664c4a0ca2a07ac13963974d",  # State Geologic Map Compilation – Structure
    nome="State Geologic Map Compilation – Structure",
    portal_url=os.environ["PORTAL_GIS_URL"],
)
app.criar_backup()
app.download()
app.delete_backup()
