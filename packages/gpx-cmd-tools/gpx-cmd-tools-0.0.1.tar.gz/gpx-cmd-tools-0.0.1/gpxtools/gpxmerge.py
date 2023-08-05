import argparse
import gpxpy.gpx as gpx
import gpxpy
import datetime
import os.path as path
import datetime

from . import common

from typing import *

def get_time(g: gpx.GPX) -> Optional[datetime.datetime]:
    for t in g.tracks:
        for s in t.segments:
            for pt in s.points:
                if pt.time:
                    return pt.time
    return None

def main() -> None:
    parser = argparse.ArgumentParser(description='Merge GPX files')
    parser.add_argument('gpx_files', metavar='gpx', type=str, default='', nargs='*', help='GPX file')
    parser.add_argument('-o', '--output', metavar='F', type=str, default='merged.gpx', help='Output GPX file')
    parser.add_argument('-t', '--time', action='store_true', help='Sort by time')
    args = parser.parse_args()

    gpx_files = args.gpx_files
    out_file = args.output
    sort_by_time = args.time

    keep_extensions = True

    if not gpx_files:
        print("Nothing to do")
        return

    gpxs: List[gpx.GPX] = []

    for gpx_file in gpx_files:
        print(f"Reading {gpx_file}")
        gpxs.append(gpxpy.parse(open(gpx_file)))

    if sort_by_time:
        print("Sorting by time")
        gpxs = sorted(gpxs, key=get_time)

    base_gpx: Optional[gpx.GPX] = None
    for g in gpxs:
        if base_gpx:
            if len(g.nsmap) != len(base_gpx.nsmap):
                keep_extensions = False
            else:
                for key in base_gpx.nsmap:
                    if not key in g.nsmap or g.nsmap[key] != base_gpx.nsmap[key]:
                        keep_extensions = False
        else:
            base_gpx = g.clone()
            base_gpx.tracks = []
            base_gpx.routes = []
        
        for track in g.tracks:
            print("adding track")
            base_gpx.tracks.append(track)
        for route in g.routes:
            base_gpx.routes.append(route)
        
    if base_gpx:
        if not keep_extensions:
            print("Removing extensions")
            common.clean_extensions(base_gpx)
    
        with open(out_file, "w") as f:
            f.write(base_gpx.to_xml())