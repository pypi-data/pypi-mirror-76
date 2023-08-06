import os
import shutil
import subprocess

_cell_size = 10000
_left, _bottom, _right, _top = 746100, 1458570, 1387980, 2068800


def grid(
        src_path,
        dst_path,
        field,
        query=None, left=_left, bottom=_bottom, right=_right, top=_top, cell_size=_cell_size
):
    tmp_path = f'{dst_path}.tmp'
    cmd = [
        'gdal_grid',
        '-q',
        '-ot', 'float32',
        '-co', 'compress=deflate',
        '-co', 'tiled=yes',
        '-zfield', field,
        '-a_srs', 'EPSG:5179',
        '-txe', str(left), str(right),
        '-tye', str(top), str(bottom),
        '-outsize', str(int((right - left) / cell_size)), str(int((top - bottom) / cell_size)),
        '-a', 'invdistnn:radius=999999999,max_points=3',
        src_path,
        tmp_path
    ]

    if query:
        cmd.append('-query')
        cmd.append(query)

    print(' '.join(cmd))

    proc = subprocess.Popen(cmd, env=os.environ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
