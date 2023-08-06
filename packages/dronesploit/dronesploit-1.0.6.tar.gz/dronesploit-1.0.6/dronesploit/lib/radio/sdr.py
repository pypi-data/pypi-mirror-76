# -*- coding: UTF-8 -*-
from tinyscript.helpers.
from sploitkit import *


class SDRModule(Module):
	""" Module proxy class for defining multiple common utility methods for
	radio-controlled drones.
	
	Author:  Enzo Borel
	Email:   borelenzo@gmail.com
	Version: 1.0
	"""	
	FREQUENCY = "FREQUENCY"
	SAMP_RATE = "SAMP_RATE"
	SAMP_SYMS = "SAMP_SYMS"
	RF_GAIN   = "RF_GAIN"
	IF_GAIN   = "IF_GAIN"
	BB_GAIN   = "BB_GAIN"

	config = Config({
		Option(
			FREQUENCY,
			"Capture frequency",
			True,
			validate=validate_float
		): "2.4e9",
		Option(
			SAMP_RATE,
			"Sampling rate",
			True,
			validate=validate_float
		): "8e6",
		Option(
			SAMP_SYMS,
			"Samples per symbol",
			True,
			validate=validate_int
		): 8,
		Option(
			RF_GAIN,
			"RF Gain",
			True,
			validate=validate_int
		) : 10,
		Option(
			IF_GAIN,
			"IF Gain",
			True,
			validate=validate_int
		) : 20,
		Option(
			BB_GAIN,
			"BB Gain",
			True,
			validate=validate_int
		) : 20
	})
	requirements = {'python': ["gnuradio", "osmosdr", "crcmod"]}

	def __init__(self):
		self.silent = (-0.0078125-0.0078125j)

	def init(self):
		self.frequency = int(float(self.config.option(SDRModule.FREQUENCY).value))
		self.samp_rate = int(float(self.config.option(SDRModule.SAMP_RATE).value))
		self.samp_syms = int(self.config.option(SDRModule.SAMP_SYMS).value)
		self.rf_gain   = int(self.config.option(SDRModule.RF_GAIN).value)
		self.if_gain   = int(self.config.option(SDRModule.IF_GAIN).value)
		self.bb_gain   = int(self.config.option(SDRModule.BB_GAIN).value)
	
	def wait_for_exit(self):
		try:
			input('Press Enter to quit: ')
		except EOFError:
			pass

	def build_payload(self, body):
		import crcmod
		payload = self.preamble + self.TXid + body
		crc16 = crcmod.mkCrcFun(self.polynomial, self.seed, self.endianess, self.xorout)
		crc = crc16(bytes(payload))
		payload.append(crc >> 8)
		payload.append(crc & 0xFF)
		payload = self.sync + payload
		#payload.append(64)
		return tuple(payload), len(payload) * 8 * 32

	def setup_osmosdr_sink(self):
		import osmosdr
		osmosdr_sink = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
		osmosdr_sink.set_sample_rate(self.samp_rate)
		osmosdr_sink.set_center_freq(self.frequency, 0)
		osmosdr_sink.set_freq_corr(0, 0)
		osmosdr_sink.set_gain(self.rf_gain, 0)
		osmosdr_sink.set_if_gain(self.if_gain, 0)
		osmosdr_sink.set_bb_gain(self.bb_gain, 0)
		osmosdr_sink.set_antenna('', 0)
		osmosdr_sink.set_bandwidth(0, 0)
		return osmosdr_sink

class SnifferModule(SDRModule):
	TIMEOUT   = "TIMEOUT"
	config = Config({
		Option(
			TIMEOUT,
			"Capturing time duration",
			True,
			validate=validate_int
		): 10,
	})
	def __init__(self):
		super(SnifferModule, self).__init__()

	def find_sub_list(self, sl, l):
		"""
		Finds all occurences of a subsequence in a sequence
		:param sl: the subsequence to look for
		:param l:  the sequence in which to search
		:returns:  a liste of tuples (x,y) being the indexes of starting and enfing of each found subsequence
		"""
		results = []
		sll = len(sl)
		for ind in (i for i, e in enumerate(l) if e == sl[0]):
			if l[ind:ind+sll] == sl:
				results.append((ind, ind + sll -1))
		return results
	def init(self):
		super().init()
		self.timeout   = int(self.config.option(SnifferModule.TIMEOUT).value)

class SDRXN297Module(SDRModule):

	TXID 	   = "TXID"
	POLYNOMIAL = "POLYNOMIAL"
	SEED       = "SEED"
	ENDIANESS  = "ENDIANESS"
	XOROUT	   = "XOROUT"

	config = Config({
		Option(
			TXID,
			"Id of the transceiver,as given by the sniffer XN297",
			True,
			validate=validate_id
		): "c3 d0 20 e1",
		Option(
			POLYNOMIAL,
			"Polynomial used to compute the CRC",
			False,
			validate=validate_int
		): 69665,
		Option(
			SEED,
			"Seed used to compute the CRC",
			False,
			validate=validate_int
		): 0,
		Option(
			ENDIANESS,
			"Endianess used to compute the CRC",
			False,
			validate=validate_bool
		): False,
		Option(
			XOROUT,
			"Final xor used to compute the CRC",
			False,
			validate=validate_int
		): 0
	})

	def __init__(self):
		super(SDRXN297Module, self).__init__()
		self.sync = [0, 170, 170, 170, 170, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
		self.preamble = [0x71, 0x0F, 0x55]

	def init(self):
		super().init()
		self.TXid       = [int(x, 16) for x in self.config.option(SDRXN297Module.TXID).value.split(" ")]
		self.polynomial = int(self.config.option(SDRXN297Module.POLYNOMIAL).value)
		self.seed       = int(self.config.option(SDRXN297Module.SEED).value)
		self.endianess  = int(self.config.option(SDRXN297Module.ENDIANESS).value)
		self.xorout     = int(self.config.option(SDRXN297Module.XOROUT).value)	
	
