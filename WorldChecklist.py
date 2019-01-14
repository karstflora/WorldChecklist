####################################################################################################
#                                     Karst Flora Research Group                                   #
#                                                                                                  #
# Checks the scientific name of the plants according to http://plantsoftheworldonline.org/         #
# using https://github.com/RBGKew/pykew                                                            #
#                                                                                                  #
# Pablo Hendrigo Alves de Melo (pablopains@yahoo.com.br)                                           #  
#                                                                                                  #
# Last update : 12-12-2018                                                                         #  
####################################################################################################

import csv

nome_arquivo_in = '...'
nome_arquivo_out = '...'

''' cria o arquivo saida'''
with open(nome_arquivo_out, "a") as arquivo_out:
    arquivo_out.close()
    
arquivo_out = open(nome_arquivo_out, 'r')
conteudo_out = arquivo_out.readlines()
conteudo_out.append(str('nomenclaturestatus'+'\t'+'author'+'\t'+'kingdom'+'\t'+'family'+'\t'+'name'+'\t'+'rank'+'\t'+'url'+'\t'+'fqId'+'\t'+'synonyms_homonyms'+'\n'))

with open(nome_arquivo_in, 'r') as arquivo_in:
    c = arquivo_in.read()
    valores = c.split('\n')         
    for e in valores:
        conteudo_out.append(str(check_powo(e)))

arquivo_out = open(nome_arquivo_out, 'w')
arquivo_out.writelines(conteudo_out)
arquivo_out.close()        
arquivo_in.close()


import pykew
import pykew.powo as powo
from pykew.powo_terms import Name

def check_powo(full_name):
    resposta_txt = ''
    synonyms_homonyms = ''
    query = {Name.full_name: str(full_name)} 
    
    ''' Busca '''
    res_query = powo.search(query)
    
    ''' Se não encontrar '''
    if res_query._response['totalResults'] == 0:
        #resposta_txt = 'no results'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\t''NA'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\n'
        resposta_txt = 'no results'+'\t'+'NA'+'\t'+''+'\t'+''+'\t'+''+'\t'''+'\t'+''+'\t'+''+'\t'+''+'\n'
        return(resposta_txt)
        
    ''' Se encontrar '''
    if res_query._response['totalResults'] > 0:
        resposta_query = res_query._response['results']
        
        print(full_name)
        print('\n')
        
        if res_query._response['totalResults'] > 1:
            #i=1
            # carrega sinonimos homonimos
            # testar resposta Artemisia annua and Ixora coccinea
            
            for i1 in range(0,res_query._response['totalResults']):
                if synonyms_homonyms == '':
                    synonyms_homonyms = resposta_query[i1]['name']
                else:
                    #print(resposta_query[i1])
                    synonyms_homonyms = synonyms_homonyms+'; '+resposta_query[i1]['name']
                
                author = ''
                for key in resposta_query[i1].keys():
                    if str(key) == str("author"):
                        author = resposta_query[i1]['author']
                
                if author != '': 
                    synonyms_homonyms = synonyms_homonyms+' '+resposta_query[i1]['author']
           
            # carrega resposta
            for i in range(0,res_query._response['totalResults']):
                if resposta_query[i]['accepted'] == True:
                    author = ''
                    for key in resposta_query[i].keys():
                        if str(key) == str("author"):
                            author = resposta_query[i]['author']
                    resposta_txt = 'accepted'+'\t'+author+'\t'+resposta_query[i]['kingdom']+'\t'+resposta_query[i]['family']+'\t'+resposta_query[i]['name']+'\t'+resposta_query[i]['rank']+'\t'+resposta_query[i]['url']+'\t'+resposta_query[i]['fqId']+'\t'+synonyms_homonyms+'\n'
                    return(resposta_txt)    
        
        if resposta_query[0]['accepted'] == False:
            
            # case of Actinodaphne sieboldiana
            nomenclaturestatus = 'synonym without accepted name resolution'
                
            for key in resposta_query[0].keys():
                if str(key) == str("synonymOf"):
                    nomenclaturestatus = 'synonym'

            if nomenclaturestatus == 'synonym':
                query = {Name.full_name : str(resposta_query[0]['synonymOf']['name'])} 
                res_query = powo.search(query)
                resposta_query = res_query._response['results']
            else:
                #resposta_txt = nomenclaturestatus+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\t''NA'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\n'
                resposta_txt = nomenclaturestatus+'\t'+'NA'+'\t'+''+'\t'+''+'\t'+''+'\t'''+'\t'+''+'\t'+''+'\t'+''+'\n'
                return(resposta_txt)
        else:
            nomenclaturestatus = 'accepted'
    
        author = ''
        for key in resposta_query[0].keys():
            if str(key) == str("author"):
                author = resposta_query[0]['author']
            
        resposta_txt = nomenclaturestatus+'\t'+author+'\t'+resposta_query[0]['kingdom']+'\t'+resposta_query[0]['family']+'\t'+resposta_query[0]['name']+'\t'+resposta_query[0]['rank']+'\t'+resposta_query[0]['url']+'\t'+resposta_query[0]['fqId']+'\t'+synonyms_homonyms+'\n'
            
    #print(resposta_txt)
    return(resposta_txt)