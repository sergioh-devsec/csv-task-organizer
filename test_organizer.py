import csv
import unittest
from pathlib import Path
from organizer import organize,export_csv,safe_cell
class OrganizerTests(unittest.TestCase):
    def test_sample(self):
        result=organize(Path(__file__).with_name('sample.csv').read_text())
        self.assertEqual((result['total'],result['duplicates'],result['completed'],len(result['tasks'])),(6,1,1,3))
        self.assertEqual(result['invalid_rows'],[7]);self.assertEqual(result['tasks'][0]['task'],'Preparar informe')
    def test_formula_and_quotes(self):
        result=organize('task,owner,priority,due,status\n"=HYPERLINK(1)","A, B",high,2028-02-29,todo')
        output=export_csv(result['tasks']);self.assertIn("'=HYPERLINK(1)",output);self.assertIn('"A, B"',output)
        for value in ['=1','+1','-1','@SUM(1)','  =1']:
            self.assertTrue(safe_cell(value).startswith("'"))
    def test_same_name_different_owners_survive(self):
        r=organize('task,owner,priority,due,status\nReport,A,high,2026-11-01,todo\nReport,B,high,2026-11-01,todo')
        self.assertEqual(len(r['tasks']),2)
    def test_rejects_size_header_and_bad_dates(self):
        for text in ['', 'wrong\n', 'a'*20001]:
            with self.assertRaises(ValueError):organize(text)
        r=organize('task,owner,priority,due,status\nTask,A,high,2026-02-29,todo');self.assertEqual(r['invalid_rows'],[2])

if __name__=='__main__': unittest.main()
