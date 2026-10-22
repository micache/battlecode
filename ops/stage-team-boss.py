#!/usr/bin/env python3
"""Read the current own-team source in the approved browser and stage it privately.

No contest upload/activation and no cookie/token export. Run the stopped server
configurator afterward; staging alone never changes the live arena opponent.
"""
import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shlex
import sys
import time
import uuid
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from arena.common import atomic_bytes,atomic_json,canonical,lock,read_json,require
from arena.protocol import decode_source
from ops.blaxel import APIError,Client,CREDENTIALS

SAVE='''import base64,json,pathlib,sys,uuid
sys.path.insert(0,'/opt/battlecode')
from arena.common import atomic_json,read_json,require
from arena.protocol import decode_source
v=json.loads(base64.b64decode(sys.argv[1]));p=v['proof'];sid=str(uuid.UUID(p['active']['id']))
_,digest=decode_source(v['source'])
require(digest==p['source_hash'] and p['team_id']==read_json('/etc/battlecode/arena.json')['official_exploration']['team_id'],'boss source/team mismatch')
target=pathlib.Path('/srv/battlecode/boss')/('source-envelope-'+sid+'.json')
if target.exists():
 old=read_json(target)
 require(old['source']==v['source'] and all(old['proof'][k]==p[k] for k in ['team_id','source_hash','package_sha256']), 'existing immutable boss envelope differs')
else:atomic_json(target,v,384)
print(json.dumps({'source_envelope':str(target),'submission_id':sid,'source_hash':digest}))
'''


def main():
    from playwright.sync_api import sync_playwright
    # Reuse the already-reviewed bounded ZIP/path validation.
    spec=importlib.util.spec_from_file_location('source_attestation',Path(__file__).with_name('attest-official-exploration.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    root=Path.home()/'.local/share/battlecode-exploration';root.mkdir(mode=0o700,parents=True,exist_ok=True)
    with lock(root/'attestation.lock'):
        with sync_playwright() as p:
            browser=p.chromium.launch_persistent_context(str(Path.home()/'.local/share/battlecode-contest-browser'),headless=True)
            try:
                listing=browser.request.get(module.ORIGIN+'/api/v1/submissions',timeout=60000)
                require(listing.ok,'owner browser login/access required: HTTP '+str(listing.status))
                data=listing.json();active,selected=data.get('active'),data.get('selected')
                require(active and selected and active['id']==selected['id'] and active['status']=='active' and
                        active['language']=='cpp','active and selected must identify the same compiled C++ bot')
                sid=str(uuid.UUID(active['id']))
                response=browser.request.get(module.ORIGIN+'/api/v1/submissions/'+sid+'/archive',timeout=60000)
                require(response.ok,'own-team archive access stop: HTTP '+str(response.status))
                package=response.body();digest=module.archive_source_hash(package)
            finally:browser.close()
        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            files=[v for v in archive.infolist() if not v.is_dir()]
            parts=Path(files[0].filename).parts;prefix='/'.join(parts[:parts.index('src')+1])+'/'
            source={v.filename.removeprefix(prefix):base64.b64encode(archive.read(v)).decode() for v in files}
        require(decode_source(source)[1]==digest,'source archive identities differ')
        proof={'team_id':data['team']['id'],'active':active,'selected':selected,'source_hash':digest,
               'package_sha256':hashlib.sha256(package).hexdigest(),'observed_at':time.time()}
        envelope={'source':source,'proof':proof}
        private=root/'boss';private.mkdir(mode=0o700,exist_ok=True)
        cached=private/(sid+'.json')
        if cached.exists():require(all(read_json(cached)[k]==proof[k] for k in
            ['team_id','source_hash','package_sha256']),'immutable own submission archive changed')
        atomic_bytes(private/(sid+'.zip'),package,0o600)
        atomic_json(private/(sid+'.json'),proof,0o600)
        credentials=read_json(CREDENTIALS);client=Client(credentials['key'],credentials['workspace']);endpoint=client.endpoint()
        name='stage-team-boss-'+sid
        try:result=client.request('GET','/process/'+name,base=endpoint)
        except APIError as exc:
            if exc.code!=404:raise
            encoded=base64.b64encode(canonical(envelope)).decode()
            require(len(encoded)<200000,'source transfer exceeds reviewed bound')
            result=client.request('POST','/process',{'name':name,'command':shlex.join([
                'python3','/opt/battlecode/ops/as-arena.py','python3','-c',SAVE,encoded]),
                'waitForCompletion':False,'keepAlive':True,'timeout':0},base=endpoint)
        until=time.monotonic()+20
        while result['status']=='running' and time.monotonic()<until:
            time.sleep(2);result=client.request('GET','/process/'+name,base=endpoint)
        require(result['status']=='completed' and result['exitCode']==0,'staging pending/failed; reconcile process '+name)
        print(result['stdout'].strip())


if __name__=='__main__':main()
