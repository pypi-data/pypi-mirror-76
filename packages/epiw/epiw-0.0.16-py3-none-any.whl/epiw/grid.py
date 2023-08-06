import os
import shutil
import subprocess
import tempfile

from dateutil.parser import parse as parse_date
from dateutil.rrule import DAILY, HOURLY, rrule

from epiw import read_as_gpd

_cell_size = 10000
_left, _bottom, _right, _top = 746100, 1458570, 1387980, 2068800


def grid(
        src_path,
        dst_path,
        field,
        query=None, left=_left, bottom=_bottom, right=_right, top=_top, cell_size=_cell_size,
        crs='EPSG:5179',
        algorithm='invdistnn:radius=999999999,max_points=3'
):
    tmp_path = f'{dst_path}.tmp'
    cmd = [
        'gdal_grid',
        '-q',
        '-of', 'GTiff',
        '-ot', 'float32',
        '-co', 'compress=deflate',
        '-co', 'tiled=yes',
        '-zfield', field,
        '-a_srs', crs,
        '-txe', str(left), str(right),
        '-tye', str(top), str(bottom),
        '-where', f'{field} is not null',
        '-outsize', str(int((right - left) / cell_size)), str(int((top - bottom) / cell_size)),
        '-a', algorithm,
        src_path,
        tmp_path
    ]

    if query:
        cmd.append('-query')
        cmd.append(query)

    print(' '.join(cmd))

    env = os.environ
    proc = subprocess.Popen(cmd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = proc.communicate()
    if out:
        try:
            out = out.decode('utf-8')
        except:
            pass

        try:
            err = err.decode('utf-8')
        except:
            pass

        raise Exception(f'Failed to run gdal_grid!\nproc.returncode:{proc.returncode}\nerr:{err}\nout:{out}')
    shutil.move(tmp_path, dst_path)


def create_grid(
        category,
        interval,
        begin,
        field,
        output_dir,
        until=None,
        query=None,
        left=_left,
        bottom=_bottom,
        right=_right,
        top=_top,
        cell_size=_cell_size,
        crs='EPSG:5179',
        algorithm='invdistnn:radius=999999999,max_points=3',
):
    begin = isinstance(begin, str) and parse_date(begin)
    until = isinstance(until, str) and parse_date(until) or begin

    itv = {
        'hourly': HOURLY,
        'daily': DAILY,
    }[interval]
    dates = rrule(itv, begin, until=until)

    output_format = {
        'hourly': f'{output_dir}/%Y/%m/%d/{field}.%Y%m%dT%H%M%S.tiff',
        'daily': f'{output_dir}/%Y/%m/%d/{field}.%Y%m%d.tiff'
    }[interval]

    for date in dates:
        output_path = date.strftime(output_format)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp_dir:
            vect_file_path = f'{output_path}.json'
            data = read_as_gpd(category, interval, begin, fields=[field])
            if data.empty:
                print(f'# Warning: retrieved data is null {category}/{interval}/{begin}/{field}')
                continue
            data = data.set_crs(4326).to_crs(5179)
            data.drop(['tm'], axis=1).to_file(vect_file_path, driver='GeoJSON')

            grid(
                vect_file_path,
                output_path,
                field,
                query=query,
                left=left,
                bottom=bottom,
                right=right,
                top=top,
                cell_size=cell_size,
                crs=crs,
                algorithm=algorithm,
            )
