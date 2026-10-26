import concurrent.futures, hashlib, json, pathlib, re, subprocess, sys, tempfile, time, urllib.parse

from bs4 import BeautifulSoup
W=pathlib.Path(sys.argv[2]);mode=sys.argv[1]
d=json.loads((W/(mode+'-deploy.json')).read_text());origin=d['deploy_ssl_url']
def pretty_url_changes_only(expected,actual):
 a=re.split(rb'(<a\b[^>]*>)',expected);b=re.split(rb'(<a\b[^>]*>)',actual)
 if len(a)!=len(b):return False
 for i,(left,right) in enumerate(zip(a,b)):
  if i%2==0:
   if left!=right:return False
  else:
   attrs=dict(BeautifulSoup(left,'html.parser').a.attrs)
   if 'href' in attrs:
    attrs['href']=re.sub(r'(https://forflow\.ai/[^?#]*)\.html(?=[?#]|$)',r'\1',attrs['href'])
   if attrs!=dict(BeautifulSoup(right,'html.parser').a.attrs):return False
 return True
def fetch(base,path,follow=True):
 with tempfile.TemporaryDirectory(prefix='forflow-company-check-') as temp:
  body=pathlib.Path(temp)/'body';headers=pathlib.Path(temp)/'headers'
  args=['curl','-sS','--retry','2','--retry-all-errors','--retry-delay','1','--max-time','25','-D',str(headers),'-o',str(body),'-w','%{http_code}']
  if follow:args.append('-L')
  args.append(base+urllib.parse.quote(path,safe='/?=&'))
  r=subprocess.run(args,check=True,capture_output=True,text=True)
  h={}
  for line in headers.read_text().splitlines():
   if line.startswith('HTTP/'):h={}
   elif ':' in line:
    k,v=line.split(':',1);h[k.lower()]=v.strip()
  return int(r.stdout),h,body.read_bytes()
package=json.loads((W/'package/data-package.json').read_text())
def verify_file(entry):
 name=entry['path'];expected=(W/'package'/name.lstrip('/')).read_bytes()
 for attempt in range(3):
  try:
   status,h,body=fetch(origin,name)
   assert status==200,(name,status)
   transformation=None
   if body!=expected:
    injected=re.findall(rb'<script>[^<]*__CF\$cv\$params[^<]*</script>',body)
    if len(injected)==1 and b'/cdn-cgi/challenge-platform/scripts/jsd/main.js' in injected[0] and body.replace(injected[0],b'')==expected:
     transformation='Cloudflare appended its JavaScript detection script; page bytes otherwise identical'
    else:
     assert name=='/company/data/index.html' and pretty_url_changes_only(expected,body),('body mismatch',name)
     transformation='Netlify Pretty URLs changed only same-domain .html links and opening anchor tag quotes'
   assert h.get('x-content-type-options')=='nosniff',name
   if name.endswith('.html'):assert h.get('x-frame-options','').upper()=='SAMEORIGIN',name
   return {'path':name,'status':status,'sha256':hashlib.sha256(body).hexdigest(),'transformation':transformation}
  except (OSError,AssertionError,subprocess.CalledProcessError):
   if attempt==2:raise
   time.sleep(.5)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 verified=list(pool.map(verify_file,package['files']))
route_origin='https://forflow.ai' if mode=='production' else origin
routes=[]
for path,expected in [('/company/data',200),('/company/data/',200),('/company/data/index.html',200),('/company',200),('/company/',200),('/product/one/',200),('/product/one/ai-governance',200),('/',302),('/cases.html',302),('/company-other',302),('/assets/site/home-workspace.js',302),('/api/gate-login',405),('/api/leads',302),('/api/events',302),('/api/assessments',302),('/q/company-check-nonexistent',404)]:
 status,h,body=fetch(route_origin,path,follow=expected==200)
 assert status==expected,(path,status)
 if expected==302:assert '/landing.html?next=' in h.get('location',''),path
 if path in ('/company', '/company/') and expected==200:
  assert b'home-workspace.js?v=20261014-lean' in body,path
  assert b'/company/assets/' in body,path
  assert b'forflow.ai/company' in body,path
  assert b'Customer logos' not in body and b'reference-logo-wall' not in body,path
 routes.append({'path':path,'status':status})
custom=[]
if mode=='production':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  unique_origin=origin
  origin=route_origin
  custom=list(pool.map(verify_file,package['files']))
  origin=unique_origin
result={'passed':True,'deploy_id':d['id'],'url':route_origin,'payload_sha256':hashlib.sha256((W/'payload.json').read_bytes()).hexdigest(),'verified_files':verified,'routes':routes,'custom_domain_files':custom,'checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
(W/(mode+'-qa.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':True,'id':d['id'],'files':len(verified),'routes':len(routes),'url':route_origin}),flush=True)
