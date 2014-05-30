#!/usr/bin/env python
# *-* coding: utf-8 *-*

# pylinguinization Copyright (C) 2014  Jean-Marc MARTINS, Kozea
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse, glob, mmap, re, os

parser = argparse.ArgumentParser(description="Parses files looking for strings to translate.")
parser.add_argument('-o', '--output', help='xliff file output directory')
parser.add_argument('-l', '--locales', help='locales to generate', nargs='+')
parser.add_argument('files', help='files to parse', nargs='+')
args = parser.parse_args()
locales = args.locales


class Parser(object):
    """
    This class parses files looking for strings to translate.
    """
    def __init__(self):
        pass

    @property
    def strings(self):
        """Returns a list of strings to translate."""
        strings = []
        for filename in args.files:
            f = open(filename)
            try:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as fd:
                    strings.extend(re.findall(b"_\([\"\'](.+)[\"\']\)", fd.read()))
            except ValueError:
                pass
            f.close()
        return list(map(lambda x: x.decode('utf-8'), strings))

    def gen_xml(self, lang=None):
        """Generates an xml file for a given language."""
        xml = ""
        xml_body = ""
        for i, to_translate in enumerate(self.strings):
            xml_body += """%s<trans-unit id="%d">
          <source>%s</source>
          <target></target>
        </trans-unit>""" % ("        " if i == 0 else "\n        ", i, to_translate)
        xml = """<?xml version="1.0" ?>
  <xliff version="1.0">
    <file original="global" source-language="en_US" datatype="plaintext">
      <body>
%s
      </body>
    </file>
  </xliff>
""" % xml_body
        return xml


if __name__ == '__main__':
    parser = Parser()
    output_dir = args.output or '.'
    for lang in locales:
        with open(output_dir + '/%s.xliff' % lang, 'w') as fd:
            fd.write(parser.gen_xml())
