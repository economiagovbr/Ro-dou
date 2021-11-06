""" Parsers unit tests
"""

import os
import sys
import inspect

import pytest

import pandas as pd

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from dou_dag_generator import DouDigestDagGenerator, YAMLParser

@pytest.mark.parametrize(
    'dag_id, size, hashed',
    [
        ('unique_id_for_each_dag', 60, 56),
        ('generates_sparses_hashed_results', 120, 59),
        ('unique_id_for_each_dag', 10, 6),
        ('', 10, 0),
        ('', 100, 0),
    ])
def test_hash_dag_id(yaml_parser, dag_id, size, hashed):
    assert yaml_parser._hash_dag_id(dag_id, size) == hashed

@pytest.mark.parametrize(
    'filepath, result_tuple',
    [
        ('basic_example.yaml',
         (
             'basic_example',
             ['TODOS'],
             'DIA',
             'TUDO',
             True,
             False,
             False,
             ['dados abertos',
             'governo aberto',
             'lei de acesso à informação'],
             None,
             None,
             ['destination@economia.gov.br'],
             'Teste do Ro-dou',
             True,
             '37 5 * * *',
             'DAG de teste',
             {'dou', 'generated_dag'}
             )
        ),
        ('all_params_example.yaml',
         (
             'all_params_example',
             ['SECAO_1', 'EDICAO_SUPLEMENTAR'],
             'MES',
             'TUDO',
             True,
             True,
             True,
             ['dados abertos',
             'governo aberto',
             'lei de acesso à informação',
             ],
             None,
             None,
             ['dest1@economia.gov.br', 'dest2@economia.gov.br'],
             'Assunto do Email',
             True,
             '0 8 * * MON-FRI',
             'DAG exemplo utilizando todos os demais parâmetros.',
             {'dou', 'generated_dag', 'projeto_a', 'departamento_x'}
             )
        ),
        ('terms_from_db_example.yaml',
         (
             'terms_from_db_example',
             ['TODOS'],
             'MES',
             'TUDO',
             True,
             False,
             False,
             [],
             ("SELECT 'cloroquina' as termo, 'remédio falso' as grupo "
              "UNION SELECT 'ivermectina' as termo, 'remédio falso' as grupo "
              "UNION SELECT 'vacina' as termo, 'remédio verdadeiro' as grupo\n"),
             'example_database_conn',
             ['destination@economia.gov.br'],
             '[String] com caracteres especiais deve estar entre aspas',
             True,
             '2 5 * * *',
             'DAG de teste',
             {'dou', 'generated_dag'}
             )
        ),
    ])
def test_parse(filepath, result_tuple):
    filepath = os.path.join(DouDigestDagGenerator().YAMLS_DIR,
                            filepath)
    assert YAMLParser(filepath=filepath).parse() == result_tuple
