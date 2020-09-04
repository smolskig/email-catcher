import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import xlsxwriter
import time

lastPage = '1'
maxRange = None


def requisitarDados(actualPage,getPages):
  global maxPages 
  dados = {  #dados a serem buscados
    '_token':'3btFaAnSNQznlq3XWGm1vvGHUKACZs2TjQOjUTe4',
    'page': actualPage,
    'localizar_tipo':1,
    'nome':'',
    'cpf':'',
    'registro_cau':'',
    'uf':state
  }
  try:
    requisicao = requests.post('https://acheumarquiteto.caubr.gov.br/pesquisarProfissional',dados)
  except:
    requisicao.raise_for_status()

  if getPages == True:
      maxPages = pegarNumeroDePags(requisicao.content)
  return BeautifulSoup(requisicao.content, 'html.parser')

def pegarNumeroDePags(content):
  req = BeautifulSoup(content, 'html.parser')
  tagQuantidade = req.find('span', style='padding-right: 20px')
  
  try:
    return int(tagQuantidade.text)
  except :
    print('Ocorreu um erro')

def pegaEmail(content):
  filteredEmails = []
  lengEmails = []
  
  for item in content:
    lengEmails = item.findAll('a', href=re.compile('mailto:'))
    for email in item.findAll('a', href=re.compile('mailto:')):
      if len(email.text)> 0 or email is not None :  
        filteredEmails.append(email.text)
  if lengEmails is not None:
      print(len(lengEmails),'emails retornados na pagina',str(pageNumber))
  return filteredEmails

def startFunc():
  global lista
  global state
  global pageNumber

  count = 0
  lista = []
  
  state = input('[ Insira o estado ] :').upper()

  print('-------------- Primeira consulta --------------')
  requisitarDados(1,True)
  print('Total de Páginas: ',maxPages)

  for index in range(maxPages):
    pageNumber = index + 1
    print('-----------------------------------------------')
    print('Consulta nº:',pageNumber)
    lista.append(requisitarDados(pageNumber,False))
    count = count + 1
    
    if count == 100:
      print('-----')
      processData(pageNumber)
      count = 0

    time.sleep(1)
    print('')

  print('-----------------------------------------------')

  print('Tamanho da lista: ',len(lista))
  print('-----------------------------------------------')
  processData(0)
   
 
def processData(pag):
  emails = pegaEmail(lista)
  data = pd.DataFrame({'Emails':emails})
  dataToExcel = pd.ExcelWriter('emails'+state+'.xlsx',engine='xlsxwriter')
  data.to_excel(dataToExcel, sheet_name="emails-mesmo")
  dataToExcel.save()
  print('Excel Processado pag: ' + str(pag))
  lista = []


startFunc()
