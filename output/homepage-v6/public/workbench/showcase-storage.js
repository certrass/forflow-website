// Tour mutations never replace a visitor's independent workbench session.
(()=>{
 const tour=new URLSearchParams(location.search).has('tour');
 const memory=new Map(),prefix='forflow.homepage.workbench.20260910.';
 window.FFShowcaseStorage={
  getItem(key){if(tour)return memory.get(key)||null;try{return sessionStorage.getItem(prefix+key)}catch{return memory.get(key)||null}},
  setItem(key,value){memory.set(key,value);if(!tour)try{sessionStorage.setItem(prefix+key,value)}catch{}},
 };
})();
