import pandas as pd
import numpy as np
from tempo_processamento_tracker import TempoProcessamentoTracker

class TempoProcessamentoTrackerIntermitente(TempoProcessamentoTracker):
    """
    Classe para calcular o tempo decorrido intermitentes entre eventos.

    Esta classe estende a funcionalidade da classe base TempoProcessamentoTracker
    e adiciona métodos específicos para calcular o tempo decorrido intermitentes entre eventos.

    Methods:
        calcular_delta: Calcula o tempo decorrido intermitentes entre eventos e adiciona o registro ao DataFrame.
    """

    def calcular_delta(self, descricao, nivel, _id = None, item_id = None, incrementar_id = False):
        """
        Calcula o tempo decorrido intermitentes entre eventos e adiciona o registro ao DataFrame.

        Args:
            descricao (str): Descrição do evento.
            nivel (str): Nível do evento.
            _id (int, optional): O identificador do evento. Se não for fornecido, será usado o ID atual da instância.
            item_id (int, optional): O identificador do item associado ao evento.
            incrementar_id (bool, optional): Se True, incrementa o ID antes de adicionar o registro (padrão: False).

        Returns:
            None
        """
        if incrementar_id:
            self.incrementar_id()
        
        #Caso não seja passado _id pela função, usar o id da classe
        if(_id == None):
            _id = self.id

        decorrido_atual = self.calcular_tempo_decorrido()
        self.decorrido_anterior = self.decorrido_atual
        self.decorrido_atual = decorrido_atual 

        tempo_decorrido = self.decorrido_atual - self.decorrido_anterior 
        tempo_decorrido = round(max(tempo_decorrido, 0), self.quantidade_casas_decimais)

        df_data = pd.DataFrame({'id': [_id], 'item_id':[item_id], 'descricao': [descricao], 'tempo': [tempo_decorrido], 'nivel': [nivel], 'percentual_tempo' : [np.nan]})

        self.adicionar_df(df_data)