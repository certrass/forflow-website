import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';

export function createCapabilityScene(host) {
  const scene = new THREE.Scene();
  const renderer = new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power',preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.VSMShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = .82;
  renderer.setClearColor(0xffffff, 0);
  renderer.domElement.setAttribute('aria-hidden','true');
  host.appendChild(renderer.domElement);

  const environment = new RoomEnvironment();
  const pmrem = new THREE.PMREMGenerator(renderer);
  const env = pmrem.fromScene(environment, .04);
  scene.environment = env.texture;
  scene.environmentIntensity = .5;
  environment.dispose();
  const camera = new THREE.OrthographicCamera(-4,4,4,-4,.1,60);
  camera.position.set(7,6.3,9);
  camera.lookAt(0,1.35,0);
  scene.add(new THREE.HemisphereLight(0xffffff,0xbac5d8,1.1));
  const key = new THREE.DirectionalLight(0xffffff,2.2);
  key.position.set(-3,9,6);key.castShadow=true;
  key.shadow.mapSize.set(1024,1024);
  key.shadow.camera.left=-7;key.shadow.camera.right=7;key.shadow.camera.top=7;key.shadow.camera.bottom=-7;
  key.shadow.normalBias=.03;key.shadow.bias=-.0004;
  key.shadow.radius=5;key.shadow.blurSamples=8;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xe8f2ff,.8);rim.position.set(4,4,-5);scene.add(rim);

  const group = new THREE.Group(); scene.add(group);
  const levels = [new THREE.Group(),new THREE.Group(),new THREE.Group()];
  levels.forEach((level,i)=>{level.position.y=[0,1.4,2.85][i];group.add(level);});
  const tracked = [];
  const material = (color,extra={}) => new THREE.MeshPhysicalMaterial({color,roughness:.3,metalness:.08,...extra});
  const ceramic = material(0xffffff,{roughness:.24,clearcoat:.4});
  const pale = material(0xe8ebef,{roughness:.43});
  const blue = material(0x3267d1,{roughness:.22,metalness:.2,clearcoat:.7});
  const blueInset = material(0x357ae5,{roughness:.21,clearcoat:.8});
  function box(parent,w,h,d,x,y,z,mat,radius=.08) {
    const mesh = new THREE.Mesh(new RoundedBoxGeometry(w,h,d,4,Math.min(radius,h*.43)),mat);
    mesh.position.set(x,y,z);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;
  }
  box(levels[0],4.65,.22,3.4,0,0,0,pale,.1);
  const glassMiddle = material(0xbcd5fb,{transmission:.5,thickness:.15,roughness:.17,metalness:0,transparent:true,opacity:.92});
  const glassTop = material(0xe3f0f2,{transmission:.55,thickness:.12,roughness:.14,metalness:.03,transparent:true,opacity:.9});
  box(levels[1],4.55,.075,3.25,0,0,0,glassMiddle,.025).castShadow=false;
  box(levels[2],4.2,.075,3.1,0,0,0,glassTop,.025).castShadow=false;
  // Fine edge profiles give the two glass plates a legible thickness.
  for (const [i,w,d] of [[1,4.55,3.25],[2,4.2,3.1]]) {
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(w,.07,d)),new THREE.LineBasicMaterial({color:i===1?0x99b9ed:0x8fb2bd,transparent:true,opacity:.55}));
    levels[i].add(edges);
  }
  function label(parent,text,x,y,z,w,d,color='#486da6') {
    const canvas = document.createElement('canvas');canvas.width=512;canvas.height=200;
    const ctx=canvas.getContext('2d');ctx.clearRect(0,0,512,200);
    ctx.fillStyle=color;ctx.font=`500 ${text.length>2?95:140}px "PingFang SC", "Microsoft YaHei", sans-serif`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,256,100);
    const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;
    const mesh=new THREE.Mesh(new THREE.PlaneGeometry(w,d),new THREE.MeshBasicMaterial({map:texture,transparent:true,depthWrite:false}));
    mesh.rotation.x=-Math.PI/2;mesh.position.set(x,y,z);parent.add(mesh);
  }
  ['合同','数据','图纸','知识','规则','判断'].forEach((name,i)=>{
    const x=(i%3-1)*1.28,z=(Math.floor(i/3)-.5)*1.27;
    box(levels[0],1.05,.17,.96,x,.23,z,ceramic);
    label(levels[0],name,x,.321,z,.8,.38);
  });
  ['关联依据','分析判断','复核交接'].forEach((name,i)=>{
    const x=(i-1)*1.37;
    const tile=box(levels[1],1.15,.27,.71,x,.19,.05,blue.clone());tracked.push({mesh:tile,level:1});
    label(levels[1],name,x,.328,.05,.99,.31,'#ffffff');
  });
  const routes = [];
  const lineMat = material(0x4c7cd4,{roughness:.4});
  for (let i=0;i<2;i++) {
    const from=(i-1)*1.37,to=i*1.37;
    const path = new THREE.CatmullRomCurve3([new THREE.Vector3(from,.08,-.38),new THREE.Vector3(from,.08,-.91),new THREE.Vector3((from+to)/2,.08,-.97),new THREE.Vector3(to,.08,-.91),new THREE.Vector3(to,.08,-.38)],false,'catmullrom',.1);
    levels[1].add(new THREE.Mesh(new THREE.TubeGeometry(path,40,.015,6,false),lineMat));
    const dot=new THREE.Mesh(new THREE.SphereGeometry(.035,12,8),new THREE.MeshBasicMaterial({color:0x2362d5}));levels[1].add(dot);routes.push({path,dot});
  }
  ['知识','规则','流程','评估'].forEach((name,i)=>{
    const x=(i%2-.5)*1.83,z=(Math.floor(i/2)-.5)*1.25;
    box(levels[2],1.56,.27,1.07,x,.18,z,ceramic);
    const inset=box(levels[2],1.13,.023,.42,x,.328,z-.17,blueInset.clone(),.01);tracked.push({mesh:inset,level:2});
    label(levels[2],name,x,.33,z+.28,.79,.26,'#4c5e75');
  });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.ShadowMaterial({opacity:.06}));
  floor.rotation.x=-Math.PI/2;floor.position.y=-.14;floor.receiveShadow=true;scene.add(floor);

  let active=1, rotating=false, visible=false, dead=false, frame=0, last=0, rotation=0;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  function resize(){
    const w=host.clientWidth,h=host.clientHeight,aspect=w/h;
    const halfH=Math.max(3.5,3.4/aspect);
    camera.left=-halfH*aspect;camera.right=halfH*aspect;camera.top=halfH;camera.bottom=-halfH;
    camera.updateProjectionMatrix();renderer.setSize(w,h,false);render(0);
  }
  function render(time){
    levels.forEach((level,i)=>{const target=[0,1.4,2.85][i]+(active===i?.10:0);level.position.y += (target-level.position.y)*.15;});
    if(rotating && !reduced.matches) rotation += .003;
    group.rotation.y=rotation;
    tracked.forEach(({mesh,level})=>mesh.material.color.setHex(level===active?0x2864d3:level===1?0x497aca:0x5787df));
    routes.forEach(({path,dot},i)=>dot.position.copy(path.getPoint((((reduced.matches?0:time)*.00022+i*.45)%1))));
    renderer.render(scene,camera);
  }
  function tick(time){
    if(dead)return;
    if(visible && !document.hidden && time-last>33){render(time);last=time;}
    frame=requestAnimationFrame(tick);
  }
  const resizeObserver=new ResizeObserver(resize);resizeObserver.observe(host);
  const intersection=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;},{threshold:0});intersection.observe(host);
  resize();frame=requestAnimationFrame(tick);
  return {
    setLayer(i){active=i;render(0);},
    setRotating(value){rotating=value;},
    reset(){rotation=0;render(0);},
    dispose(){dead=true;cancelAnimationFrame(frame);resizeObserver.disconnect();intersection.disconnect();scene.traverse(object=>{object.geometry?.dispose();const mats=Array.isArray(object.material)?object.material:[object.material];mats.filter(Boolean).forEach(mat=>{mat.map?.dispose();mat.dispose();});});env.dispose();pmrem.dispose();renderer.dispose();renderer.domElement.remove();}
  };
}
