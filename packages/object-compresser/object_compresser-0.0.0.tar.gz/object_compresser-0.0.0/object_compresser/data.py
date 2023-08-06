import pickle
import bz2

class data(object):
	def load(self, filename):
		"""loads and return's the bytes like object which is saved in the file"""
		with open(filename, 'rb') as f:
			data=f.read()
			return data
	def decompress(self, b):
		"""decompresses the give byte like object to normal python object and return's it.
		please note: use byte like object create by this module only"""
		d=bz2.decompress(b)
		data=pickle.loads(d)
		return data
	def load_and_decompress(self, filename):
		"""loads and decompresses the data from the given filename/path"""
		d=self.load(filename)
		data=self.decompress(d)
		return data
	def save(self, filename, b):
		"""saves the given bytes in to spesifyed file/path.
		please note: use bytes made by this module only. other wise you will have problems loading the data from the file."""
		f=open(filename, 'wb')
		f.write(b)
		f.close()
	def compress(self, data):
		"""convert's to bytes like object and compresses it."""
		d=pickle.dumps(data)
		data=bz2.compress(d)
		return data
	def compress_and_save(self, data, filename):
		d=self.compress(data)
		self.save(filename, d)