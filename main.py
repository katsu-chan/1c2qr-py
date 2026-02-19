import sys

from datetime import datetime
import xml.etree.ElementTree as ET

ns = "{urn:1C.ru:commerceml_2}"

tree = ET.parse(sys.argv[1])
root = tree.getroot()
doc = root[0]
cAs = doc.find(ns+"Контрагенты")

cA0 = cAs[0]
cA1 = cAs[1]

if cA0.find(ns+"Роль").text == "Продавец":
    cAs = cA0
    cAb = cA1
else:
    cAb = cA0
    cAs = cA1

#print("b", cAb.find(ns+"ИНН").text)
#print("s", cAs.find(ns+"ИНН").text)

docno = doc.find(ns+"Номер").text
docdate = doc.find(ns+"Дата").text
docdate = datetime.strptime(docdate, "%Y-%m-%d").strftime("%d.%m.%Y")

sName = cAs.find(ns+"ОфициальноеНаименование").text
sAcc = cAs.find(ns+"РасчетныйСчет")
sPAcc = sAcc.find(ns+"НомерСчета").text
sBank = sAcc.find(ns+"Банк")
sBankName = sBank.find(ns+"Наименование").text
sBIC = sBank.find(ns+"БИК").text
sCAcc = sBank.find(ns+"СчетКорреспондентский").text
total = int(float(doc.find(ns+"Сумма").text)*100)
if doc.find(ns+"Валюта").text != "643":
    print("unknown cur")
#purpose = doc.find
sINN = cAs.find(ns+"ИНН").text
sKPP = cAs.find(ns+"КПП").text
#exit()
purpose = f"Оплата по счету № {docno} от {docdate}."

code = f"ST00012|Name={sName}|PersonalAcc={sPAcc}|BankName={sBankName}|BIC={sBIC}|CorrespAcc={sCAcc}|Sum={total}|Purpose={purpose}|PayeeINN={sINN}|KPP={sKPP}"
print(code)

import qrcode

img = qrcode.make(code).show()
