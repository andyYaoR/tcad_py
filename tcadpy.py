#coding=utf8
__Author__ = "Rui Yao"
__Email__ = "andy.yao.r#gmail.com"
import csv
import time
import os
import struct
import math
import argparse

class Bin2CSV():

	
	def __init__(self,DCBpath,BINpath,OUTpath):
		a = time.time()
		self.row_length = 0
		self.names = []
		self.types = []
		self.start = []
		self.width = []
		self.matrix = []
		self.short_miss = struct.pack('h',-32767)
		self.long_miss  = struct.pack('l',-2147483647)
		self.flt_miss   = struct.pack('f',-3.402823466e+38)
		self.dbl_miss   = struct.pack('d',-1.7976931348623158e+308)
		self.ReadDict(DCBpath)
		try:
			self.matrix.append(self.names)
			self.ReadBin(BINpath)
			with open(OUTpath, 'w') as f:
				writer = csv.writer(f)
				writer.writerows(self.matrix)
			b = time.time()
			print(b-a)
			print("Conversion Completed!")
		except Exception:
			print('Reading Binary File Failed!')

	def ReadDict(self,DCBpath):
		with open(DCBpath,'rb') as f:
			lines = f.readlines()
			
			try:
				for line in lines:
					line = line.decode('ascii')
					if 'binary' in line:
						self.row_length = int(line.split(' ')[0])
					elif len(line.split(',')) != 1:
						row = line.split(',')
						if 'ID' not in row[0]:
							self.names.append(row[0].replace('"',''))
						else:
							self.names.append(row[0])
						self.types.append(row[1])
						self.start.append(int(row[2]))
						self.width.append(int(row[3]))
			except Exception:
				print('Reading DCB File ERROR!')
	
	def ReadBin(self,BINpath):

		file_size = os.path.getsize(BINpath)
		row_num = file_size // self.row_length
		colunm_num = len(self.width)
		with open(BINpath,'rb') as f:
			for i in range(0,row_num):
				row_list = []
				for j in range(0,colunm_num):
					f.seek(i * self.row_length + self.start[j]-1)
					tmp = f.read(self.width[j])
					tmp_type = self.types[j]
					if tmp_type == 'I':
						entry = int.from_bytes(tmp, byteorder='little')
						if tmp == self.long_miss:
							entry = 'NA'
						#print(entry)
					elif tmp_type == 'S':
						entry = int.from_bytes(tmp, byteorder='little')
						if tmp == self.short_miss:
							entry = 'NA'
						#print(entry)
					elif tmp_type == 'R' :
						entry = struct.unpack('d',tmp)[0]
						if tmp == self.dbl_miss:
							entry = 'NA'
						#print(entry)
					elif tmp_type == 'F':
						entry = struct.unpack('f',tmp)[0]
						if tmp == self.flt_miss:
							entry = 'NA'
						#print(entry)
					elif tmp_type == 'C':
						entry = struct.unpack('c',tmp)[0]
						#print(entry)
					row_list.append(entry)
				self.matrix.append(row_list)
			#print(self.matrix)
					
def main():
	arg_parser = argparse.ArgumentParser(
			prog='tcad_py',
			epilog='tcad_py @andy501336',
			description='TransCAD Binary File to CSV File Convertor',
			formatter_class=argparse.RawTextHelpFormatter
		)

	arg_parser.add_argument(
			'-DCB',
			help="Path of the DCB File"
		)

	arg_parser.add_argument(
			'-BIN',
			help="Path of the Binary File"
		)

	arg_parser.add_argument(
			'-OUT',
			help="Path of the Output CSV File"
		)
	args = arg_parser.parse_args()
	Bin2CSV(args.DCB,args.BIN,args.OUT)


		


if __name__ == '__main__':
	main()
