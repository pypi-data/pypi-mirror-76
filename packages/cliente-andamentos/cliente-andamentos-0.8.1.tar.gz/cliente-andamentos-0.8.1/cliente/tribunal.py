#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cliente import BaseAPI


class Tribunais(BaseAPI):

    def __init__(self, token, url=BaseAPI.URL_DEFAULT):
        super(Tribunais, self).__init__(token, url)
        self.tribunais = None

    def _obtem_dados(self):
        resposta = self.executa_tribunal()
        self.valida_resposta(resposta)
        return resposta.json()

    def _tribunal_por_sigla(self, sigla):
        #  Busca o tribunal buscando pela sigla
        for tribunal in self.tribunais:
            if sigla.upper() == tribunal['sigla'].upper():
                return tribunal
        return None

    def _tribunal_por_numero(self, numero):
        #  Busca o tribunal buscando pelo número
        for tribunal in self.tribunais:
            if numero == tribunal['numero']:
                return tribunal
        return None

    def obtem(self, tribunal):
        if not self.tribunais:
            self.tribunais = self._obtem_dados()
        t = self._tribunal_por_sigla(tribunal) or self._tribunal_por_numero(tribunal)
        if t:
            return Tribunal(t['numero'], t)
        raise KeyError('Este parâmetro não consta como um tribunal válido')

    def obtem_tribunais(self):
        return self._obtem_dados()

    def obtem_sistemas_em_manutencao(self):
        resposta = self.executa_sistemas_em_manutencao()
        self.valida_resposta(resposta)
        return resposta.json()

    def completamente_suportado(self, tribunal):
        try:
            t = self.obtem(tribunal)
            if any([not s.status_cnj == 'SUPORTADO' for s in t.sistemas]):
                return False
        except KeyError:
            return False
        return True

    def parcialmente_suportado(self, tribunal):
        t = self.obtem(tribunal)
        nenhum_suportado = all([not s.status_cnj == 'SUPORTADO' for s in t.sistemas])
        todos_suportados = all([s.status_cnj == 'SUPORTADO' for s in t.sistemas])
        if nenhum_suportado or todos_suportados:
            return False
        return True

    def em_manutencao(self, tribunal):
        tribunal = self.obtem(tribunal)
        for sistema in tribunal.sistemas:
            if sistema.status_cnj == 'MANUTENCAO' or sistema.status_oab == 'MANUTENCAO':
                return True
        return False

    def por_estado(self, estado):
        if not self.tribunais:
            self.tribunais = self._obtem_dados()
        return [str(tr['sigla']).upper()
                for tr in self.tribunais
                if estado.upper() in tr['estados']]


class Tribunal:

    def __init__(self, tribunal_numero, tribunal_info):
        self.numero = tribunal_numero
        self.sigla = tribunal_info['sigla']
        self.estados = tribunal_info['estados']
        self.nome = tribunal_info['nome']
        self.sistemas = []
        for sistema in tribunal_info['sistemas']:
            self.sistemas.append(SistemaTribunal(sistema))


class SistemaTribunal:

    def __init__(self, info):
        self.nome = info['nome']
        self.status_cnj = info['status_cnj']
        self.status_oab = info['status_oab']
