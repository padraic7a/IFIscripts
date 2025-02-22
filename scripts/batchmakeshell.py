#!/usr/bin/env python3

import argparse
import os
import sys
import shutil


def set_options():
    parser = argparse.ArgumentParser(
        description='IFI Irish Film Institute AIPs shell creator.'
                    ' Written by Yazhou He.'
    )
    parser.add_argument(
        'input'
    )
    parser.add_argument(
        '-as11',
        action='store_true',
        help='AS-11 UK DPP requires files except .mxf (A&V) files in the objects folder kept.'
    )
    parser.add_argument(
        '-dcp',
        action='store_true',
        help='Digital Cinema Package (DCP) requires files except .mxf (A&V) files in the objects folder kept.'
    )
    parser.add_argument(
        '-o',
        help='Set output directory.', required=True
    )
    return parser.parse_args()


def main():
    args = set_options()
    input = args.input
    output = args.o
    if not os.path.exists(input):
        print("Input directory doesn't exist! Exit...")
        sys.exit()
    if not os.path.exists(output):
        print("Output directory doesn't exist! Exit...")
        sys.exit()
    for root, dirs, files in os.walk(input):
        aip = os.path.basename(root)
        if 'aaa' in aip:
            aip_fpath = root
            print("\nAIP has found: %s" % aip_fpath)
            aip_dest = aip + '_shell'
            aip_dest_fpath = os.path.join(output, aip_dest)
            try:
                os.mkdir(aip_dest_fpath)
                print("\nMaking %s in %s" % (aip_dest, output))
            except:
                print("%s already exists in the output directory %s" % (aip_dest, output))
                sys.exit()
            for aroot, adirs, afiles in os.walk(aip_fpath):
                dir_path = aroot.replace(aip_fpath, "")
                dir_path = dir_path[1:]
                print("\nroot: %s\nsubfolders: %s\nsubfiles: %s" % (dir_path, adirs, afiles))
                if adirs:
                    print("\t---clone folders---")
                    for adir in adirs:
                        adir_copy_fpath = os.path.join(aroot, adir)
                        adir_dest = os.path.join(aip_dest, dir_path, adir)
                        adir_dest_fpath = os.path.join(output, adir_dest)
                        print("\t Source:\t" + adir_copy_fpath)
                        os.mkdir(adir_dest_fpath)
                        print("\t Destination:\t" + adir_dest_fpath)
                if afiles:
                    print("\t---copy files---")
                    for afile in afiles:
                        afile_copy_fpath = os.path.join(aroot, afile)
                        afile_dest_fpath = os.path.join(output, aip_dest, dir_path, afile)
                        if "objects" in afile_copy_fpath:
                            if args.as11 or args.dcp:
                                if not afile_dest_fpath.endswith(".mxf"):
                                    print("\t Source:\t" + afile_copy_fpath)
                                    shutil.copy(afile_copy_fpath, afile_dest_fpath)
                                    print("\t Destination:\t" + afile_dest_fpath)
                                else:
                                    print("\t*Skip:\t\t" + afile_copy_fpath)
                            else:
                                print("\t*Skip:\t\t" + afile_copy_fpath)
                        else:
                            print("\t Source:\t" + afile_copy_fpath)
                            shutil.copy(afile_copy_fpath, afile_dest_fpath)
                            print("\t Destination:\t" + afile_dest_fpath)


if __name__ == "__main__":
    main()
