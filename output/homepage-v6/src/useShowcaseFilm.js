import {usePlaybackClock} from './usePlaybackClock.js';

export function useShowcaseFilm(root,duration,enabled=true,observeKey){
 return usePlaybackClock(root,duration,{enabled,reducedEnd:true,observeKey});
}
