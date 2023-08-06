#!python

'''Extract EXIF info from discrete image files.

Extract Latitude, Longitude, Altitude, DateTime and Heading from the image files
and put the information into sidecar files (same filename with an added extension
of .mapillary).

Process images from a directory:

  mapillary_process.py ~/Pictures/Mapillary/*.jpg

Process images from a list of images (one complete filepath per line):

  mapillary_process.py @picture_list.txt
  find ~/Pictures/Mapillary -name "*.jpg" | mapillary_process.py @/dev/stdin

'''

import logging

import mapillary_tools as mt


def build_parser ():
    ''' Build the commandline parser. '''

    parser = mt.build_parser (__doc__)

    parser.add_argument (
        'images', metavar='FILENAME', type=str, nargs='+',
        help='the images to process'
    )

    parser.add_argument (
        '--clean', action='store_true',
        help='remove sidecar files for selected images'
    )
    return parser


def main ():
    ''' The main function. '''

    args = build_parser ().parse_args ()
    mt.init_logging (args.verbose)

    if args.clean:
        for image in args.images:
            mt.delete_sidecar_file (image)
            logging.info (image)
        return

    for image in args.images:
        logging.info (image)

        geotags = mt.read_sidecar_file (image)
        mt.set_uuid (geotags)

        try:
            geotags.update (mt.get_image_geotags (image))
            mt.write_sidecar_file (image, geotags)

        except mt.MapillaryError as e:
            logging.exception (e)

        if 'MAPCaptureTime' not in geotags:
            logging.warning ('%s has no timestamp', image)

        if 'MAPLatitude' not in geotags:
            logging.warning ('%s has no GPS data', image)


if __name__ == '__main__':
    main ()
