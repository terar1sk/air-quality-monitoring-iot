from machine import Pin
import time

class DS1302:
    def __init__(self, clk, dio, cs):
        self.clk = Pin(clk, Pin.OUT)
        self.dio = Pin(dio, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.cs.value(0)
        self.clk.value(0)
        self._CE = self.cs
        self._CLK = self.clk
        self._IO = Pin(dio, Pin.OUT)
        self._CE.value(0)

    def _write_byte(self, val):
        for i in range(8):
            self._IO.value((val >> i) & 1)
            self._CLK.value(1)
            self._CLK.value(0)

    def _read_byte(self):
        result = 0
        self._IO.init(Pin.IN)
        for i in range(8):
            bit = self._IO.value()
            result |= (bit << i)
            self._CLK.value(1)
            self._CLK.value(0)
        self._IO.init(Pin.OUT)
        return result

    def _bcd2dec(self, bcd):
        return (bcd // 16) * 10 + (bcd % 16)

    def _dec2bcd(self, dec):
        return (dec // 10) * 16 + (dec % 10)

    def _write_register(self, reg, val):
        self._CE.value(1)
        self._write_byte(reg)
        self._write_byte(val)
        self._CE.value(0)

    def _read_register(self, reg):
        self._CE.value(1)
        self._write_byte(reg | 0x01)
        data = self._read_byte()
        self._CE.value(0)
        return data

    # === PUBLIC METHODS ===
    def read_time(self):
        """Возвращает кортеж (год, месяц, день, день_недели, час, минута, секунда)"""
        self._CE.value(1)
        self._write_byte(0xBF)
        data = [self._read_byte() for _ in range(8)]
        self._CE.value(0)
        second = self._bcd2dec(data[0] & 0x7F)
        minute = self._bcd2dec(data[1])
        hour = self._bcd2dec(data[2])
        day = self._bcd2dec(data[3])
        month = self._bcd2dec(data[4])
        day_of_week = self._bcd2dec(data[5])
        year = 2000 + self._bcd2dec(data[6])
        return (year, month, day, day_of_week, hour, minute, second)

    def write_time(self, year, month, day, day_of_week, hour, minute, second):
        """Устанавливает время"""
        self._CE.value(1)
        self._write_byte(0xBE)
        self._write_byte(self._dec2bcd(second))
        self._write_byte(self._dec2bcd(minute))
        self._write_byte(self._dec2bcd(hour))
        self._write_byte(self._dec2bcd(day))
        self._write_byte(self._dec2bcd(month))
        self._write_byte(self._dec2bcd(day_of_week))
        self._write_byte(self._dec2bcd(year % 100))
        self._write_byte(0)
        self._CE.value(0)
        time.sleep_ms(10)

    def halt(self, val):
        """Останавливает или запускает часы"""
        sec = self._read_register(0)
        if val:
            sec |= 0x80
        else:
            sec &= 0x7F
        self._write_register(0x80, sec)
