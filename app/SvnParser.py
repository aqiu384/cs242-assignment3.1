import xml.etree.ElementTree as ET
from collections import namedtuple

__author__ = 'Allen Qiu'

# Tuple for Project Info: Holds revision number, author, info (from latest revision) and date
ProjectEntry = namedtuple('ProjectEntry', 'revision author info date')
# Tuple for File Info: Holds file name, revision number, author, date, size, and type (from dictionary)
FileEntry = namedtuple('FileEntry', 'name revision author date file_size file_type')
# Tuple for Revision Info: Holds author, description, and date of revision
RevisionEntry = namedtuple('RevisionEntry', 'author info date')
# Maps file extensions to description of intended use of file
FileTypeDict = {'java': 'code', 'py': 'code', 'xml': 'data', 'txt': 'documentation', 'pdf': 'documentation',
				'zip': 'compressed', 'json': 'data'}


class SvnParser():
	"""Parses pair of SVN list and log into information about that repository"""

	def __init__(self, svn_list, svn_log):
		"""Loads SVN list and log files and initializes all dictionaries"""
		self.projects = {}		# Dictionary of all projects and their basic info by project name
		self.files = {}			# Dictionary of all files and their basic info grouped by project name
		self.revisions = {}		# Dictionary of all revisions and their basic info grouped by file path

		list_tree = ET.parse(svn_list)
		log_tree = ET.parse(svn_log)

		self.list_entries = list_tree.getroot()[0]		# Storage for SVN list
		self.log_entries = log_tree.getroot()			# Storage for SVN log

		self.root_path = str(self.list_entries.get('path'))		# Path to root SVN repository

	def init_project_list(self):
		"""Scans for projects in SVN list and stores their basic info"""
		for entry in self.list_entries:
			if str(entry.get('kind')) == 'dir':
				path = str(entry.find('name').text)
				dir_level = path.count('/')

				if dir_level == 0:		# Projects are defined by the highest directory under root
					commit = entry.find('commit')
					revision = commit.get('revision')
					author = str(commit.find('author').text)
					date = str(commit.find('date').text)

					project_entry = ProjectEntry(revision, author, "Nothing.", date)
					self.projects[path] = project_entry
					self.files[path] = {}

	def init_file_list(self):
		"""Must run after init_project_list - Scans for files in SVN list and stores them under parent project"""
		for entry in self.list_entries:
			if str(entry.get('kind')) == 'file':
				path = str(entry.find('name').text)
				path_parts = path.split('/')
				project = path_parts[0]

				if project in self.projects:
					name = path_parts[-1]
					file_extension = name.split('.')[-1]
					file_type = "other"

					if file_extension in FileTypeDict:
						file_type = FileTypeDict[file_extension]

					commit = entry.find('commit')
					revision = commit.get('revision')
					author = str(commit.find('author').text)
					date = str(commit.find('date').text)
					file_size = entry.find('size').text

					file_entry = FileEntry(name, revision, author, date, file_size, file_type)
					self.files[project][path] = file_entry
					self.revisions[path] = {}

	def init_revision_list(self):
		"""Must run after init_file_list - Scans for revisions in SVN log and stores them under parent file"""
		for entry in self.log_entries:
			revision = str(entry.get('revision'))
			author = str(entry.find('author').text)
			date = str(entry.find('date').text)
			message = str(entry.find('msg').text)

			if message == "None":
				message = "No message included."

			paths = entry.find('paths')
			for path in paths:
				kind = str(path.get('kind'))
				path_name = str(path.text)
				path_parts = (path_name + '/').split('/')
				project = path_parts[2]
				file_path = '/'.join(path_parts[2:])[:-1]

				# Update parent project with this description if this is the latest update
				if kind == 'dir' and len(path_parts) == 4 and project in self.projects:
					project_info = self.projects[project]
					updated_project = ProjectEntry(project_info.revision, project_info.author,
												   message, project_info.date)
					self.projects[project] = updated_project

				elif file_path in self.revisions:
					revision_entry = RevisionEntry(author, message, date)
					self.revisions[file_path][revision] = revision_entry

	def delete_list_entry(self):
		"""Deletes list_entry tree"""
		self.list_entries = None

	def delete_log_entry(self):
		"""Deletes log_entry tree"""
		self.log_entries = None

	def print_projects(self):
		"""Prints list of projects and their properties"""
		for project in self.projects:
			print project
			entry = self.projects[project]
			print "     " + entry.revision
			print "     " + entry.author
			print "     " + entry.info
			print "     " + entry.date

	def print_files(self):
		"""Prints list of files and their properties"""
		for project in self.files:
			print "-----" + project + "-----"
			for file_entry in self.files[project]:
				print file_entry
				entry = self.files[project][file_entry]
				print "     " + entry.name
				print "     " + entry.revision
				print "     " + entry.author
				print "     " + entry.date
				print "     " + entry.file_size
				print "     " + entry.file_type

	def print_revisions(self):
		"""Prints list of revisions and their properties"""
		for file_entry in self.revisions:
			print "-----" + file_entry + "-----"
			for revision in self.revisions[file_entry]:
				print revision
				entry = self.revisions[file_entry][revision]
				print "     " + entry.author
				print "     " + entry.info
				print "     " + entry.date