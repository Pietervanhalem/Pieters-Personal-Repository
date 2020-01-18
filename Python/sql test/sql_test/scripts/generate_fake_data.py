"""Use this script to generate fake CPT data."""
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from faker import Faker

fake = Faker()
fake.seed(0)


def usage(argv):
    """Give feedback on commandline usage."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <file_path> <# cpt> <# psd>\n'
          '(example: "%s faux_data 100 1000")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Put fake CPT and PSD files to folder.
    Every PSD files contains 20 PSD samples.
    """
    if len(argv) < 3:
        usage(argv)
    folder = Path(argv[1])
    folder.mkdir()
    cpt_folder = folder.joinpath('cpt')
    cpt_folder.mkdir()

    num_cpts = int(argv[2])

    for cpt in range(num_cpts):
        filename = ('CPT name=CPT-{}-{},date={:%Y%m%d},'
                    'latitude={:0.3f},longitude={:0.3f}.csv').format(
            fake.building_number(),
            fake.country_code(),
            fake.date_time_this_year(),
            fake.latitude(),
            fake.longitude())

        path = cpt_folder.joinpath(filename)

        depths = np.arange(0, 3, 0.02)
        df = pd.DataFrame(
            {'depth': depths,
             'qc': abs(np.cos((depths + 1)**5)) + depths**.3,
             'fs': abs(np.sin(depths)**2 + np.cos((depths + 12)**5) / 1.2)
             })
        df.to_csv(str(path))

    psd_folder = folder.joinpath('psd')
    psd_folder.mkdir()

    num_psds = int(argv[3])

    for psd in range(num_psds):
        filename = ('PSD name=PSD-{}-{},date={:%Y%m%d}.csv').format(
            fake.building_number(),
            fake.country_code(),
            fake.date_time_this_year())
        path = psd_folder.joinpath(filename)
        name = filename.split(',')[0].split('=')[1]
        df = pd.DataFrame([fake_psd(name + '-' + str(i)) for i in range(20)])
        df.index = df['name']
        df.sort_index().to_csv(str(path))


def fake_psd(name):
    """Create fake PSD data."""
    return {
        'name': name,
        'latitude': fake.latitude(),
        'longitude': fake.longitude(),
        'density': fake.random.randrange(1100, 1600),
        'quality': fake.random_element(('good', 'bad'))
    }


if __name__ == "__main__":
    main()
