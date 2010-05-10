'''
Created on 30.8.2009

@author: Kosta Mihajlov
'''
#import Models.AccountingModels as am
#cont_d=True
#cont_b=True
#bcount=0
#dcount=0
#while cont_d:
#    dolgovi = am.Dolg.all().fetch(100)
#    if len(dolgovi)<100:
#        cont_d=False
#    for d in dolgovi:
#        d.delete()
#        dcount+=1
#while cont_b:
#    balansi =am.FinalnaSmetka.all().fetch(100)
#    if len(balansi)<100:
#        cont_b=False
#    for b in balansi:
#        b.delete()
#        bcount+=1
#
#print 'Deleted all items---\n'+'Balances: '+str(bcount)+'\n--Depts: '+str(dcount)

import datetime as dt
print 'Cron Happened at '+ dt.date.strftime()