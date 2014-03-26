import unittest
from SvnParser import SvnParser

__author__ = 'Allen Qiu'


class TestSvnParser(unittest.TestCase):

	def setUp(self):
		pass

	def test_init_project(self):
		svn_parser0 = SvnParser('test_data/svn_list0.xml', 'test_data/svn_log0.xml')

		svn_parser0.init_project_list()

		self.assertTrue('Assignment2.0' in svn_parser0.projects)
		self.assertTrue('Assignment2.1' in svn_parser0.projects)
		self.assertFalse('Assignment2.2' in svn_parser0.projects)

		self.assertEqual(svn_parser0.projects['Assignment2.0'].revision, '6476')
		self.assertEqual(svn_parser0.projects['Assignment2.0'].author, 'aqiu2')
		self.assertEqual(svn_parser0.projects['Assignment2.0'].date, '2014-02-26T20:46:58.344992Z')

		self.assertEqual(svn_parser0.projects['Assignment2.1'].revision, '7776')
		self.assertEqual(svn_parser0.projects['Assignment2.1'].author, 'aqiu2')
		self.assertEqual(svn_parser0.projects['Assignment2.1'].date, '2014-03-07T17:51:01.000834Z')

	def test_init_files(self):
		svn_parser0 = SvnParser('test_data/svn_list0.xml', 'test_data/svn_log0.xml')

		svn_parser0.init_project_list()
		svn_parser0.init_file_list()

		self.assertTrue('Assignment2.0' in svn_parser0.files)
		self.assertTrue('Assignment2.1' in svn_parser0.files)
		self.assertFalse('Assignment2.2' in svn_parser0.files)

		self.assertTrue('Assignment2.0/map_data/map_test0.json' in svn_parser0.files['Assignment2.0'])
		self.assertTrue('Assignment2.0/map_data/map_test0.json' in svn_parser0.files['Assignment2.0'])
		self.assertTrue('Assignment2.0/map_data/map_test1.json' in svn_parser0.files['Assignment2.0'])
		self.assertTrue('Assignment2.0/TestAirlineGraph.py' in svn_parser0.files['Assignment2.0'])
		self.assertTrue('Assignment2.0/AirlineCommandInterface.py' in svn_parser0.files['Assignment2.0'])
		self.assertTrue('Assignment2.0/map_data/map_test2.json' in svn_parser0.files['Assignment2.0'])
		self.assertTrue('Assignment2.0/AirlineGraph.py' in svn_parser0.files['Assignment2.0'])
		self.assertTrue('Assignment2.0/map_data/map_data.json' in svn_parser0.files['Assignment2.0'])

		self.assertFalse('Assignment2.0' in svn_parser0.files['Assignment2.0'])
		self.assertFalse('Assignment2.0/map_data' in svn_parser0.files['Assignment2.0'])

		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/map_data/map_test0.json'].name,
						 'map_test0.json')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/map_data/map_test0.json'].revision,
						 '6476')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/map_data/map_test0.json'].author,
						 'aqiu2')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/map_data/map_test0.json'].date,
						 '2014-02-26T20:46:58.344992Z')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/map_data/map_test0.json'].file_size,
						 '1240')

		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/TestAirlineGraph.py'].name,
						 'TestAirlineGraph.py')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/TestAirlineGraph.py'].revision,
						 '6476')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/TestAirlineGraph.py'].author,
						 'aqiu2')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/TestAirlineGraph.py'].date,
						 '2014-02-26T20:46:58.344992Z')
		self.assertEqual(svn_parser0.files['Assignment2.0']['Assignment2.0/TestAirlineGraph.py'].file_size,
						 '7116')

	def test_init_revisions(self):
		svn_parser0 = SvnParser('test_data/svn_list0.xml', 'test_data/svn_log0.xml')

		svn_parser0.init_project_list()
		svn_parser0.init_file_list()
		svn_parser0.init_revision_list()

		self.assertTrue('Assignment2.0/map_data/map_test0.json' in svn_parser0.revisions)
		self.assertTrue('Assignment2.0/map_data/map_test0.json' in svn_parser0.revisions)
		self.assertTrue('Assignment2.0/map_data/map_test1.json' in svn_parser0.revisions)
		self.assertTrue('Assignment2.0/TestAirlineGraph.py' in svn_parser0.revisions)
		self.assertTrue('Assignment2.0/AirlineCommandInterface.py' in svn_parser0.revisions)
		self.assertTrue('Assignment2.0/map_data/map_test2.json' in svn_parser0.revisions)
		self.assertTrue('Assignment2.0/AirlineGraph.py' in svn_parser0.revisions)
		self.assertTrue('Assignment2.0/map_data/map_data.json' in svn_parser0.revisions)

		self.assertFalse('Assignment2.0' in svn_parser0.revisions)
		self.assertFalse('Assignment2.0/map_data' in svn_parser0.revisions)

		self.assertEqual(svn_parser0.revisions['Assignment2.1/AirlineGraph.py']['7776'].author, 'aqiu2')
		self.assertEqual(svn_parser0.revisions['Assignment2.1/AirlineGraph.py']['7776'].info, 'No message included.')
		self.assertEqual(svn_parser0.revisions['Assignment2.1/AirlineGraph.py']['7776'].date,
						 '2014-03-07T17:51:01.000834Z')

		self.assertEqual(svn_parser0.revisions['Assignment2.1/AirlineGraph.py']['7763'].author, 'aqiu2')
		self.assertEqual(svn_parser0.revisions['Assignment2.1/AirlineGraph.py']['7763'].info, 'No message included.')
		self.assertEqual(svn_parser0.revisions['Assignment2.1/AirlineGraph.py']['7763'].date,
						 '2014-03-07T16:49:03.411339Z')

		self.assertEqual(svn_parser0.revisions['Assignment2.1/map_data/map_data.json']['7763'].author, 'aqiu2')
		self.assertEqual(svn_parser0.revisions['Assignment2.1/map_data/map_data.json']['7763'].info,
						 'No message included.')
		self.assertEqual(svn_parser0.revisions['Assignment2.1/map_data/map_data.json']['7763'].date,
						 '2014-03-07T16:49:03.411339Z')

		self.assertFalse('7776' in svn_parser0.revisions['Assignment2.1/map_data/map_data.json'])

if __name__ == "__main__":
	unittest.main()