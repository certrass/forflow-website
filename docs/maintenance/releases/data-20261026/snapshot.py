import json, pathlib, sys, urllib.request
W = pathlib.Path(sys.argv[1]); W.mkdir(parents=True, exist_ok=True)
SITE = 'cfe11c44-420e-4af6-9472-e2c4570d84c5'
c = json.loads((pathlib.Path.home()/'Library/Preferences/netlify/config.json').read_text())
token = c['users'][c['userId']]['auth']['token']
def api(path):
    req=urllib.request.Request('https://api.netlify.com/api/v1'+path,headers={'Authorization':'Bearer '+token})
    with urllib.request.urlopen(req,timeout=40) as r: return json.load(r)
site=api('/sites/'+SITE)
base=api('/deploys/'+site['published_deploy']['id'])
assert base['state']=='ready' and base['edge_functions_present']
listing=[]
for page in range(1,101):
    batch=api('/deploys/'+base['id']+'/files?per_page=100&page='+str(page)); listing.extend(batch)
    if len(batch)<100: break
assert len(listing)>0
for name,data in [('base-deploy.json',base),('base-files.json',listing)]:
    path=W/name
    assert not path.exists(), 'Snapshot already exists; do not overwrite a release base'
    path.write_text(json.dumps(data,indent=2))
summary={'site_id':SITE,'production_base':base['id'],'file_count':len(listing),'function_count':len(base['available_functions']),'edge_functions_present':base['edge_functions_present'],'git_cd_connected':bool(site.get('build_settings',{}).get('repo_url')),'existing_data_paths':[x['path'] for x in listing if x['path'].startswith('/company/data/')]}
(W/'base-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary))
