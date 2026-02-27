# SSD1107 OLED driver for 64x128 vertical display (GME64128-11)
# Works with Raspberry Pi Pico / MicroPython
# Rotated 90° to fill full screen (fixes "right half only" issue)

from micropython import const
import framebuf
from time import sleep_ms

SET_DISP_OFF     = const(0xAE)
SET_DISP_ON      = const(0xAF)
SET_START_LINE   = const(0x40)
SET_PAGE_ADDR    = const(0xB0)
SET_CONTRAST     = const(0x81)
SET_SEG_REMAP    = const(0xA0)
SET_COM_SCAN_DIR = const(0xC0)
SET_DISP_OFFSET  = const(0xD3)
SET_CLK_DIV      = const(0xD5)
SET_PRECHARGE    = const(0xD9)
SET_VCOM_DESEL   = const(0xDB)
SET_CHARGE_PUMP  = const(0x8D)
SET_ENTIRE_ON    = const(0xA4)
SET_NORM_INV     = const(0xA6)
SET_MUX_RATIO    = const(0xA8)

COL_OFFSET_LOW   = const(0x00)
COL_OFFSET_HIGH  = const(0x10)

class SSD1107(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray(self.width * self.height // 8)
        # создаём вспомогательный буфер для поворота
        self.tmp = bytearray(self.width * self.height // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self._init_display()

    def _cmd(self, *cmds):
        for c in cmds:
            self.i2c.writeto(self.addr, bytes((0x00, c)))
            sleep_ms(1)

    def _data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)

    def _init_display(self):
        self._cmd(
            SET_DISP_OFF,
            SET_DISP_OFFSET, 0x00,
            SET_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,
            SET_COM_SCAN_DIR | 0x08,
            SET_MUX_RATIO, 0x7F,  # 128 строк
            SET_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0x7F,
            SET_CHARGE_PUMP, 0x14,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_DISP_ON
        )
        self.fill(0)
        self.show()

    def _rotate_buffer(self):
        """Поворачивает содержимое экрана на 90°."""
        w, h = self.width, self.height
        self.tmp[:] = b'\x00' * len(self.tmp)
        fb = framebuf.FrameBuffer(self.tmp, h, w, framebuf.MONO_VLSB)
        for y in range(h):
            for x in range(w):
                if self.pixel(x, y):
                    fb.pixel(y, w - 1 - x, 1)
        self.buffer[:] = self.tmp[:]

    def show(self):
        # поворачиваем буфер перед выводом
        self._rotate_buffer()
        for page in range(self.height // 8):
            self._cmd(SET_PAGE_ADDR + page)
            self._cmd(COL_OFFSET_LOW)
            self._cmd(COL_OFFSET_HIGH)
            start = page * self.width
            end = start + self.width
            self._data(self.buffer[start:end])
