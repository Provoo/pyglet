"""Test that multiple windows share objects by default.

This test is non-interactive.
"""


import unittest
from ctypes import *

from pyglet import window, canvas
from pyglet.gl import *


class ContestShareTestCase(unittest.TestCase):

    def create_context(self, share):
        display = canvas.get_display()
        screen = display.get_default_screen()
        config = pyglet.gl.Config.match(screen)
        return config.create_context(share)

    def test_context_share_list(self):
        w1 = window.Window(200, 200)
        try:
            w1.switch_to()
            glist = glGenLists(1)
            glNewList(glist, GL_COMPILE)
            glLoadIdentity()
            glEndList()
            self.assertTrue(glIsList(glist))
        except:
            w1.close()
            raise

        w2 = window.Window(200, 200)
        try:
            w2.switch_to()
            self.assertTrue(glIsList(glist))
        finally:
            w1.close()
            w2.close()

    def test_context_noshare_list(self):
        w1 = window.Window(200, 200)
        try:
            w1.switch_to()
            glist = glGenLists(1)
            glNewList(glist, GL_COMPILE)
            glLoadIdentity()
            glEndList()
            self.assertTrue(glIsList(glist))
        except:
            w1.close()
            raise

        w2 = window.Window(200, 200, context=self.create_context(None))
        try:
            w2.set_visible(True)
            w2.switch_to()
            self.assertTrue(not glIsList(glist))
        finally:
            w1.close()
            w2.close()

    def test_context_share_texture(self):
        w1 = window.Window(200, 200)
        try:
            w1.switch_to()
            textures = c_uint()
            glGenTextures(1, byref(textures))
            texture = textures.value

            glBindTexture(GL_TEXTURE_2D, texture)
            data = (c_ubyte * 4)()
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, data)
            self.assertTrue(glIsTexture(texture))
        except:
            w1.close()
            raise

        w2 = window.Window(200, 200)
        try:
            w2.switch_to()
            self.assertTrue(glIsTexture(texture))

            glDeleteTextures(1, byref(textures))
            self.assertTrue(not glIsTexture(texture))

            w1.switch_to()
            self.assertTrue(not glIsTexture(texture))

        finally:
            w1.close()
            w2.close()
