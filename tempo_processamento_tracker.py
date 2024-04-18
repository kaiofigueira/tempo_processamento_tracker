import time
import warnings
import pandas as pd
import copy
import os

from unidade_medida_tempo import UnidadeMedidaTempo

class TempoProcessamentoTracker:
    """
    Uma classe para rastrear o tempo decorrido entre eventos e manter os registros em um DataFrame.

    Attributes:
        inicio (float): O tempo de início do rastreamento.
        decorrido_atual (float): O tempo decorrido atual desde o início.
        decorrido_anterior (float): O tempo decorrido anterior desde o início.
        colunas_df (list): Uma lista das colunas do DataFrame.
        df (pd.DataFrame): O DataFrame para armazenar os registros de tempo.
        unidade_medida (UnidadeMedidaTempo): A unidade de medida para o tempo (padrão: segundos).
        quantidade_casas_decimais (int): A quantidade de casas decimais para arredondamento (padrão: 3).
        id (int): O identificador único para os registros de tempo.
        nivel (int): para casos em que queira medir o tempo dentro de funções que chama outras funções.
    
    Methods:
            agora(): Retorna o tempo atual.
            start(): Define o tempo de início para rastreamento.
            restart(): Define novamente o tempo de início para rastreamento.
            calcular_tempo_decorrido(): Calcula o tempo decorrido desde o início na unidade especificada.
            converter_tempo(): Converte o tempo decorrido para a unidade especificada.
            mostrar_resultados(): Mostra o DataFrame armazenado.
            mostrar_resultados_id(_ids): Mostra os resultados filtrados por IDs do DataFrame.
            mostrar_resultados_nivel(self, _ids, niveis): Mostra os resultados filtrados por IDs e níveis.
            mostrar_resultados_itens(itens_id): Mostra os resultados filtrados por IDs de item.
            adicionar_df(df): Adiciona um DataFrame ao DataFrame existente.
            adicionar_item_df(self, item_id, _ids): Adiciona um ID de item em linhas específicas no DataFrame.
            incrementar_id(self): Incrementa + 1 ao ID.
            calcular_percentual_tempo(self, nivel, _id = None): Calcula o percentual de tempo de processamento para um nível e _id específicos.
            calcular_percentual_tempo_todos(self): Calcula o percentual de tempo de processamento para todos os registros do DataFrame.
            exportar_df(self, path): Exporta o DataFrame para um arquivo csv ou xlsx.
            copy(self): Cria uma cópia do objeto.
    """

    inicio: float
    decorrido_atual: float
    decorrido_anterior: float
    colunas_df: list
    df: pd.DataFrame
    unidade_medida: UnidadeMedidaTempo

    def __init__(self, unidade_medida = UnidadeMedidaTempo.SEGUNDOS, quantidade_casas_decimais = 3):
        """
        Inicializa uma instância de TempoProcessamentoTracker.

        Args:
            unidade_medida (UnidadeMedidaTempo, optional): A unidade de medida para o tempo (padrão: segundos).
            quantidade_casas_decimais (int, optional): A quantidade de casas decimais para arredondamento (padrão: 3).
        """
        self.start()
        self.colunas_df = ['id', 'item_id', 'descricao', 'tempo', 'nivel', 'percentual_tempo']
        self.df = pd.DataFrame(columns=self.colunas_df)
        self.decorrido_atual = 0.0
        self.decorrido_anterior = 0.0
        self.unidade_medida = unidade_medida
        self.quantidade_casas_decimais = quantidade_casas_decimais
        self.id = 0
        
    def agora(self):
        """
        Obtém o tempo atual em segundos.

        Args:
            None

        Returns:
            float: O clock atual.
        """
        return time.time()
        
    def start(self):
        """
        Define o tempo de início para rastreamento.

        Args:
            None

        Returns:
            float: O clock atual.
        """
        self.inicio = self.agora()
    
    def restart(self):
        """
        Define novamente o tempo de início para rastreamento.

        Args:
            None

        Returns:
            float: O clock atual.
        """
        self.start()
        
    def calcular_tempo_decorrido(self):
        """
        Calcula o tempo decorrido desde o início na unidade especificada.

        Args:
            None

        Returns:
            float: O tempo decorrido em segundos.
        """
        tempo_decorrido = self.agora() - self.inicio
        return self.converter_tempo(tempo_decorrido)
    
    def converter_tempo(self, tempo):
        """
        Converte o tempo para a unidade de medida especificada.

        Args:
            tempo (float): O tempo a ser convertido.

        Returns:
            float: O tempo convertido.
        """

        if(self.unidade_medida == UnidadeMedidaTempo.MILISEGUNDOS):
            return tempo * 1000
        elif self.unidade_medida == UnidadeMedidaTempo.SEGUNDOS:
            return tempo
        elif self.unidade_medida == UnidadeMedidaTempo.MINUTOS:
            return tempo / 60
        elif self.unidade_medida == UnidadeMedidaTempo.HORAS:
            return tempo / 3600
        else:
            print("Unidade de medida não definida.")
            return None

    def mostrar_resultados(self):
        """
        Mostra o DataFrame armazenado.

        Args:
            None

        Returns:
            None
        """
        print()
        print(self.df)
        print()
    
    def mostrar_resultados_id(self, _ids = None):
        """
        Mostra os resultados filtrados por IDs.

        Args:
            _ids (list, optional): Uma lista de IDs a serem filtrados. Se None, todos os IDs serão mostrados.

        Returns:
            None

        Raises:
            ValueError: Se _ids não for uma lista
        """
        print()
        if _ids == None:
            _ids = list(self.id)

        if isinstance(_ids, list):
            print(self.df.loc[self.df['id'].isin(_ids)])
        else:
            raise ValueError("_ids deve ser uma lista")
        
        print()

    def mostrar_resultados_nivel(self, _ids, niveis):
        """
        Mostra os resultados filtrados por IDs e níveis.

        Args:
            _ids (list): Uma lista de IDs a serem filtrados.
            niveis (list): Uma lista de níveis a serem filtrados.

        Returns:
            None

        Raises:
            ValueError: Se _ids e niveis não forem uma lista
        """
        print()

        if isinstance(_ids, list) and isinstance(niveis, list):
            print(self.df.loc[self.df['id'].isin(_ids) & self.df['nivel'].isin(niveis)])
        else:
            raise ValueError("_ids e niveis deve uma lista")
        
        print()
    
    def mostrar_resultados_itens(self, itens_id):
        """
        Mostra os resultados filtrados por IDs de item.

        Args:
            itens_id (list): Uma lista de IDs de matrícula a serem filtrados.

        Returns:
            None

        Raises:
            ValueError: Se itens_id não for uma lista
        """
        print()

        if isinstance(itens_id, list):
            print(self.df.loc[self.df['item_id'].isin(itens_id)])
        else:
            raise ValueError("itens_id deve ser uma lista")
        
        print()

    def adicionar_df(self, df):
        """
        Adiciona um DataFrame ao DataFrame existente.

        Args:
            df (pd.DataFrame): O DataFrame a ser adicionado.

        Returns:
            None
        """
        # Suprimir o aviso
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)

            self.df = pd.concat([self.df, df], ignore_index=True)

    def adicionar_item_df(self, item_id, _ids = None):
        """
        Adiciona um ID de item em linhas específicas no DataFrame.

        Args:
            item_id: O ID da item a ser adicionado.
            _ids (list, optional): Uma lista de IDs a serem filtrados. Se None, todos os IDs serão considerados.
        
        Returns:
            None

        Raises:
            ValueError: Se _ids não satisfazer o tipo esperando pela função
        """

        if isinstance(_ids, list):
            self.df.loc[self.df['id'].isin(_ids), 'item_id'] = item_id
        elif _ids == None:
            self.df['item_id'] = item_id
        else:
            raise ValueError("_ids inválido")
    
    def incrementar_id(self):
        """
        Incrementa + 1 ao ID.

        Args:
            None

        Returns:
            None
        """
        self.id += 1

    def calcular_percentual_tempo(self, nivel, _id = None):
        """
        Calcula o percentual de tempo de processamento para um nível e _id específicos.

        Args:
            nivel: O nível para o qual calcular o percentual de tempo.
            _id (int, optional): O ID para o qual calcular o percentual de tempo. Se None, utiliza o ID atual.
        
        Returns:
            None
        """

        if(_id == None):
            _id = self.id

        df_filtrado = self.df[(self.df['id'] == _id) & (self.df['nivel'] == nivel)].copy()

        total_tempo = df_filtrado['tempo'].sum()
        
        df_filtrado.loc[:, 'percentual_tempo'] = round((df_filtrado['tempo'] / total_tempo) * 100, self.quantidade_casas_decimais)

        self.df.update(df_filtrado)

    def calcular_percentual_tempo_todos(self):
        """
        Calcula o percentual de tempo de processamento para todos os registros do DataFrame.
        
        Args:
            nivel: O nível para o qual calcular o percentual de tempo.
            _id (int, optional): O ID para o qual calcular o percentual de tempo. Se None, utiliza o ID atual.
        
        Returns:
            None
        """
        for id in self.df['id'].unique():
            for nivel in self.df['nivel'].unique():
                self.calcular_percentual_tempo(nivel, id)
    
    def exportar_df(self, path):
        """
        Exporta o DataFrame para um arquivo csv ou xlsx.

        Args:
            path (str): O caminho do arquivo de destino.
        
        Returns:
            None

        Raises:
            ValueError: Se a extensão do arquivo não for csv ou xlsx.
        """

        extensao = os.path.splitext(path)[1][1:]

        if extensao == 'csv':
            self.df.to_csv(path)
        elif extensao == 'xlsx':
            self.df.to_excel(path)
        else:
            raise ValueError("Extensão inválida")
        
        print(f'Arquivo exportado para {path}')

    def copy(self):
        """
        Cria uma cópia do objeto.

        Args:
            None

        Returns:
            Objeto: Uma nova instância do objeto.
        """

        # Cria uma nova instância do objeto passado.
        new_instance = copy.deepcopy(self)
        
        return new_instance