import pandas as pd
import numpy as np
from tempo_processamento_tracker import TempoProcessamentoTracker

'''
TempoTrackerConsecutivo: Uma subclasse de TempoTracker para rastrear o tempo entre eventos consecutivos.

calcular_delta(_id, descricao, nivel, matricula_id, incrementar_id): Calcula e armazena o tempo decorrido entre eventos consecutivos.

'''
class TempoProcessamentoTrackerConsecutivo(TempoProcessamentoTracker):
    #Este método calcula o tempo decorrido entre eventos consecutivos.
    def calcular_delta(self, descricao, nivel, _id = None, matricula_id = None, incrementar_id = False):
        if incrementar_id:
            self.incrementar_id()
        
        #Caso não seja passado _id pela função, usar o id da classe
        if(_id == None):
            _id = self.id

        tempo_decorrido = self.calcular_tempo_decorrido()
        tempo_decorrido = round(max(tempo_decorrido, 0), self.quantidade_casas_decimais)

        df_data = pd.DataFrame({'id': [_id], 'matricula_id':[matricula_id], 'descricao': [descricao], 'tempo': [tempo_decorrido], 'nivel': [nivel], 'percentual_tempo' : [np.nan]})

        self.adicionar_df(df_data)
        
    def copy(self):
        # Cria uma nova instância de TempoProcessamentoTrackerConsecutivo
        new_instance = TempoProcessamentoTrackerConsecutivo()
        
        # Copia os atributos
        new_instance.inicio = self.inicio
        new_instance.decorrido_atual = self.decorrido_atual
        new_instance.decorrido_anterior = self.decorrido_anterior
        new_instance.colunas_df = self.colunas_df
        new_instance.df = self.df.copy()
        new_instance.unidade_medida = self.unidade_medida
        new_instance.quantidade_casas_decimais = self.quantidade_casas_decimais
        new_instance.id = self.id
        
        return new_instance