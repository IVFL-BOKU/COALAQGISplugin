import requests
import tempfile
import datetime
import os

from qgis.core import *

boku_astoken = 'c749b213208b179046d877bd21e2d635241c4f03d40fb19712b72894e34877daec4f29c971e50652'
boku_post = False
boku_host = 'https://api.coalaproject.eu/api'
boku_token = ''
boku_period = 0
boku_ahead = 180
boku_forward = 15
boku_srid  = '3857'
boku_geom = ''
boku_cm = '0'
boku_indicator = ''
boku_daily = '0'
boku_start = ''
boku_end = ''
boku_date = ''
boku_outpath = ''

boku_dailys = ['et','cwr']      # lista degli indicatori a sviluppo giornaliero

# variabili globali
boku_qryparms = {}
boku_status_code = 0

def boku_info(txt):
  QgsMessageLog.logMessage(txt,'boku_download',level=Qgis.Info)
  
def boku_warn(txt):
  QgsMessageLog.logMessage(txt,'boku_download',level=Qgis.Warning)

def boku_init():
  boku_info('boku_init:in')
  global boku_outpath
  global boku_qryparms
  boku_outpath = tempfile.gettempdir()
  boku_qryparms = {
    'outpath'   : boku_outpath,
    'boku'      : boku_host,
    'token'     : boku_token,
    'srid'      : boku_srid,
    'geom'      : boku_geom,
    'cm'        : boku_cm,
    'period'    : boku_period,
    'indicator' : boku_indicator,
    'daily'     : boku_daily,
    'start'     : boku_start,
    'end'       : boku_end,
    'date'      : boku_date   
  }
  boku_info('boku_init:out')

# lista delle date disponibile per uno specifico indicator/poligono
def boku_request_urldate():
  boku_info("boku_request_urldate:in")
  global boku_qryparms
  url = '{boku}/indicator/{indicator}/rasterBuffer?srcSrid={srid}&minCover=0&dateFrom={start}&dateTo={end}&geometry={geom}&token={token}&daily={daily}'.format(**boku_qryparms)
  boku_info("boku_request_urldate:out")
  return url

def boku_request_urldate_post():
  boku_info("boku_request_urldate_post:in")
  global boku_qryparms
  url = '{boku}/indicator/{indicator}/rasterBuffer?srcSrid={srid}&minCover=0&dateFrom={start}&dateTo={end}&token={token}&daily={daily}'.format(**boku_qryparms)
  payload = {'geometry':boku_qryparms['geom']}
  boku_info("boku_request_urldate_post:out")
  return {'url':url,'payload':payload}

# ritorna la lista delle date , 
# rev=False in ordine crescente
# rev=True in ordine decrescente
def boku_request_dates(url,rev):
  boku_info("boku_request_dates:in")
  global boku_status_code
  dates = []
  try:
    r = requests.get(url)
    boku_status_code = r.status_code 
    if r.status_code==200:
      rj = r.json()
#    print(len(rj))
      for i in rj:
#      print(i['date'])
        dates.append(i['date'])
      dates.sort(reverse=rev)
    else:
      boku_info("boku_request_dates:error " + str(r.status_code))
      boku_status_code = r.status_code
  except:
    boku_info("boku_request_dates:except")
    boku_status_code = -1
  boku_info("boku_request_dates:out " + str(boku_status_code))
  return dates

def boku_request_dates_post(url,payload,rev):
  boku_info("boku_request_dates:in")
  global boku_status_code
  dates = []
  try:
    r = requests.post(url,data=payload)
    boku_status_code = r.status_code 
    if r.status_code==200:
      rj = r.json()
#    print(len(rj))
      for i in rj:
#      print(i['date'])
        dates.append(i['date'])
      dates.sort(reverse=rev)
    else:
      boku_info("boku_request_dates:error " + str(r.status_code))
      boku_status_code = r.status_code
  except:
    boku_info("boku_request_dates:except")
    boku_status_code = -1
  boku_info("boku_request_dates:out " + str(boku_status_code))
  return dates
  
