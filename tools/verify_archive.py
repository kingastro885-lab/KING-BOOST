import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
m=json.loads(Path('release/verified-manifest.json').read_text(encoding='utf-8'))
required={'KING_BOOSTER.exe','KING_BOOSTER.exe.config','KingGpuBridge.dll','KingUpdater.exe','KING_BOOSTER.updates.json'}
allowed=required|{'LEGGIMI.txt','LICENSE.txt','NVIDIA_LICENSE.txt','AMD_ADLX_LICENSE.pdf'}
files=m['Files']
assert len(files)==len({f['Name'].lower() for f in files})
assert required<={f['Name'] for f in files}<=(allowed)
assert sum(f['Size'] for f in files)<=100663296
with ZipFile('release/KING_BOOSTER_runtime_x64.zip') as z:
    assert len(z.infolist())==len(files)
    assert len({x.filename.lower() for x in z.infolist()})==len(files)
    assert set(z.namelist())=={f['Name'] for f in files}
    for f in files:
        info=z.getinfo(f['Name'])
        assert info.file_size==f['Size'] and 0<f['Size']<=33554432
        assert (info.external_attr>>16)&0xf000!=0xa000
        data=z.read(f['Name'])
        assert len(data)==f['Size'] and hashlib.sha256(data).hexdigest()==f['Sha256']
print('Contenuto runtime verificato')
