import concurrent.futures, hashlib, json, pathlib, sys, time, urllib.error, urllib.parse, urllib.request
# Raw API state stays outside the repository; pass the release directory as argv[2].
W=pathlib.Path(sys.argv[2])
SITE='cfe11c44-420e-4af6-9472-e2c4570d84c5'
c=json.loads((pathlib.Path.home()/'Library/Preferences/netlify/config.json').read_text())
TOKEN=c['users'][c['userId']]['auth']['token']
def api(path,data=None,method=None,binary=False):
    headers={'Authorization':'Bearer '+TOKEN}
    if data is not None:
        headers['Content-Type']='application/octet-stream' if binary else 'application/json'
        if not binary: data=json.dumps(data).encode()
    with urllib.request.urlopen(urllib.request.Request('https://api.netlify.com/api/v1'+path,data=data,headers=headers,method=method),timeout=40) as r:
        raw=r.read(); return json.loads(raw) if raw else {}
base=json.loads((W/'base-deploy.json').read_text())
original={x['path']:x['sha'] for x in json.loads((W/'base-files.json').read_text())}
package=json.loads((W/'package/data-package.json').read_text())
paths={x['path']:W/'package'/x['path'].lstrip('/') for x in package['files']}
files=original.copy()
for name,p in paths.items():
    assert name.startswith('/company/data/')
    files[name]=hashlib.sha1(p.read_bytes()).hexdigest()
assert all(files[k]==v for k,v in original.items() if k not in paths)
assert all(files[k]==v for k,v in original.items() if k.startswith('/product/one/'))
fc={}
for f in base['available_functions']:
    fm={'dn':'display_name','g':'generator','bd':'build_data','p':'priority','tr':'traffic_rules'}
    cfg={v:f[k] for k,v in fm.items() if f.get(k) is not None}
    if f.get('ro'):
        rm={'p':'pattern','l':'literal','e':'expression','m':'methods','ps':'prefer_static'}
        cfg['routes']=[{v:r[k] for k,v in rm.items() if r.get(k) is not None} for r in f['ro']]
    fc[f['n']]=cfg
payload={'files':files,'functions':{f['n']:f['d'] for f in base['available_functions']},'functions_config':fc,'function_schedules':base.get('function_schedules') or [],'framework':base.get('framework','unknown')}
assert all(files[k]==v for k,v in original.items() if not k.startswith('/company/data/'))
payload_bytes=json.dumps(payload,sort_keys=True).encode(); phash=hashlib.sha256(payload_bytes).hexdigest()
(W/'payload.json').write_bytes(payload_bytes)
mode=sys.argv[1]; assert mode in ('draft','production')
if mode=='production':
    qa=json.loads((W/'draft-qa.json').read_text()); assert qa['passed'] and qa['payload_sha256']==phash
statefile=W/(mode+'-state.json')
if statefile.exists():
    did=json.loads(statefile.read_text())['deploy_id']; deploy=api('/deploys/'+did)
else:
    assert api('/sites/'+SITE)['published_deploy']['id']==base['id'],'Production changed; rebase required'
    request=payload|{'draft':mode=='draft','title':'ForFlow data partnerships: public release at /company/data/'}
    deploy=api('/sites/'+SITE+'/deploys',request,'POST'); did=deploy['id']
    statefile.write_text(json.dumps({'deploy_id':did,'base':base['id'],'payload_sha256':phash},indent=2))
    print(json.dumps({'id':did,'state':deploy['state'],'required_files':len(deploy.get('required') or [])}),flush=True)
required=set(deploy.get('required') or [])
by_hash={hashlib.sha1(p.read_bytes()).hexdigest():(name,p) for name,p in paths.items()}
assert not required-set(by_hash), 'Unexpected preserved-file upload required'
def upload(digest):
    name,p=by_hash[digest]
    api('/deploys/'+did+'/files'+urllib.parse.quote(name),p.read_bytes(),'PUT',True)
    return name
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    uploaded=list(pool.map(upload,required))
if uploaded: print(json.dumps({'uploaded':len(uploaded)}),flush=True)
for f in base['available_functions']:
    if f['d'] not in (deploy.get('required_functions') or []): continue
    candidates=[pathlib.Path('/tmp/forflow-product-one-production/stream-fix')/(f['n']+'.zip'),pathlib.Path('/Users/zezhou/Documents/Forflow website/.netlify/functions')/(f['n']+'.zip')]
    p=next((p for p in candidates if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==f['d']),None)
    assert p is not None, 'Missing unchanged function archive: '+f['n']
    invocation='&invocation_mode='+f['im'] if f.get('im') else ''
    api('/deploys/'+did+'/functions/'+f['n']+'?runtime=js'+invocation,p.read_bytes(),'PUT',True)
for _ in range(20):
    deploy=api('/deploys/'+did)
    if deploy['state'] in ('ready','error'):break
    time.sleep(2)
assert deploy['state']=='ready',(deploy['state'],deploy.get('error_message'))
assert deploy['edge_functions_present']
assert {f['n']:f['d'] for f in deploy['available_functions']}==payload['functions']
for f in deploy['available_functions']:
    old=next(o for o in base['available_functions'] if o['n']==f['n'])
    for key in ['bd','ro','tr','p','im']:assert f.get(key)==old.get(key),(f['n'],key)
listing=[]
for page in range(1,101):
    batch=api('/deploys/'+did+'/files?per_page=100&page='+str(page)); listing.extend(batch)
    if len(batch)<100:break
actual={x['path'].lower():x['sha'] for x in listing}
for name,digest in files.items():
    if name not in ('/_redirects','/_headers'):assert actual[name.lower()]==digest,('digest mismatch',name)
published=api('/sites/'+SITE)['published_deploy']['id']
assert published==(did if mode=='production' else base['id'])
(W/(mode+'-deploy.json')).write_text(json.dumps(deploy,indent=2))
(W/(mode+'-files.json')).write_text(json.dumps(listing,indent=2))
print(json.dumps({'id':did,'state':'ready','url':deploy['deploy_ssl_url'],'published':published,'files':len(listing),'functions_preserved':True,'existing_files_preserved':sum(k not in paths for k in original),'product_files_preserved':sum(k.startswith('/product/one/') for k in original),'payload_sha256':phash}),flush=True)
