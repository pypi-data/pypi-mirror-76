from serial import Serial as _Serial
from typing import List as _List


class DL_RS1A:
	ReadAllCommand = b'M0'

	def __init__(self, port: str, baudrate=9600, timeout=0.2):
		self._serial = _Serial(port=port, baudrate=baudrate, timeout=0.2)

	def _read_frame(self) -> bytes:
		return self._serial.readline()

	def _write_frame(self, frame: bytes):
		if not frame.endswith(b'\n'):
			frame += b'\r\n'
		self._serial.write(frame)

	def read_all(self) -> _List[float]:
		self._serial.flushInput()
		self._write_frame(DL_RS1A.ReadAllCommand)
		line = self._read_frame().strip()
		if len(line) == 0:
			raise IOError('Device response timeout.')
		if not line.startswith(DL_RS1A.ReadAllCommand):
			raise IOError('Device feedback format not valid: %s.' % line.decode('latin'))
		segments = line.split(b',')[1:]
		values = [float(seg) for seg in segments]
		return values
