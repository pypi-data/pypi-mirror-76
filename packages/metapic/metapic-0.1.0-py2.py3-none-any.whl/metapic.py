#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''metapic - Command line tool for modifying picture metadata
from file/folder names and config.
'''

__author__ = '''luphord'''
__email__ = '''luphord@protonmail.com'''
__version__ = '''0.1.0'''


import subprocess
from argparse import ArgumentParser
from pathlib import Path


EXIFTOOL = 'exiftool'
DTFMT = '{:04d}:{:02d}:{:02d} 12:{:02d}:{:02d}'


PLACES = {
}


class FieldName:
    def __init__(self, image):
        parts = Path(image).stem.split('__')
        if len(parts) < 2:
            raise Exception('Illegal file name')
        self.prefix = parts[0]
        self.number = parts[1]
        self.date = parts[2] if len(parts) > 2 else None
        self.place = parts[3] if len(parts) > 3 else None

    @property
    def date_time_original(self):
        year, month, day = [int(s) for s in self.date.split('_')]
        sec = int(self.number)
        return DTFMT.format(year, month, day, sec // 60, sec % 60)

    @property
    def lat(self):
        return PLACES[self.place.lower()][0]

    @property
    def lon(self):
        return PLACES[self.place.lower()][1]

    @property
    def place_name(self):
        return PLACES[self.place.lower()][2]

    @property
    def place_sub_name(self):
        p = PLACES[self.place.lower()]
        return p[3] if len(p) > 3 else None

    def __str__(self):
        parts = [self.prefix, self.number]
        if self.date:
            parts.append(self.date)
        if self.place:
            parts.append(self.place)
        return '__'.join(parts) + '.jpg'


parser = ArgumentParser(description=__doc__)
parser.add_argument('-p', '--prefix',
                    help='''prefix for all output filenames before numbering;
                            if not set, no renaming takes place''',
                    default='', required=False)
parser.add_argument('-d', '--digits',
                    help='number of digits for automatic numbering',
                    default=3, required=False)
parser.add_argument('--set-digitized',
                    help='''set DateTimeDigitized of
                            images to modification date''',
                    default=False, action='store_true', required=False)
parser.add_argument('--dry-run',
                    help='do not make any changes, perform dry run',
                    default=False, action='store_true', required=False)
parser.add_argument('--version',
                    help='Print version number',
                    default=False,
                    action='store_true')


def main():
    args = parser.parse_args()
    if args.version:
        print('''metapic ''' + __version__)
    fmt = args.prefix + '__{:0' + str(args.digits) + 'd}.jpg'
    cwd = Path.cwd()
    print('Working in {}'.format(cwd))
    i = 0
    for image in sorted(list(cwd.iterdir())):
        if image.is_file() and image.suffix.lower() == '.jpg':
            if args.prefix:
                new_name = fmt.format(i)
                if args.dry_run:
                    print('DRY-RUN: Would rename {} to {}'.format(image,
                                                                  new_name))
                else:
                    print('Renaming {} to {}'.format(image, new_name))
                    image.rename(new_name)
                    image = cwd / new_name
            if args.set_digitized:
                if args.dry_run:
                    print('DRY-RUN: Would set DateTimeDigitized ' +
                          'of {}'.format(image))
                else:
                    print('Setting DateTimeDigitized of {}'.format(image))
                    output = subprocess.run(
                        [EXIFTOOL, '-DateTimeDigitized<FileModifyDate',
                         str(image)],
                        stdout=subprocess.PIPE)
                    output.check_returncode()
            try:
                field_name = FieldName(image)
            except Exception:
                continue
            if field_name.date:
                if args.dry_run:
                    print('DRY-RUN: Would set DateTimeOriginal of {} to {}'
                          .format(image, field_name.date_time_original))
                else:
                    print('Setting DateTimeOriginal of {} to {}'.format(
                        image, field_name.date_time_original))
                    output = subprocess.run(
                        [EXIFTOOL, '-DateTimeOriginal=' +
                                   field_name.date_time_original,
                                   str(image)],
                        stdout=subprocess.PIPE)
                    output.check_returncode()
            if field_name.place:
                if args.dry_run:
                    print('DRY-RUN: Would set location of ' +
                          ' {} to {} at lat={}, lon={}'
                          .format(image, field_name.place_name,
                                  field_name.lat, field_name.lon))
                else:
                    print('Setting location of {} to {} at lat={}, lon={}'
                          .format(image, field_name.place_name,
                                  field_name.lat, field_name.lon))
                    fields_set = ['-GPSLatitude={}'.format(field_name.lat),
                                  '-GPSLongitude={}'.format(field_name.lon),
                                  '-LocationShownCity={}'.format(
                                      field_name.place_name)]
                    if field_name.place_sub_name:
                        fields_set.append('-LocationShownSublocation={}'
                                          .format(field_name.place_sub_name))
                    output = subprocess.run([EXIFTOOL, *fields_set,
                                             str(image)],
                                            stdout=subprocess.PIPE)
                    output.check_returncode()
            i += 1


if __name__ == '__main__':
    main()
