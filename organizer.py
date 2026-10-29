"""Offline CSV task organizer. Python 3.10+, standard library only."""
import argparse
import csv
import datetime
import io
import json
import re
import unicodedata
from pathlib import Path

def normalized(value):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFD',value.lower()) if unicodedata.category(c)!='Mn').split())

def organize(text):
    if len(text.encode('utf8'))>20000: raise ValueError('maximum input size: 20 KB')
    rows=list(csv.reader(io.StringIO(text.lstrip('\ufeff')),strict=True))
    rows=[r for r in rows if any(c.strip() for c in r)]
    headers=[['tarea','responsable','prioridad','fecha','estado'],['task','owner','priority','due','status']]
    if not rows or [normalized(c) for c in rows[0]] not in headers: raise ValueError('invalid or missing CSV header')
    if len(rows)>201: raise ValueError('maximum 200 records')
    priorities={'alta':0,'high':0,'media':1,'medium':1,'baja':2,'low':2}
    statuses={'pendiente':'todo','todo':'todo','en curso':'doing','doing':'doing','completada':'done','done':'done'}
    seen=set(); result={'total':len(rows)-1,'duplicates':0,'completed':0,'invalid_rows':[],'tasks':[]}
    for number,row in enumerate(rows[1:],2):
        try:
            if len(row)!=5: raise ValueError()
            task,owner,p,due,s=[v.strip() for v in row]
            if not task or len(task)>240 or not owner or len(owner)>80 or re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]',task+owner): raise ValueError()
            priority,status=priorities[normalized(p)],statuses[normalized(s)]
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',due) or datetime.date.fromisoformat(due).isoformat()!=due: raise ValueError()
        except (ValueError,KeyError): result['invalid_rows'].append(number); continue
        key=(normalized(task),normalized(owner),priority,due,status)
        if key in seen: result['duplicates']+=1; continue
        seen.add(key)
        if status=='done': result['completed']+=1; continue
        result['tasks'].append({'task':task,'owner':owner,'priority':priority,'due':due,'status':status})
    result['tasks'].sort(key=lambda t:(t['priority'],t['due'],normalized(t['task'])))
    return result

def safe_cell(value):
    text=str(value)
    return "'"+text if re.match(r'^[\s]*[=+@\-\t\r\n]',text) else text

def export_csv(tasks):
    output=io.StringIO();writer=csv.writer(output,quoting=csv.QUOTE_ALL)
    writer.writerow(['tarea','responsable','prioridad','fecha','estado'])
    for task in tasks: writer.writerow([safe_cell(task['task']),safe_cell(task['owner']),['alta','media','baja'][task['priority']],task['due'],'pendiente' if task['status']=='todo' else 'en curso'])
    return '\ufeff'+output.getvalue()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    try:
        if args.input.stat().st_size>20000: raise ValueError('maximum input size: 20 KB')
        result=organize(args.input.read_text(encoding='utf-8-sig'))
        with args.output.open('x',encoding='utf8',newline='') as stream:stream.write(export_csv(result['tasks']))
        print(json.dumps({k:v for k,v in result.items() if k!='tasks'},ensure_ascii=False,indent=2))
    except (ValueError,OSError,csv.Error) as error:parser.exit(2,f'Error: {error}\n')

if __name__=='__main__':main()
