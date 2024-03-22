import time
import warnings
import pandas as pd

from unidade_medida_tempo import UnidadeMedidaTempo

'''
TempoTracker: A classe base que fornece funcionalidades para rastrear o tempo.

agora(): Retorna o tempo atual.
start(): Define o tempo de início para rastreamento.
restart(): Define novamente o tempo de início para rastreamento.
calcular_tempo_decorrido(): Calcula o tempo decorrido desde o início na unidade especificada.
converter_tempo(): Converte o tempo decorrido para a unidade especificada.
mostrar_resultados(): Imprime o DataFrame armazenado.
mostrar_resultados_id(_id): Imprime as linhas do DataFrame com um ID específico.
mostrar_resultados_matricula(matricula_id): Imprime as linhas do DataFrame com uma matrícula específica.
adicionar_df(df): Adiciona um DataFrame ao DataFrame existente.
adicionar_matricula_df(_id, matricula_id): Adiciona um ID de matrícula a uma linha específica no DataFrame.

'''
class TempoProcessamentoTracker:
    inicio: float
    decorrido_atual: float
    decorrido_anterior: float
    colunas_df: list
    df: pd.DataFrame
    unidade_medida: UnidadeMedidaTempo

    def __init__(self, unidade_medida = UnidadeMedidaTempo.SEGUNDOS, quantidade_casas_decimais = 3):
        self.start()
        self.colunas_df = ['id', 'matricula_id', 'descricao', 'tempo', 'nivel', 'percentual_tempo']
        self.df = pd.DataFrame(columns=self.colunas_df)
        self.decorrido_atual = 0.0
        self.decorrido_anterior = 0.0
        self.unidade_medida = unidade_medida
        self.quantidade_casas_decimais = quantidade_casas_decimais
        self.id = 0
        
    def agora(self):
        return time.time()
        
    def start(self):
        self.inicio = self.agora()
    
    def restart(self):
        self.start()
        
    def calcular_tempo_decorrido(self):
        tempo_decorrido = self.agora() - self.inicio
        return self.converter_tempo(tempo_decorrido)
    
    def converter_tempo(self, tempo):
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
        print()
        print(self.df)
        print()
    
    def mostrar_resultados_id(self, _ids = None):
        print()
        if _ids == None:
            _ids = list(self.id)

        if isinstance(_ids, list):
            print(self.df.loc[self.df['id'].isin(_ids)])
        else:
            raise ValueError("_ids deve ser uma lista")
        
        print()

    def mostrar_resultados_nivel(self, _ids, niveis):
        print()

        if isinstance(_ids, list) and isinstance(niveis, list):
            print(self.df.loc[self.df['id'].isin(_ids) & self.df['nivel'].isin(niveis)])
        else:
            raise ValueError("_ids e niveis deve uma lista")
        
        print()
    
    def mostrar_resultados_matricula(self, matriculas_id):
        print()

        if isinstance(matriculas_id, list):
            print(self.df.loc[self.df['matricula_id'].isin(matriculas_id)])
        else:
            raise ValueError("matriculas_id deve ser uma lista")
        
        print()

    def adicionar_df(self, df):
        # Suprimir o aviso
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)

            self.df = pd.concat([self.df, df], ignore_index=True)

    def adicionar_matricula_df(self, matricula_id, _ids = None):
        if _ids == None:
           _ids = list(self.id)

        if isinstance(_ids, list):
            self.df.loc[self.df['id'].isin(_ids), 'matricula_id'] = matricula_id
        else:
            raise ValueError("_ids deve ser uma lista")
    
    def incrementar_id(self):
        self.id += 1

    def calcular_percentual_tempo(self, nivel, _id = None):
        if(_id == None):
            _id = self.id

        df_filtrado = self.df[(self.df['id'] == _id) & (self.df['nivel'] == nivel)].copy()

        total_tempo = df_filtrado['tempo'].sum()
        
        df_filtrado.loc[:, 'percentual_tempo'] = round((df_filtrado['tempo'] / total_tempo) * 100, self.quantidade_casas_decimais)

        self.df.update(df_filtrado)

    def calcular_percentual_tempo_todos(self):
        for id in self.df['id'].unique():
            for nivel in self.df['nivel'].unique():
                self.calcular_percentual_tempo(nivel, id)
    
    def exportar_df(self, path, extensao):
        path = path + '.' + extensao
        if(extensao == 'csv'):
            self.df.to_csv(path)
        elif(extensao == 'xlsx'):
            self.df.to_excel(path)
        else:
            raise ValueError("Extensão inválida")
        print(f'Arquivo exportado para {path}')