def boku_getdates(token,indicator,geom):  
  boku_info("boku_getdates:in")
  global boku_qryparms
  today = datetime.date.today()
  forward = today+datetime.timedelta(days=boku_forward)
  ahead = today-datetime.timedelta(days=boku_ahead)
  if indicator in boku_dailys:
    boku_qryparms['daily'] = 1
  else:
    boku_qryparms['daily'] = 0
  boku_qryparms['indicator'] = indicator
  boku_qryparms['token'] = token
  boku_qryparms['start'] = ahead.strftime('%Y-%m-%d')
  boku_qryparms['end'] = forward.strftime('%Y-%m-%d')
  boku_qryparms['geom'] = geom
  print(boku_qryparms)
  if boku_post:
    urlp = boku_request_urldate_post()
    print(urlp['url'])
    dates = boku_request_dates_post(urlp['url'].urlp['payload'],True)
  else:
    url = boku_request_urldate()
    print(url)
    dates = boku_request_dates(url,True)
  boku_info("boku_getdates:out " + str(len(dates)))
  return dates

# download del tif 
def boku_request_urldownload():
  boku_info("boku_request_urldownload:in")
  global boku_qryparms
  url = '{boku}/indicator/{indicator}/rasterData?srcSrid={srid}&srid={srid}&minCover=0&format=image/tiff&colorMap=0&scale=real&date={date}&period={period}&geometry={geom}&token={token}&daily={daily}'.format(**boku_qryparms)
  boku_info("boku_request_urldownload:out")
  return url

def boku_request_urldownload_post():
  boku_info("boku_request_urldownload:in")
  global boku_qryparms
  url = '{boku}/indicator/{indicator}/rasterData?srcSrid={srid}&srid={srid}&minCover=0&format=image/tiff&colorMap=0&scale=real&date={date}&period={period}&token={token}&daily={daily}'.format(**boku_qryparms)
  payload = {'geometry':boku_qryparms['geom']}
  boku_info("boku_request_urldownload:out")
  return {'url':url,'payload':payload}

# download di un file con salvataggio sul disco
def boku_request_download(url,filename):
  boku_info("boku_request_download:in")
  global boku_status_code
  try:
    r = requests.get(url, stream=True)
    boku_status_code = r.status_code 
    if r.status_code==200:
      with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
          fd.write(chunk)
      errcode = 0
    else:
      errcode = 1
  except:
    boku_info("boku_request_download:except")
    boku_status_code = -1 
    errcode = 1
  boku_info("boku_request_download:out "+str(boku_status_code)+','+str(errcode))
  return errcode

def boku_request_download_post(url,payload,filename):
  boku_info("boku_request_download_post:in")
  global boku_status_code
  try:
    r = requests.post(url, data=payload,stream=True)
    boku_status_code = r.status_code 
    if r.status_code==200:
      with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
          fd.write(chunk)
      errcode = 0
    else:
      errcode = 1
  except:
    boku_info("boku_request_download_post:except")
    boku_status_code = -1 
    errcode = 1
  boku_info("boku_request_download_post:out "+str(boku_status_code)+','+str(errcode))
  return errcode

def boku_download(token,indicator,geom,date):
  boku_info("boku_download:in")
  global boku_qryparms
  boku_qryparms['outpath'] = tempfile.gettempdir()
  if indicator in boku_dailys:
    boku_qryparms['daily'] = 1
  else:
    boku_qryparms['daily'] = 0
  boku_qryparms['indicator'] = indicator
  boku_qryparms['token'] = token
  boku_qryparms['geom'] = geom
  boku_qryparms['date'] = date
  outfile = '{outpath}/{indicator}_{date}.tif'.format(**boku_qryparms)
  layname = '{indicator}_{date}'.format(**boku_qryparms)
  if boku_post:
    urlp = boku_request_urldownload()
    print(urlp['url'],outfile,layname)
    errcode = boku_request_download_post(urlp['url'].urlp['payload'],outfile)
  else:
    url = boku_request_urldownload()
    print(url,outfile,layname)
    errcode = boku_request_download(url,outfile)

  filesz = os.path.getsize(outfile)
  boku_info("boku_download:errcode/filesize " + str(errcode)+','+str(filesz))
  boku_info("boku_download:out")
  return {"errcode":errcode,"outfile":outfile,"layname":layname}
