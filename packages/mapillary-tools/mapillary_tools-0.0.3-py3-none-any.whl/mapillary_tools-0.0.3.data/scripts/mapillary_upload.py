#!python

''' Upload images to Mapillary.

Sorts images into sequences and uploads them to the Mapillary server.

Upload images from a directory:

  mapillary_upload.py ~/Pictures/Mapillary/*.jpg
  mapillary_upload.py -n -v ~/Pictures/Mapillary/*.jpg
  mapillary_upload.py -d 50 -t 5 ~/Pictures/Mapillary/*.jpg

Upload images from a list of images (one complete filepath per line):

  mapillary_upload.py @picture_list.txt
  find ~/Pictures/Mapillary/ -name "*.jpg" | mapillary_upload.py @/dev/stdin

'''

import itertools
import logging
from multiprocessing.dummy import Pool
import operator

from tqdm import tqdm

import mapillary_tools as mt


SEQUENCE_THREADS = 2 # upload this many sequences in parallel
UPLOAD_THREADS   = 2 # upload this many images in parallel per sequence

DEFAULT_MAX_TIME = 5 * 60.0 # in seconds. max time between images in same sequence
DEFAULT_MAX_DIST = 100.0    # in meters.  max distance between images in same seq.
DEFAULT_MAX_DOP  = 20.0     # discard images with GPS DOP greater than this


def build_parser ():
    ''' Build the commandline parser. '''

    parser = mt.build_parser (__doc__)

    parser.add_argument (
        'images', metavar='FILENAME', type=str, nargs='+',
        help='the images to upload'
    )

    parser.add_argument (
        '-n', '--dry-run', dest='dry_run', action='store_true',
        help='dry run: do not upload any images',
    )
    parser.add_argument (
        '-t', '--t_max', type = float, metavar='SECONDS',
        help='max time delta between images in sequence', default=DEFAULT_MAX_TIME
    )
    parser.add_argument (
        '-d', '--d_max', type = float, metavar='METERS',
        help='max distance between images in sequence', default=DEFAULT_MAX_DIST
    )
    parser.add_argument (
        '--dop_max', type = float, metavar='DOP',
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

        if gt.get ('MAPDOP', 1.0) > args.dop_max:
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
        if not args.dry_run:
            for geotags in sequence:
                del geotags['sequence_id']
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

    geotags = mt.cut_sequences (geotags, args.t_max, args.d_max)
    parameters = [(args, k, list (v)) for k, v in itertools.groupby (
        geotags, operator.itemgetter ('sequence_id'))]

    logging.info ('Sequenced %d images in %d sequences', len (geotags), len (parameters))

    with tqdm (total = len (geotags), desc = 'Dry run' if args.dry_run else 'Uploading',
               unit = 'image', smoothing = 0, disable = args.verbose == 0) as args.pbar:

        with Pool (SEQUENCE_THREADS) as seq_pool:
            seq_pool.starmap (upload_sequence, parameters)

    logging.info ('Done.')


if __name__ == '__main__':
    main ()
