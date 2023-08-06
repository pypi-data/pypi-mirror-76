#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Fits a batch profile to a set of data.

This script can be used to fit multiple models to multiple datasets. It needs a batch profile with information
about the subjects. If no batch profile is given, this routine will try to auto-detect a good batch profile.

The most general batch profile is the 'DirPerSubject' profile which assumes that every subject has
its own subdirectory under the given data folder. For details, please look up the batch profiles in your home folder.

A few of the batch profile settings can be altered with arguments to this script. For example,
use_gradient_deviations and models_to_fit override the values in the batch profile.
"""
import argparse
import os
import mdt
from argcomplete.completers import FilesCompleter
from mdt.lib.batch_utils import batch_profile_factory, SelectedSubjects
from mdt.lib.components import get_component_list

from mdt.lib.shell_utils import BasicShellApplication
from mot.lib import cl_environments
import textwrap

__author__ = 'Robbert Harms'
__date__ = "2015-08-18"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"


class BatchFit(BasicShellApplication):

    def __init__(self):
        super().__init__()
        self.available_devices = list((ind for ind, env in
                                       enumerate(cl_environments.CLEnvironmentFactory.smart_device_selection())))

    def _get_arg_parser(self, doc_parser=False):
        description = textwrap.dedent(__doc__)

        examples = textwrap.dedent('''
            mdt-batch-fit . NODDI
            mdt-batch-fit /data/mgh 'BallStick_r1' --batch-profile 'HCP_MGH'
            mdt-batch-fit . CHARMED_r1 --subjects-id 1003 1004 --subjects-index 0 1 2
            mdt-batch-fit . BallStick_r1 Tensor --dry-run
        ''')
        epilog = self._format_examples(doc_parser, examples)

        batch_profiles = get_component_list('batch_profiles')

        parser = argparse.ArgumentParser(description=description, epilog=epilog,
                                         formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('data_folder', help='the directory with the subject to fit').completer = FilesCompleter()

        parser.add_argument('models_to_fit', type=str, nargs='*', help="The models to fit")

        parser.add_argument('-o', '--output_folder',
                            help='the directory for the output, defaults to an output dir next to the input dir.')\
            .completer = FilesCompleter()

        parser.add_argument('-b', '--batch_profile', default=None, choices=batch_profiles,
                            help='The batch profile (by name) to use during fitting. If not given a'
                                 'batch profile is auto-detected.')

        parser.add_argument('--cl-device-ind', type=int, nargs='*', choices=self.available_devices,
                            help="The index of the device we would like to use. This follows the indices "
                                 "in mdt-list-devices and defaults to the first GPU.")

        parser.add_argument('--recalculate', dest='recalculate', action='store_true',
                            help="Recalculate the model(s) if the output exists.")
        parser.add_argument('--no-recalculate', dest='recalculate', action='store_false',
                            help="Do not recalculate the model(s) if the output exists. (default)")
        parser.set_defaults(recalculate=False)

        parser.add_argument('--use-gradient-deviations', dest='use_gradient_deviations', action='store_true',
                            help="Uses the gradient deviations. If not set, the default in the profile is used.")
        parser.add_argument('--no-gradient-deviations', dest='use_gradient_deviations', action='store_false',
                            help="Disable the use of gradient deviations. If not set, the default "
                                 "in the profile is used.")
        parser.set_defaults(use_gradient_deviations=None)

        parser.add_argument('--double', dest='double_precision', action='store_true',
                            help="Calculate in double precision.")
        parser.add_argument('--float', dest='double_precision', action='store_false',
                            help="Calculate in single precision. (default)")
        parser.set_defaults(double_precision=False)

        parser.add_argument('--subjects-index', type=int, nargs='*',
                            help="The indices of the subjects we would like to fit. This reduces the set of "
                                 "subjects.")

        parser.add_argument('--subjects-id', type=str, nargs='*',
                            help="The id of the subjects we would like to fit. This reduces the set of "
                                 "subjects.")

        parser.add_argument('--dry-run', dest='dry_run', action='store_true',
                            help="Shows what it will do without the dry run argument.")
        parser.set_defaults(dry_run=False)

        parser.add_argument('--tmp-results-dir', dest='tmp_results_dir', default='True', type=str,
                            help='The directory for the temporary results. The default ("True") uses the config file '
                                 'setting. Set to the literal "None" to disable.').completer = FilesCompleter()

        return parser

    def run(self, args, extra_args):
        batch_profile = batch_profile_factory(args.batch_profile, os.path.realpath(args.data_folder))

        subjects_selection = None
        if args.subjects_index or args.subjects_id:
            indices = args.subjects_index if args.subjects_index else []
            subject_ids = args.subjects_id if args.subjects_id else []

            subjects_selection = SelectedSubjects(indices=indices, subject_ids=subject_ids)

        tmp_results_dir = args.tmp_results_dir
        for match, to_set in [('true', True), ('false', False), ('none', None)]:
            if tmp_results_dir.lower() == match:
                tmp_results_dir = to_set
                break

        mdt.batch_fit(os.path.realpath(args.data_folder),
                      args.models_to_fit,
                      output_folder=args.output_folder,
                      subjects_selection=subjects_selection,
                      batch_profile=batch_profile,
                      recalculate=args.recalculate,
                      cl_device_ind=args.cl_device_ind,
                      double_precision=args.double_precision,
                      dry_run=args.dry_run,
                      tmp_results_dir=tmp_results_dir,
                      use_gradient_deviations=args.use_gradient_deviations)


def get_doc_arg_parser():
    return BatchFit().get_documentation_arg_parser()


if __name__ == '__main__':
    BatchFit().start()
