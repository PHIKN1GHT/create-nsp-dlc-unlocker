import os
import shutil
from typing import List


WORKDIR = "workdir"
PRODKEY = "prod.keys"  # USE YOUR OWN KEY
TITLE_IDS: List[str] = []  # INPUT DLC TITLE IDS HERE


def ensure_dir(path: str, clean_up=False) -> None:
    if clean_up and os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    elif not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    ensure_dir(WORKDIR)

    for title_id in TITLE_IDS:
        romfs_dir = os.path.join(WORKDIR, f"romfs_{title_id}")
        output_dir = os.path.join(WORKDIR, f"output_{title_id}")
        temp_dir = os.path.join(WORKDIR, f"temp_{title_id}")
        ensure_dir(romfs_dir, True)
        ensure_dir(output_dir, True)
        ensure_dir(temp_dir, True)

        # GENERATE NCA
        open(os.path.join(romfs_dir, f"empty_file_{title_id}"), "w").write("")
        common_options = f" --type=nca --titleid={title_id} -k {PRODKEY} --romfsdir={romfs_dir} --tempdir={temp_dir} -o {output_dir}"
        cmd = f"hacpack --ncatype=publicdata" + common_options
        os.system(cmd)
        nca_path = ""
        for _, __, files in os.walk(output_dir):
            for file in files:
                nca_path = os.path.join(output_dir, file)

        # GENERATE META NCA
        if nca_path.endswith('nca'):
            cmd = f"hacpack --ncatype=meta --titletype=addon --publicdatanca={nca_path}" + common_options
            os.system(cmd)

        # GENERATE NSP
        cmd = f"hacpack --type=nsp --titleid={title_id} -k {PRODKEY} --ncadir={output_dir} -o {WORKDIR}"
        os.system(cmd)
