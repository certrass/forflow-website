// Exact visual modules captured from AfterQuery on 2026-10-26.
window.afterqueryVisualFactories={13987:t=>{"use strict";var e=t.i(43476),a=t.i(71645);let o=`#version 300 es
layout(location = 0) in vec2 a_pos;
out vec2 v_uv;
void main() {
  v_uv = a_pos * 0.5 + 0.5;
  gl_Position = vec4(a_pos, 0.0, 1.0);
}`,i=`
float hash(float n) { return fract(sin(n * 127.1) * 43758.5453); }
float hash2(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

// Simplex 2D (Ashima Arts, MIT)
vec3 permute(vec3 x) { return mod(((x * 34.0) + 1.0) * x, 289.0); }
float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
  vec2 i = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.0);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);
  m = m * m; m = m * m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);
  vec3 g;
  g.x = a0.x * x0.x + h.x * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}

// Liquid flow: two noise layers drifting slowly and warping each other.
vec2 flow(vec2 uv) {
  float t = u_time * u_flowSpeed;
  vec2 p = uv * vec2(u_resolution.x / u_resolution.y, 1.0) * u_flowScale;
  vec2 q = vec2(snoise(p + vec2(0.0, t)), snoise(p + vec2(5.2, -t * 0.8)));
  vec2 r = vec2(snoise(p + q * 1.2 + vec2(1.7, 9.2) + t * 0.6), snoise(p + q * 1.2 + vec2(8.3, 2.8) - t * 0.5));
  return r * u_flow;
}

// Blobs, measured on the short side so they keep their size on a phone.
float blobs(vec2 uv) {
  float t = u_time * u_blobSpeed;
  vec2 p = (uv + flow(uv)) * u_resolution / min(u_resolution.x, u_resolution.y) * u_blobScale;
  float n = snoise(p + vec2(t, -t * 0.7)) * 0.65 + snoise(p * 2.3 + vec2(-t * 1.3, t + 3.1)) * 0.35;
  return n * 0.5 + 0.5;
}`,n=t=>[1,3,5].map(e=>parseInt(t.slice(e,e+2),16)/255);function l(t,e){let a=(e,a)=>{let o=t.createShader(e);if(t.shaderSource(o,a),t.compileShader(o),!t.getShaderParameter(o,t.COMPILE_STATUS))throw Error(t.getShaderInfoLog(o)??"shader");return o},i=t.createProgram();if(t.attachShader(i,a(t.VERTEX_SHADER,o)),t.attachShader(i,a(t.FRAGMENT_SHADER,e)),t.linkProgram(i),!t.getProgramParameter(i,t.LINK_STATUS))throw Error(t.getProgramInfoLog(i)??"link");let n={},l=t.getProgramParameter(i,t.ACTIVE_UNIFORMS);for(let e=0;e<l;e++){let a=t.getActiveUniform(i,e);n[a.name.replace(/\[0\]$/,"")]={loc:t.getUniformLocation(i,a.name),type:a.type}}return{program:i,run(e,a,o,l){t.bindFramebuffer(t.FRAMEBUFFER,a),t.viewport(0,0,o,l),t.useProgram(i);let r=0;for(let[a,o]of Object.entries(e)){let e=n[a];e&&(e.type===t.SAMPLER_2D?(t.activeTexture(t.TEXTURE0+r),t.bindTexture(t.TEXTURE_2D,o),t.uniform1i(e.loc,r++)):"number"==typeof o?t.uniform1f(e.loc,o):Array.isArray(o)&&(e.type===t.FLOAT_VEC4?t.uniform4fv(e.loc,o):e.type===t.FLOAT_VEC3?t.uniform3fv(e.loc,o):e.type===t.FLOAT_VEC2&&t.uniform2fv(e.loc,o)))}t.drawArrays(t.TRIANGLE_STRIP,0,4)}}}function r(t,e){let a=t.getBoundingClientRect(),o=[],i=[];for(let t of document.querySelectorAll("[data-logo-tint]")){let[n,l,r,u]=(t.dataset.logoTint??"").split(",").map(Number),h=t.getBoundingClientRect();if(h.width&&u>0&&(o.push(((h.left+h.right)/2-a.left)*e,((h.top+h.bottom)/2-a.top)*e,4*Math.max(h.width,h.height)*e,u),i.push(n/255,l/255,r/255),32===o.length))break}let n=o.length/4;for(;o.length<32;)o.push(0);for(;i.length<24;)i.push(0);return{spots:o,cols:i,count:n}}let u={ink:[246/255,245/255,238/255],cell:16,cellAspect:1.25,maxWidth:.82,tints:[],tintStrength:0,tintFill:0,hairDim:.35,coverageGamma:1,grain:.036,blobScale:1.4,blobCover:.45,blobSoft:.22,blobMin:.01,blobMax:.42,blobSpeed:.07,blobBreak:.35,blobBasis:0,seed:0,flow:.006,flowSpeed:.095,flowScale:1.85,textLine:.4,textStrength:.55,textPad:14,textFade:.65,textSoft:110,textRadius:48,bandStrength:1,navLine:.6,navPad:10,navSoft:50,maxPixelRatio:3},h=t=>t-Math.floor(t),s=t=>t-289*Math.floor(t/289),f=t=>s((34*t+1)*t),c=t=>h(43758.5453*Math.sin(127.1*t)),m=(t,e)=>h(43758.5453*Math.sin(12.9898*t+78.233*e)),d=(t,e,a)=>{let o=Math.min(1,Math.max(0,(a-t)/(e-t)));return o*o*(3-2*o)};function M(t,e){let a=Math.floor(t+(t+e)*.366025403784439),o=Math.floor(e+(t+e)*.366025403784439),i=t-a+(a+o)*.211324865405187,n=e-o+(a+o)*.211324865405187,l=+(i>n),r=i>n?0:1,u=i+.211324865405187-l,c=n+.211324865405187-r,m=i+-.577350269189626,d=n+-.577350269189626;a=s(a);let M=f(f(o=s(o))+a),p=f(f(o+r)+a+l),b=f(f(o+1)+a+1),x=Math.max(.5-(i*i+n*n),0),g=Math.max(.5-(u*u+c*c),0),_=Math.max(.5-(m*m+d*d),0);x*=x,x*=x,g*=g,g*=g,_*=_,_*=_;let v=(t,e,a,o)=>{let i=2*h(.024390243902439*t)-1,n=Math.abs(i)-.5,l=i-Math.floor(i+.5);return e*(1.79284291400159-.85373472095314*(l*l+n*n))*(l*a+n*o)};return 130*(v(M,x,i,n)+v(p,g,u,c)+v(b,_,m,d))}let p={rects:Array(64).fill(0),count:0},b="#55534d",x=`repeating-linear-gradient(to right, transparent 0 ${7.5}px, rgb(85 83 77 / 0.13) ${7.5}px ${8.5}px, transparent ${8.5}px 16px)`,g=`
uniform vec2  u_resolution;
uniform float u_dpr;
uniform float u_time;
uniform float u_cell;
uniform float u_cellAspect;
uniform float u_squares;
uniform float u_horizontal; // 1 = lines run across, rows instead of columns
uniform float u_spill; // canvas px the field hangs below the hero
uniform float u_rise; // canvas px at the top where vertical lines stop at uneven heights
uniform float u_curtainMin;
uniform float u_curtainSpeed;
uniform float u_flow;
uniform float u_flowSpeed;
uniform float u_flowScale;
uniform float u_blobScale;
uniform float u_blobSpeed;
uniform float u_fill; // < 0 = off
`,_=`#version 300 es
precision highp float;
${g}
uniform vec3  u_ink;
uniform vec3  u_ink2;
uniform float u_blobZoom; // < 1 draws the blobs larger than the canvas's short side would
uniform vec4  u_quiet[16];
uniform vec4  u_logo[8];
uniform vec3  u_logoCol[8];
uniform float u_logoCount;
uniform vec3  u_sweep[6];
uniform float u_sweepCount;
uniform float u_quietCount;
uniform float u_quietPad;
uniform float u_quietSoft;
uniform float u_quietMax;
uniform float u_maxWidth;
uniform float u_blobCover;
uniform float u_blobSoft;
uniform float u_blobMin;
uniform float u_blobMax;
uniform float u_blobBreak;

${i}

layout(location = 0) out vec4 outLine;
layout(location = 1) out vec4 outColour;

void main() {
  float cell = u_cell * u_dpr;
  // The grid is built in a frame where lines always run along y; horizontal
  // lines swap x and y going in and out.
  bool horiz = u_horizontal > 0.5;
  // Squares: square cells, so each mark is a square rather than a line segment.
  vec2 size = vec2(cell, cell * mix(u_cellAspect, 1.0, u_squares));
  vec2 id = floor(gl_FragCoord.xy);
  vec2 centerSp = (id + 0.5) * size;
  vec2 centerUV = (horiz ? centerSp.yx : centerSp) / u_resolution;

  float thr = mix(0.85, 0.3, u_blobCover);
  float blob = smoothstep(thr, thr + u_blobSoft, blobs(centerUV * u_blobZoom));
  float m = blob * (1.0 - u_blobBreak * hash2(id + 0.37));
  float w = mix(u_blobMin, u_blobMax, clamp(m, 0.0, 1.0));
  // Two-ink mode: a blob's rim (cells partway into it, not the hairline field
  // outside it or its heavy core) takes u_ink2, as the site's own screens edge
  // their blobs in a page's colour (HalftoneFrame's tints).
  float rim = smoothstep(0.02, 0.22, blob) * (1.0 - smoothstep(0.4, 0.85, blob));
  vec3 inkCol = mix(u_ink, u_ink2, rim);
  // Lines near a logo take its colour, full over the inner half of its reach and
  // fading out over the rest: blobs fully, hairlines mostly, so around a logo
  // its colour, not the grey, is what reads.
  if (u_logoCount > 0.0) {
    vec2 qLogo = vec2(centerUV.x, 1.0 - centerUV.y) * u_resolution;
    float near = 0.0;
    vec3 logoCol = u_ink;
    for (int i = 0; i < 8; i++) {
      if (float(i) >= u_logoCount) break;
      vec4 L = u_logo[i];
      float wgt = (1.0 - smoothstep(L.z * 0.45, L.z, distance(qLogo, L.xy))) * L.w;
      if (wgt > near) {
        near = wgt;
        logoCol = u_logoCol[i];
      }
    }
    inkCol = mix(inkCol, logoCol, mix(0.75, 1.0, smoothstep(0.02, 0.22, blob)) * near);
  }

  // Filling in from the left with u_fill (a form's progress): past its edge
  // the bars stay in the plain ink. Filled bars take a colour of the sweep at
  // full strength, one per region across the field, the boundaries dithered a
  // column or so, so the colours meet as the screen's own grain.
  float filled = u_fill < 0.0 ? 1.0 : 1.0 - smoothstep(u_fill * 1.1 - 0.08, u_fill * 1.1, centerUV.x);
  if (u_sweepCount > 0.0) {
    float region = clamp(centerUV.x, 0.0, 0.9999) * u_sweepCount + (hash(id.x * 5.31) - 0.5) * 0.45;
    vec3 sweepCol = u_sweep[0];
    for (int i = 1; i < 6; i++) {
      if (float(i) >= u_sweepCount) break;
      if (region >= float(i)) sweepCol = u_sweep[i];
    }
    inkCol = mix(inkCol, sweepCol, filled);
    // Filled bars keep their colour at every weight: never thinner than a slim
    // bar, so a filled column reads in colour even between the blobs.
    w = mix(w, max(w, 0.14), filled);
  }

  // Always leave a visible gap between lines.
  float minGapPx = 1.5 * u_dpr;
  w = min(w, min(u_maxWidth, 1.0 - minGapPx / cell));

  // Behind text, hairlines only, in a shape that never reads as a box: the
  // text rects melt into one rounded outline (smooth union, corners rounded
  // by the pad), its edge wanders with slow noise, and every line segment
  // ends at its own jittered point, so the lines thin out raggedly, the way
  // the blobs themselves end.
  if (u_quietCount > 0.0) {
    vec2 q0 = vec2(centerUV.x, 1.0 - centerUV.y) * u_resolution;
    float sd = 1e5;
    float k = u_quietPad * 1.5; // how far neighbouring rects merge
    for (int i = 0; i < 16; i++) {
      if (float(i) >= u_quietCount) break;
      vec4 r = u_quiet[i];
      vec2 q = abs(q0 - (r.xy + r.zw) * 0.5) - (r.zw - r.xy) * 0.5;
      float d = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - u_quietPad;
      float h = clamp(0.5 + 0.5 * (d - sd) / k, 0.0, 1.0);
      sd = mix(d, sd, h) - k * h * (1.0 - h);
    }
    float soft = max(u_quietSoft, 1.0);
    float wander = snoise(q0 / (soft * 3.0) + vec2(3.1, u_time * 0.04)) * soft * 0.6;
    float jag = (hash2(id + 5.3) - 0.5) * cell * 1.6;
    float quiet = 1.0 - smoothstep(0.0, soft, sd + wander + jag);
    w = mix(w, min(w, u_quietMax), quiet);
  }

  // Each column's drip below the hero and reach at the top: its own slowly
  // drifting length, as a share of the spill (rise); SCREEN cuts each pixel by it.
  float drip = 1.0;
  float climbLen = 1.0;
  if (!horiz) {
    float drape = 0.5 + 0.5 * snoise(vec2(id.x * 0.08, u_time * u_curtainSpeed));
    float fray = mix(0.45, 1.0, hash(id.x * 1.31 + 4.7));
    drip = mix(u_curtainMin, 1.0, drape * fray);
    float drapeTop = 0.5 + 0.5 * snoise(vec2(id.x * 0.08 + 17.0, u_time * u_curtainSpeed));
    float frayTop = mix(0.3, 1.0, hash(id.x * 2.17 + 9.1));
    climbLen = mix(u_curtainMin, 1.0, drapeTop * frayTop);
  }

  w = clamp(w, 0.0, 1.0);
  outLine = vec4(floor(w * 255.0) / 255.0, fract(w * 255.0), drip, climbLen);
  outColour = vec4(clamp(inkCol, 0.0, 1.0), filled);
}`,v=`#version 300 es
precision highp float;
${g}
uniform highp sampler2D u_cellLine;
uniform highp sampler2D u_cellColour;
uniform float u_cutoff;
uniform float u_cutoffSoft;
uniform float u_hairDim;
uniform float u_grain;

${i}

in vec2 v_uv;
out vec4 outColor;

void main() {
  vec2 px = v_uv * u_resolution;
  float cell = u_cell * u_dpr;
  bool horiz = u_horizontal > 0.5;
  vec2 sp = horiz ? px.yx : px;
  vec2 size = vec2(cell, cell * mix(u_cellAspect, 1.0, u_squares));
  vec2 c = sp / size;
  ivec2 id = clamp(ivec2(floor(c)), ivec2(0), textureSize(u_cellLine, 0) - 1);
  vec2 f = fract(c);
  vec4 line = texelFetch(u_cellLine, id, 0);
  vec4 colour = texelFetch(u_cellColour, id, 0);
  float w = line.r + line.g / 255.0;

  // Below the hero, vertical lines (and squares) drip: each line hangs its own
  // slowly drifting length and thins toward its tip, so the hero melts into
  // the next section instead of ending on a straight edge.
  float depth = u_spill - px.y; // canvas px past the hero's foot (px.y runs bottom-up)
  if (depth > 0.0 && !horiz) {
    float k = depth / max(u_spill * line.b, 1.0);
    w *= (1.0 - k * 0.7) * step(k, 1.0);
  }

  // The same at the top with \`rise\`: each line reaches up its own drifting
  // length, full weight up to its tip, so the field ends on a ragged edge.
  // Applied to the ink, since a zero-width line still draws as a hairline.
  float reach = 1.0;
  float climb = px.y - (u_resolution.y - u_rise);
  if (climb > 0.0 && !horiz) reach = step(climb, u_rise * line.a);

  float aa = 1.0 / cell;
  float half_ = w * 0.5;
  float ink = smoothstep(0.5 - half_ - aa, 0.5 - half_ + aa, f.x)
            * (1.0 - smoothstep(0.5 + half_ - aa, 0.5 + half_ + aa, f.x));
  // Squares: the same width across y too, so the line segment closes into a square.
  ink *= mix(1.0, smoothstep(0.5 - half_ - aa, 0.5 - half_ + aa, f.y)
                  * (1.0 - smoothstep(0.5 + half_ - aa, 0.5 + half_ + aa, f.y)), u_squares);
  // Under 1 px antialiasing can't make a line thinner, so it dims instead (Option 7).
  ink *= mix(u_hairDim, 1.0, clamp(w * cell, 0.0, 1.0));
  // With a cutoff, anything thinner is dropped, so the blobs float on bare ground.
  float widthPx = w * cell / u_dpr;
  if (u_cutoff > 0.0) ink *= smoothstep(u_cutoff, u_cutoff + u_cutoffSoft, widthPx);
  ink *= reach;

  // Below the hero, horizontal lines fade out slowly instead, each row over
  // its own length, wavering along the row.
  if (depth > 0.0 && horiz) {
    float rowDepth = u_spill - (float(id.x) + 0.5) * size.x;
    float drift = 0.5 + 0.5 * snoise(vec2(px.x / (cell * 30.0), float(id.x) * 0.37 + u_time * u_curtainSpeed));
    float len = u_spill * mix(u_curtainMin + 0.25, 1.0, drift);
    ink *= 1.0 - smoothstep(0.0, len, rowDepth);
  }

  // With a fill, nothing shows past its edge: only the filled, coloured side.
  if (u_fill >= 0.0) ink *= colour.a;

  // Transparent ground: the lines alone, so the field can hang over the next section.
  vec3 col = colour.rgb + (hash2(px + fract(u_time) * 100.0) - 0.5) * u_grain;
  outColor = vec4(clamp(col, 0.0, 1.0) * ink, ink);
}`;t.s(["HalftoneField",0,function({className:t,ink:o,ink2:i,screen:h="lines",direction:s="vertical",spill:f=0,rise:g=0,blobSize:w=0,cover:y,colors:R,fill:S,quiet:C=!0}){let E=(0,a.useRef)(null),T=R?.join(",")??"",A=(0,a.useRef)({ink:o,ink2:i,screen:h,direction:s});return(0,a.useEffect)(()=>{A.current={ink:o,ink2:i,screen:h,direction:s}},[o,i,h,s]),(0,a.useEffect)(()=>{let t,e,a,o=E.current,i=o?.parentElement?.parentElement;if(!o||!i)return;let h=o.getContext("webgl2",{antialias:!1,premultipliedAlpha:!0});if(!h){if(S)return;return function({canvas:t,frame:e,settings:a,underBar:o=!1}){let i=t.getContext("2d");if(!i)return()=>{};let n={...u,...a},l=n.tints.slice(0,16),r=window.matchMedia("(prefers-reduced-motion: reduce)").matches,h=t=>t.map(t=>Math.round(255*Math.min(1,Math.max(0,t)))),s=h(n.ink),f=l.map(h),p=1,b=0;function x(){b=((t.getBoundingClientRect().left+window.scrollX)%n.cell+n.cell)%n.cell*p,T()}function g(){let e=t.getBoundingClientRect();p=Math.min(n.maxPixelRatio,window.devicePixelRatio||1),t.width=Math.max(1,Math.round(e.width*p)),t.height=Math.max(1,Math.round(e.height*p)),x()}let _=[],v=document.createRange(),w=performance.now(),y=0,R=-1/0,S=!0,C=!1;function E(a){y=0,(a-R>=1e3/30||!C)&&(R=a,function(a){let u=t.width,h=t.height,x=r?0:a,g=r?0:n.flow,w=e.getBoundingClientRect();for(let t of(_.length=0,e.querySelectorAll("[data-halftone-quiet]"))){for(let e of t.childElementCount?[t.getBoundingClientRect()]:(v.selectNodeContents(t),v.getClientRects())){if(12===_.length)break;!e.width||e.right<w.left||e.left>w.right||e.bottom<w.top||e.top>w.bottom||_.push({x0:(e.left-w.left)*p,y0:(e.top-w.top)*p,x1:(e.right-w.left)*p,y1:(e.bottom-w.top)*p,strength:"strong"===t.getAttribute("data-halftone-quiet")?n.bandStrength:n.textStrength})}}let y=function(){let t=o&&document.querySelector("header");if(!t)return 0;let a=t.getBoundingClientRect().bottom-e.getBoundingClientRect().top;return a>0?a+n.navPad:0}()*p,R=n.cell*p,S=R*n.cellAspect,C=Math.max(1,Math.ceil((u+b)/R)),E=Math.max(1,Math.ceil(h/S)),T=n.blobBasis?n.blobBasis*p:Math.min(u,h),A=17.31*n.seed,k=-9.17*n.seed,q=.85+-.55*n.blobCover,P=Math.min(n.maxWidth,1-1.5*p/R),F=n.navLine/n.cell,L=n.textLine/n.cell,z=n.textPad*p,B=n.textSoft*p,U=n.textRadius*p,I=n.navSoft*p,D=u/h,O=x*n.flowSpeed,N=x*n.blobSpeed,X=u/5,j=(t,e)=>1-d(0,Math.max(e,1),t);i.clearRect(0,0,u,h);for(let t=0;t<E;t++){let e=(t+.5)*S,a=e/h,o=(1-a)*h;for(let r=0;r<C;r++){let p=(r+.5)*R-b,x=p/u,v=x*D*n.flowScale,w=a*n.flowScale,C=M(v,w+O),E=M(v+5.2,w-.8*O),V=M(v+1.2*C+1.7+.6*O,w+1.2*E+9.2+.6*O),$=M(v+1.2*C+8.3-.5*O,w+1.2*E+2.8-.5*O),G=u/T*(x+V*g)*n.blobScale+A,W=h/T*(a+$*g)*n.blobScale+k,H=.65*M(G+N,W-.7*N)+.35*M(2.3*G-1.3*N,2.3*W+N+3.1),Y=d(q,q+n.blobSoft,.5*H+.5),K=Y*(1-n.blobBreak*m(r+.37,t+.37)),Z=n.blobMin+(n.blobMax-n.blobMin)*Math.min(1,Math.max(0,K));Z=Math.min(Z,P),y>0&&(Z+=(Math.min(Z,F)-Z)*j(o-y,I));let J=0;for(let t of _){let e=(t.x1-t.x0)*.5+z,a=(t.y1-t.y0)*.5+z,i=Math.min(U,Math.min(e,a)),n=Math.abs(p-(t.x0+t.x1)*.5)-e+i,l=Math.abs(o-(t.y0+t.y1)*.5)-a+i,r=j(Math.hypot(Math.max(n,0),Math.max(l,0))+Math.min(Math.max(n,l),0)-i,B)*t.strength;Z+=(Math.min(Z,L)-Z)*r,J=Math.max(J,r)}Z=Math.min(1,Math.max(0,Z));let Q=s;if(l.length&&n.tintStrength>0){let t=d(.02,.22,Y)*(1-d(.4,.85,Y)),a=(t+(d(.02,.22,Y)-t)*n.tintFill)*n.tintStrength;if(a>.01){let t=0;if(l.length>1){let a=M(p/X*.6+3.1,e/X*.6+3.1)*X*.35,o=M(p/X*.6+7.7,e/X*.6+7.7)*X*.35;t=((Math.floor((p+a)/X)+5*Math.floor((e+o)/X)+Math.floor(c(.5)*l.length))%l.length+l.length)%l.length}let o=f[t];Q=s.map((t,e)=>Math.round(t+(o[e]-t)*a))}}let tt=Z*R,te=Math.pow(n.hairDim+(1-n.hairDim)*Math.min(1,Math.max(0,tt)),n.coverageGamma)*(1-J*n.textFade);te<=.003||(i.fillStyle=`rgb(${Q[0]} ${Q[1]} ${Q[2]} / ${te.toFixed(3)})`,i.fillRect(p-Math.max(tt,1)/2,h-(t+1)*S,Math.max(tt,1),S))}}}(Math.max(0,(a-w)/1e3)),C||(C=!0,t.dataset.ready="")),r||T()}function T(){y||!S||document.hidden||(y=requestAnimationFrame(E))}let A=new ResizeObserver(()=>{g(),r&&(C=!1),T()});A.observe(t);let k=new IntersectionObserver(([t])=>{S=t.isIntersecting,T()});return k.observe(e),document.addEventListener("visibilitychange",T),window.addEventListener("resize",x),g(),()=>{cancelAnimationFrame(y),A.disconnect(),k.disconnect(),document.removeEventListener("visibilitychange",T),window.removeEventListener("resize",x),delete t.dataset.ready}}({canvas:o,frame:i,underBar:!0,settings:{ink:n(A.current.ink??b),blobSpeed:.11,blobCover:y??.45,blobBasis:w,tints:[],tintStrength:0}})}let s=window.matchMedia("(prefers-reduced-motion: reduce)").matches,x=(a=h.createBuffer(),h.bindBuffer(h.ARRAY_BUFFER,a),h.bufferData(h.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),h.STATIC_DRAW),h.enableVertexAttribArray(0),h.vertexAttribPointer(0,2,h.FLOAT,!1,0,0),a);try{t=l(h,_),e=l(h,v)}catch{return}let R=[h.createTexture(),h.createTexture()];for(let t of R)h.bindTexture(h.TEXTURE_2D,t),h.texParameteri(h.TEXTURE_2D,h.TEXTURE_MIN_FILTER,h.NEAREST),h.texParameteri(h.TEXTURE_2D,h.TEXTURE_MAG_FILTER,h.NEAREST),h.texParameteri(h.TEXTURE_2D,h.TEXTURE_WRAP_S,h.CLAMP_TO_EDGE),h.texParameteri(h.TEXTURE_2D,h.TEXTURE_WRAP_T,h.CLAMP_TO_EDGE);let k=h.createFramebuffer(),q=0,P=0,F=1,L=()=>{F=Math.min(window.devicePixelRatio||1,3);let{width:t,height:e}=o.getBoundingClientRect(),a=Math.max(1,Math.round(t*F)),i=Math.max(1,Math.round(e*F));(o.width!==a||o.height!==i)&&(o.width=a,o.height=i)};L();let z=new ResizeObserver(L);z.observe(o);let B=!0,U=new IntersectionObserver(([t])=>{B=t.isIntersecting});U.observe(o);let I=performance.now(),D=I,O=(T?T.split(","):[]).slice(0,6),N=O.length,X=O.flatMap(t=>n(t));for(;X.length<18;)X.push(0);let j=S?S.current:0,V=0,$=p,G=r(o,F),W=0,H=a=>{var i,l;V=requestAnimationFrame(H);let u=Math.min((a-D)/1e3,.05);if(D=a,!B||document.hidden)return;S&&(j+=(S.current-j)*(1-Math.exp(-u/.35))),W++%2==0&&($=C?function(t,e){let a=t.getBoundingClientRect(),o=[],i=document.querySelector("header");for(let t of[...i?[i]:[],...document.querySelectorAll("[data-halftone-quiet]")]){let i=t.getBoundingClientRect();if(i.width&&(o.push((i.left-a.left)*e,(i.top-a.top)*e,(i.right-a.left)*e,(i.bottom-a.top)*e),64===o.length))break}let n=o.length/4;for(;o.length<64;)o.push(0);return{rects:o,count:n}}(o,F):p,G=r(o,F));let c="horizontal"===A.current.direction,m="squares"===A.current.screen,d=16*F,M=c?o.height:o.width,x=c?o.width:o.height;i=Math.max(1,Math.ceil(M/d)),l=Math.max(1,Math.ceil(x/(d*(m?1:1.25)))),(i!==q||l!==P)&&(q=i,P=l,h.bindFramebuffer(h.FRAMEBUFFER,k),R.forEach((t,e)=>{h.bindTexture(h.TEXTURE_2D,t),h.texImage2D(h.TEXTURE_2D,0,h.RGBA8,q,P,0,h.RGBA,h.UNSIGNED_BYTE,null),h.framebufferTexture2D(h.FRAMEBUFFER,h.COLOR_ATTACHMENT0+e,h.TEXTURE_2D,t,0)}),h.drawBuffers([h.COLOR_ATTACHMENT0,h.COLOR_ATTACHMENT1]),h.bindFramebuffer(h.FRAMEBUFFER,null));let _={u_resolution:[o.width,o.height],u_dpr:F,u_time:s?0:(a-I)/1e3,u_cell:16,u_cellAspect:1.25,u_squares:+!!m,u_horizontal:+!!c,u_ink:n(A.current.ink??b),u_ink2:n(A.current.ink2??A.current.ink??b),u_spill:f*F,u_rise:g*F,u_blobZoom:w>0?Math.min(o.width,o.height)/(w*F):1,u_curtainMin:.15,u_curtainSpeed:.03,u_flow:.006*!s,u_flowSpeed:.095,u_flowScale:1.85,u_quiet:$.rects,u_quietCount:$.count,u_logo:G.spots,u_logoCol:G.cols,u_logoCount:G.count,u_sweep:X,u_sweepCount:N,u_fill:S?j:-1,u_quietPad:28*F,u_quietSoft:90*F,u_quietMax:Math.min(.025,.01),u_cutoff:2.4*!!m,u_hairDim:.35,u_cutoffSoft:1.2,u_grain:.036,u_maxWidth:.82,u_blobScale:1.4,u_blobCover:y??.45,u_blobSoft:.22,u_blobMin:.01,u_blobMax:.42,u_blobSpeed:.11,u_blobBreak:.35};t.run(_,k,q,P),e.run({..._,u_cellLine:R[0],u_cellColour:R[1]},null,o.width,o.height),o.dataset.ready=""};return V=requestAnimationFrame(H),()=>{cancelAnimationFrame(V),z.disconnect(),U.disconnect(),h.deleteProgram(t.program),h.deleteProgram(e.program),R.forEach(t=>h.deleteTexture(t)),h.deleteFramebuffer(k),h.deleteBuffer(x),delete o.dataset.ready}},[f,g,w,y,T,C]),(0,e.jsxs)("div",{"aria-hidden":!0,className:t,children:[(0,e.jsx)("canvas",{ref:E,className:"peer block h-full w-full opacity-0 transition-opacity duration-300 ease-out data-ready:opacity-100"}),"lines"===h&&"vertical"===s&&(0,e.jsx)("div",{className:"pointer-events-none absolute inset-x-0 top-0 transition-opacity duration-300 ease-out peer-data-ready:opacity-0",style:{bottom:f,backgroundImage:x}})]})}],13987)},54648:e=>{"use strict";var t=e.i(43476),r=e.i(71645),n=e.i(74080);let i=["slack","google-drive","salesforce","microsoft-teams","hubspot","gmail","jira","notion","outlook","github","asana","google-calendar","confluence","trello","sharepoint"].map(e=>`./assets/tools/${e}.webp`);function a(e,t){let r=43758.5453*Math.sin(127.1*e+311.7*t);return r-Math.floor(r)}function s(e,t){let r=Math.floor(e),n=Math.floor(t),i=e-r,s=t-n,l=i*i*(3-2*i),o=s*s*(3-2*s),d=a(r,n),c=a(r+1,n),u=a(r,n+1);return d+(c-d)*l+(u-d)*o+(d-c-u+a(r+1,n+1))*l*o}let l=e=>e*e*(3-2*e),o=e=>Math.min(1,Math.max(0,e)),d=(e,t,r)=>l(o((r-e)/(t-e)));function c(e,t,r,n,i,a){let s=0;i[0]=0,a[0]=-1/0,a[1]=1/0;for(let r=1;r<t;r++){let t=(e[r]+r*r-(e[i[s]]+i[s]*i[s]))/(2*r-2*i[s]);for(;t<=a[s];)s--,t=(e[r]+r*r-(e[i[s]]+i[s]*i[s]))/(2*r-2*i[s]);i[++s]=r,a[s]=t,a[s+1]=1/0}s=0;for(let l=0;l<t;l++){for(;a[s+1]<l;)s++;r[l]=(l-i[s])**2+e[i[s]],n[l]=i[s]}}function u(e,t,r){let n=Math.max(t,r),i=new Float64Array(n),a=new Float64Array(n),s=new Int32Array(n),l=new Int32Array(n),o=new Float64Array(n+1),d=new Float64Array(t*r),u=new Int32Array(t*r);for(let n=0;n<t;n++){for(let a=0;a<r;a++)i[a]=1e20*!e[a*t+n];c(i,r,a,s,l,o);for(let e=0;e<r;e++)d[e*t+n]=a[e],u[e*t+n]=s[e]}let f=new Float32Array(t*r),m=new Int32Array(t*r);for(let e=0;e<r;e++){for(let r=0;r<t;r++)i[r]=d[e*t+r];c(i,t,a,s,l,o);for(let r=0;r<t;r++)f[e*t+r]=Math.sqrt(a[r]),m[e*t+r]=u[e*t+s[r]]*t+s[r]}return{dist:f,near:m}}e.s(["HeroLogos",0,function(){for(let e of i.slice(0,7))(0,n.preload)(e,{as:"image"});let e=(0,r.useRef)(null),a=(0,r.useRef)(null),c=(0,r.useRef)(null);return(0,r.useEffect)(()=>{let t=e.current,r=a.current,n=c.current;if(!t||!r||!n)return;let f=n.getContext("2d");if(!f)return;let m=window.matchMedia("(prefers-reduced-motion: reduce)").matches,h=[],p=!1,g=!1,x=new Map,b=80,y=e=>{let t=`${e}-${b}`,r=x.get(t);return r||(r=function(e,t){let r=e.naturalWidth/e.naturalHeight,n=Math.round(Math.min(t,1.6*t/r)),i=Math.round(n*r),a=i+56,s=n+56,l=document.createElement("canvas");l.width=a,l.height=s;let o=l.getContext("2d",{willReadFrequently:!0});o.drawImage(e,28,28,i,n);let{data:d}=o.getImageData(0,0,a,s),c=new Uint8Array(a*s),f=new Uint8Array(a*s);for(let e=0;e<a*s;e++){let t=Math.min(d[4*e],d[4*e+1],d[4*e+2])>232;c[e]=+(!t&&d[4*e+3]>=128),f[e]=1-c[e]}let m=u(c,a,s),h=u(f,a,s),p=new Float32Array(a*s),g=new Float32Array(a*s),x=new Float32Array(a*s),b=new Float32Array(a*s);for(let e=0;e<a*s;e++){p[e]=c[e]?.5-h.dist[e]:m.dist[e]-.5;let t=(c[e]?e:m.near[e])*4;g[e]=d[t],x[e]=d[t+1],b[e]=d[t+2]}let y={};for(let e=0;e<a*s;e+=3){if(!c[e])continue;let t=d[4*e],r=d[4*e+1],n=d[4*e+2],i=Math.max(t,r,n),a=Math.min(t,r,n),s=i?(i-a)/i:0,l=0;if(i!==a){let e=i-a;l=i===t?((r-n)/e+6)%6:i===r?(n-t)/e+2:(t-r)/e+4}let o=s<.2?-1:Math.floor(2*l),u=.15+s,f=y[o]??={w:0,r:0,g:0,b:0};f.w+=u,f.r+=t*u,f.g+=r*u,f.b+=n*u}let w=Object.values(y).sort((e,t)=>t.w-e.w)[0];return{w:a,h:s,lw:i,lh:n,sdf:p,r:g,g:x,b,tint:w?[w.r/w.w,w.g/w.w,w.b/w.w]:[85,83,77]}}(h[e],b),x.set(t,r)),r},w=0,v=0,j=7,M=null,_=1,k=()=>({w:1.6*b+.11*b*2,h:b+.11*b*2}),C=(e,t)=>{let r=k(),n=e-r.w/2,i=t-r.h/2;return i>=106&&i+r.h<=v-28&&n>=28&&n+r.w<=w-28&&!(M&&n+r.w>M.left-56&&n<M.right+56&&i+r.h>M.top-56&&i<M.bottom+56)},E=[],N=0,R=()=>{let e=N;for(let t=0;t<i.length&&(!h[e]||E.some(t=>t.logo===e||t.next===e));t++)e=(e+1)%i.length;return N=(e+1)%i.length,e},S=e=>{let i;w=t.clientWidth,v=t.clientHeight,_=Math.min(3,window.devicePixelRatio||1),n.width=Math.round(w*_),n.height=Math.round(v*_),n.style.width=`${n.width/_}px`,n.style.height=`${n.height/_}px`,f.setTransform(_,0,0,_,0,0);let a=t.getBoundingClientRect(),s=t.closest("section")?.querySelector("[data-hero-copy]"),l=s?Array.from(s.children).map(e=>e.getBoundingClientRect()):[];M=l.length?{left:Math.min(...l.map(e=>e.left))-a.left,right:Math.max(...l.map(e=>e.right))-a.left,top:Math.min(...l.map(e=>e.top))-a.top,bottom:Math.max(...l.map(e=>e.bottom))-a.top}:null,({count:j,h:b}=(i=w)<768?{count:3,h:56}:i<1100?{count:5,h:72}:{count:7,h:80}),(e=>{E.forEach(e=>e.zone.remove()),E.length=0;let t=k(),n=[];for(let e=106+t.h/2;e<=v-28-t.h/2;e+=12)for(let r=28+t.w/2;r<=w-28-t.w/2;r+=12)C(r,e)&&n.push({x:r,y:e});if(!n.length)return;let i=(e,r)=>Math.hypot((e.x-r.x)/t.w,(e.y-r.y)/t.h),a=(e,r)=>Math.abs(e.x-r.x)>=t.w+40||Math.abs(e.y-r.y)>=t.h+32,s=[n[Math.floor(n.length/2)]];for(;s.length<j;){let e=null,t=-1;for(let r of n){if(!s.every(e=>a(r,e)))continue;let n=Math.min(...s.map(e=>i(r,e)));n>t&&([e,t]=[r,n])}if(!e)break;s.push(e)}for(let e=0;e<12;e++){let e=s.map(()=>({x:0,y:0,n:0}));for(let t of n){let r=0;for(let e=1;e<s.length;e++)i(t,s[e])<i(t,s[r])&&(r=e);e[r].x+=t.x,e[r].y+=t.y,e[r].n++}s.forEach((t,r)=>{if(!e[r].n)return;let l={x:e[r].x/e[r].n,y:e[r].y/e[r].n},o=C(l.x,l.y)?l:n.reduce((e,t)=>i(e,l)<i(t,l)?e:t);s.every((e,t)=>t===r||a(o,e))&&(s[r]=o)})}let l=s.map(e=>{let t=40,r=22;for(;t>1&&![[-1,-1],[1,-1],[-1,1],[1,1],[0,-1],[0,1],[-1,0],[1,0]].every(([n,i])=>C(e.x+n*t,e.y+i*r));)t*=.8,r*=.8;return{rx:t>1?t:0,ry:t>1?r:0}});s.forEach((e,r)=>s.forEach((n,i)=>{if(!(i<=r))for(;l[r].rx+l[i].rx>1&&Math.abs(e.x-n.x)-l[r].rx-l[i].rx<t.w+40&&Math.abs(e.y-n.y)-l[r].ry-l[i].ry<t.h+32;)for(let e of[r,i])l[e].rx*=.8,l[e].ry*=.8})),s.forEach((t,n)=>{let i=document.createElement("div");i.className="absolute",i.dataset.halftoneQuiet="",r.appendChild(i),E.push({hx:t.x,hy:t.y,...l[n],cx:t.x,cy:t.y,born:e+.12*n,logo:R(),next:-1,morphAt:e+1.2+2+9.6*n/s.length,seed:100*Math.random(),zone:i})})})(e)},P=0,O=(e,t,r)=>{let n=t+(e.w-1)/2,i=r+(e.h-1)/2,a=Math.min(e.w-1,Math.max(0,n)),s=Math.min(e.h-1,Math.max(0,i));return P=Math.round(s)*e.w+Math.round(a),e.sdf[P]+Math.hypot(n-a,i-s)},z=0,A=!0,$=0,I=new IntersectionObserver(([e])=>{A=e.isIntersecting});I.observe(t);let q=e=>{if(z=requestAnimationFrame(q),!A||document.hidden||!p)return;let t=(e-$)/1e3;for(let e of(f.clearRect(0,0,w,v),E)){!m&&e.next<0&&t>=e.morphAt&&(e.next=R());let r=0;e.next>=0&&(r=o((t-e.morphAt)/2.6))>=1&&(e.logo=e.next,e.next=-1,e.morphAt=t+7+2*Math.random(),r=0);let n=y(e.logo),i=e.next>=0?y(e.next):null;m||(e.cx=e.hx+(s(.05*t+e.seed,1.3*e.seed)-.5)*2*e.rx,e.cy=e.hy+(s(2.7*e.seed,.05*t*1.2+e.seed)-.5)*2*e.ry);let a=m?1:o((t-e.born)/1.2),c=1.5*a-.25,u=.11*b*(1+1.4*Math.sin(Math.PI*r)),h=i?.08*b*Math.sin(Math.PI*r):0,p=Math.max(n.lw,i?.lw??0)/2+u+h+2,g=Math.max(n.lh,i?.lh??0)/2+u+h+2;for(let a=Math.ceil((e.cx-p)/4);4*a<e.cx+p;a++)for(let l=Math.floor((e.cy-g)/5);5*l<e.cy+g;l++){let o=4*a-e.cx,p=5*l+2.5-e.cy,g=o+(m?0:(s(.02*o+e.seed,.02*p+.3*t)-.5)*2*u),x=p+(m?0:(s(.02*o+e.seed+7.3,.02*p-.27*t)-.5)*1.4*u),b=O(n,g,x),y=P,w=-1,v=0;if(i){let n=O(i,g,x);w=P,v=d(0,1,1.6*r-.3-(s(.06*a+3*e.seed,.05*l+.15*t)-.5)*.6),b+=(n-b)*v-h}let j=d(2,-3.5,b);if(j<.04)continue;let M=m?1:d(-.15,.15,c-s(.09*a+e.seed,.07*l+1.7*e.seed+.12*t));if(M<=.01)continue;let k=Math.max(.5,2.8*j*M*(m?1:.7+.55*s(.14*a+2.1*e.seed,.1*l+.4*t))),C=i?n.r[y]+(i.r[w]-n.r[y])*v:n.r[y],E=i?n.g[y]+(i.g[w]-n.g[y])*v:n.g[y],N=i?n.b[y]+(i.b[w]-n.b[y])*v:n.b[y];f.fillStyle=`rgb(${C} ${E} ${N})`;let R=Math.round((4*a-k/2)*_)/_,S=Math.max(R+1/_,Math.round((4*a+k/2)*_)/_),z=Math.round(5*l*_)/_,A=Math.round((l+1)*5*_)/_;f.fillRect(R,z,S-R,A-z)}let x=l(a),w=(Math.max(n.lw,i?.lw??0)+24)*x,v=(Math.max(n.lh,i?.lh??0)+24)*x;Object.assign(e.zone.style,{left:`${e.cx-w/2}px`,top:`${e.cy-v/2}px`,width:`${w}px`,height:`${v}px`});let j=i?l(r):0,M=n.tint.map((e,t)=>Math.round(e+((i?i.tint[t]:e)-e)*j));e.zone.dataset.logoTint=`${M.join(",")},${x.toFixed(3)}`}m&&E.length&&cancelAnimationFrame(z)},F=0;i.forEach((e,t)=>{let r=new Image,n=()=>{t<7&&7==++F&&!p&&!g&&h.some(Boolean)&&(p=!0,$=performance.now(),S(0),z=requestAnimationFrame(q))};r.onload=()=>{h[t]=r,n()},r.onerror=n,r.src=e});let D=new ResizeObserver(()=>{p&&(t.clientWidth!==w||t.clientHeight!==v)&&S((performance.now()-$)/1e3)});return D.observe(t),()=>{g=!0,cancelAnimationFrame(z),D.disconnect(),I.disconnect(),E.forEach(e=>e.zone.remove())}},[]),(0,t.jsxs)("div",{ref:e,"aria-hidden":!0,className:"pointer-events-none absolute inset-0",children:[(0,t.jsx)("div",{ref:a,className:"absolute inset-0"}),(0,t.jsx)("canvas",{ref:c,className:"absolute inset-0 size-full"})]})}])}};
