#!/usr/bin/env python

'''Upload images to Mapillary.

Sorts images into sequences and uploads them to the Mapillary server.

Upload images from a directory:

  mapillary_upload.py ~/Pictures/Mapillary/*.jpg
  mapillary_upload.py -n -v ~/Pictures/Mapillary/*.jpg
  mapillary_upload.py -d 50 -t 5 ~/Pictures/Mapillary/*.jpg

Upload images from a list of images (one complete filepath per line):

  mapillary_upload.py @picture_list.txt
  find ~/Pictures/Mapillary/ -name "*.jpg" | mapillary_upload.py @/dev/stdin

Upload images extracted from a video of a dashcam facing 90° left to the
direction of travel:

  mapillary_upload.py --add-direction=270 ~/Pictures/Dashcam/*.jpg

'''

import itertools
import logging
from multiprocessing.dummy import Pool
import operator

from tqdm import tqdm

import mapillary_tools as mt


SEQUENCE_THREADS = 2 # upload this many sequences in parallel
UPLOAD_THREADS   = 2 # upload this many images in parallel per sequence

DEFAULT_MAX_TIME     = 5 * 60.0 # in seconds. max time between images in same sequence
DEFAULT_MAX_DISTANCE = 100.0    # in meters.  max distance between images in same seq.
DEFAULT_MAX_DOP      = 20.0     # discard images with GPS DOP greater than this


def build_parser ():
    ''' Build the commandline parser. '''

    parser = mt.build_parser (__doc__)

    parser.add_argument (
        'images', metavar='FILENAME', type=str, nargs='+',
        help='the images to upload'
    )

    parser.add_argument (
        '-n', '--dry-run', action='store_true',
        help='dry run: do not upload any images',
    )
    parser.add_argument (
        '--add-direction', type = float, metavar='DEGREES',
        help='calculate image direction from successive GPS positions and apply an offset of DEGREES', default = None
    )
    parser.add_argument (
        '--max-time', type = float, metavar='SECONDS',
        help='max time delta between images in sequence', default=DEFAULT_MAX_TIME
    )
    parser.add_argument (
        '--max-distance', type = float, metavar='METERS',
        help='max distance between images in sequence', default=DEFAULT_MAX_DISTANCE
    )
    parser.add_argument (
        '--max-dop', type = float, metavar='DOP',
        help='discard images with GPS DOP greater than this', default=DEFAULT_MAX_DOP
    )
    return parser


def build_list (args):
    ''' Build a list of files to upload '''

    geotags = []
    discarded = 0
    errors = 0

    for filename in args.images:
        try:
            gt = mt.read_sidecar_file (filename)
        except mt.MapillaryError as e:
            errors += 1
            logging.exception (e)
            continue

        if gt.get ('status_code', 0) == 204:
            discarded += 1
            logging.warning ('%s was already uploaded', filename)
            continue

        if 'MAPLatitude' not in gt or 'MAPCaptureTime' not in gt:
            discarded += 1
            logging.warning ('%s has no GPS data', filename)
            continue

        if gt.get ('MAPDOP', 1.0) > args.max_dop:
            discarded += 1
            logging.warning ('%s exceeds max GPS DOP', filename)
            continue

        geotags.append (gt)

    logging.info ('%d images were discarded and %d had errors', discarded, errors)

    return geotags


def upload_image (args, session, geotags):
    ''' Upload one image. '''

    geotags = mt.upload_image (session, geotags, args.dry_run)
    args.pbar.update ()

    return geotags


def upload_sequence (args, sequence_id, sequence):
    ''' Upload a sequence of images. '''

    try:
        upload_token = args.config[args.config.sections()[0]]['user_upload_token']
        with mt.managed_session (upload_token, args.dry_run) as session:
            with Pool (UPLOAD_THREADS) as pool:
                sequence = pool.starmap (upload_image, zip (
                    itertools.repeat (args),
                    itertools.repeat (session),
                    sequence,
                ))

        # write status into sidecars only if the sequence was successful
        for geotags in sequence:
            if args.dry_run:
                del geotags['status_code']
            mt.write_sidecar_file (geotags['filename'], geotags)

    except mt.SequenceUploadError as e:
        logging.exception (e)

    return sequence


def main ():
    ''' Main function. '''

    args = build_parser ().parse_args ()
    mt.init_logging (args.verbose)
    args.config = mt.read_config_file ()

    geotags = build_list (args)
    if len (geotags) == 0:
        logging.info ('No images to upload.')
        return

    geotags = mt.cut_sequences (geotags, args.max_time, args.max_distance)
    parameters = []

    for k, v in itertools.groupby (geotags, operator.itemgetter ('sequence_id')):
        sequence = list (v)
        if args.add_direction is not None:
            mt.interpolate (sequence, args.add_direction)
        parameters.append ((args, k, sequence))

    logging.info ('Sequenced %d images in %d sequences', len (geotags), len (parameters))

    with tqdm (total = len (geotags), desc = 'Dry run' if args.dry_run else 'Uploading',
               unit = 'image', smoothing = 0, disable = args.verbose == 0) as args.pbar:

        with Pool (SEQUENCE_THREADS) as seq_pool:
            seq_pool.starmap (upload_sequence, parameters)

    logging.info ('Done.')


if __name__ == '__main__':
    main ()
