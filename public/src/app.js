import {Fragmen} from './fragmen.js';

//console.log('start');

(() => {
let canvas = null;  // スクリーン
let fragmen = null;  // fragmen.js のインスタンス

// fragmen.js 用のオプションの雛形
const FRAGMEN_OPTION = {
  target: null,
  eventTarget: null,
  mouse: true,
  resize: true,
  escape: false
}


window.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded');
  // DOM への参照
  canvas = document.querySelector('#webgl');
  
  // fragmen からデフォルトのソース一覧を取得
  const fragmenDefaultSource = Fragmen.DEFAULT_SOURCE;
  
  // ウィンドウのリサイズ時
  window.addEventListener('resize', () => {
    //console.log('resize');
    resize();
  }, false);
  // 最初に一回リサイズ相当の処理を行っておく
  resize();
  
  // メインとなる fragmen のインスタンス
  const option = Object.assign(FRAGMEN_OPTION, {
    target: canvas,
    eventTarget: window,
  });
  /*
  console.log(option);
  console.log('main');
  console.log(canvas.width);
  console.log(canvas.height);
  */
  
  fragmen = new Fragmen(option);
}, false);



/**
 * ウィンドウリサイズ時の処理
 */
function resize(){
  const canvas = document.querySelector('#webgl');
  const bound = canvas.parentElement.getBoundingClientRect();
  canvas.width = bound.width;
  canvas.height = bound.height;
  /*
  console.log('resize');
  console.log(canvas.width);
  console.log(canvas.height);
  */
}



})();
//console.log('end');

