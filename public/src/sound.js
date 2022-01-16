import {wavVisualize} from './visualizar.js';
import {barVisualize} from './visualizar.js';

let VERTEX_SHADER_SOURCE;
let FRAGMENT_SHADER_SOURCE;
const DURATION = 180;
const BUFFER_WIDTH = 512;
const BUFFER_HEIGHT = 512;
const FFT_SIZE = 128;

VERTEX_SHADER_SOURCE = `#version 300 es
in vec3 p;
void main(){
  gl_Position = vec4(p, 1.0);
}`;

FRAGMENT_SHADER_SOURCE = `#version 300 es
precision highp float;
uniform float blockOffset;
uniform float sampleRate;

out vec4 outColor;

vec2 mainSound(float time){
  //return vec2(sin(6.2831*440.*time));
  //return vec2(sin(6.2831*440.*time)*exp(-3.*time));
  //return vec2(sin(6.2831*440.*time)+sin(6.2831*440.*1.5*time));
  //return vec2((fract(sin(time*1e3)*1e6)-.5)*pow(fract(-time*4.),mod(time*4.,2.)*8.));
  return vec2(3.0*sin(3e2*time)*pow(fract(-time*2.),4.));
}
void main(){
  float time = blockOffset + ((gl_FragCoord.x - 0.5) + (gl_FragCoord.y - 0.5) * 512.0) / sampleRate;
  vec2 XY = mainSound(time);
  vec2 XV = floor((0.5 + 0.5 * XY) * 65536.0);
  vec2 XL = mod(XV, 256.0) / 255.0;
  vec2 XH = floor(XV / 256.0) / 255.0;
  outColor = vec4(XL.x, XH.x, XL.y, XH.y);
}
`;

/*
#version 300 es
precision highp float;
uniform float blockOffset;
uniform float sampleRate;

out vec4 outColor;

vec2 mainSound(float time){
  //return vec2(sin(6.2831*440.*time));
  //return vec2(sin(6.2831*440.*time)*exp(-3.*time));
  //return vec2(sin(6.2831*440.*time)+sin(6.2831*440.*1.5*time));
  //return vec2((fract(sin(time*1e3)*1e6)-.5)*pow(fract(-time*4.),mod(time*4.,2.)*8.));
  vec2 kick = vec2(3.0*sin(3e2*time)*pow(fract(-time*2.),4.));
  vec2 hh = vec2((fract(cos(time*1e3)*1e6)-.5)*pow(fract(-time*4.),mod(time*4.,2.)*8.))-0.5;
  return kick + hh;
}
void main(){
  float time = blockOffset + ((gl_FragCoord.x - 0.5) + (gl_FragCoord.y - 0.5) * 512.0) / sampleRate;
  vec2 XY = mainSound(time);
  vec2 XV = floor((0.5 + 0.5 * XY) * 65536.0);
  vec2 XL = mod(XV, 256.0) / 255.0;
  vec2 XH = floor(XV / 256.0) / 255.0;
  outColor = vec4(XL.x, XH.x, XL.y, XH.y);
}
*/


/*
#version 300 es
in vec3 p;void main(){gl_Position=vec4(p,1.);}

*/


const canvas = document.createElement('canvas');

const waveCanvas = document.querySelector('#waveVisualizer');
const barCanvas = document.querySelector('#barVisualizer');

const wrap = document.querySelector('#wrap');
wrap.appendChild(canvas);

canvas.width = BUFFER_WIDTH;
canvas.height = BUFFER_HEIGHT;


const gl = canvas.getContext('webgl2');
const vs = createShader(VERTEX_SHADER_SOURCE, true);


const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

const fs = createShader(FRAGMENT_SHADER_SOURCE, false);

let program = gl.createProgram();
gl.attachShader(program, vs);
gl.attachShader(program, fs);
gl.linkProgram(program);
gl.deleteShader(fs);


if(!gl.getProgramParameter(program, gl.LINK_STATUS)) {
  let msg = gl.getProgramInfoLog(program);
  console.log('render');
  console.log(msg);
  program = null;
}


if(program != null){gl.deleteProgram(program);}
gl.useProgram(program);
const attLocation = gl.getAttribLocation(program, 'p');

const uniLocation = {
  blockOffset: gl.getUniformLocation(program, 'blockOffset'),
  sampleRate: gl.getUniformLocation(program, 'sampleRate'),
};

gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
gl.bufferData(
  gl.ARRAY_BUFFER,
  new Float32Array(
    [-1.0,  1.0,  0.0, -1.0,
     -1.0,  0.0,  1.0,  1.0,
      0.0,  1.0, -1.0,  0.0]
  ), gl.STATIC_DRAW);
gl.enableVertexAttribArray(attLocation);
gl.vertexAttribPointer(attLocation, 3, gl.FLOAT, false, 0, 0);
gl.disable(gl.DEPTH_TEST);
gl.disable(gl.CULL_FACE);
gl.disable(gl.BLEND);
gl.clearColor(0.0, 0.0, 0.0, 0.0);
gl.clear(gl.COLOR_BUFFER_BIT);
gl.viewport(0, 0, BUFFER_WIDTH, BUFFER_HEIGHT);


/* draw */
// WebAudio 関係の初期設定
const sample = audioCtx.sampleRate;
const buffer = audioCtx.createBuffer(2, sample * DURATION, sample);

const channelDataLeft  = buffer.getChannelData(0);
const channelDataRight = buffer.getChannelData(1);
const range = BUFFER_WIDTH * BUFFER_HEIGHT;
const pixel = new Uint8Array(BUFFER_WIDTH * BUFFER_HEIGHT * 4);
gl.uniform1f(uniLocation.sampleRate, sample);
const block = Math.ceil((sample * DURATION) / range);
console.log(uniLocation.sampleRate);

for(let i = 0, j = block; i < j; ++i){
  gl.uniform1f(uniLocation.blockOffset, i * range / sample);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.readPixels(0, 0, BUFFER_WIDTH, BUFFER_HEIGHT, gl.RGBA, gl.UNSIGNED_BYTE, pixel);
  for(let k = 0, l = range; k < l; ++k){
    channelDataLeft[i * range + k]  = (pixel[k * 4 + 0] + 256 * pixel[k * 4 + 1]) / 65535 * 2 - 1;
    channelDataRight[i * range + k] = (pixel[k * 4 + 2] + 256 * pixel[k * 4 + 3]) / 65535 * 2 - 1;
  }
}



// 再生のための準備と再生処理
const audioBufferSourceNode = audioCtx.createBufferSource();
const audioAnalyserNode = audioCtx.createAnalyser();
audioAnalyserNode.smoothingTimeConstant = 0.8;
audioAnalyserNode.fftSize = FFT_SIZE * 2;
const audioFrequencyBinCount = audioAnalyserNode.frequencyBinCount;


audioAnalyserNode.minDecibels = -90;
audioAnalyserNode.maxDecibels = -10;
    wavVisualize(waveCanvas, audioAnalyserNode);
    barVisualize(barCanvas, audioAnalyserNode);

audioBufferSourceNode.connect(audioAnalyserNode);
audioAnalyserNode.connect(audioCtx.destination);
audioBufferSourceNode.buffer = buffer;

//console.log(buffer);
audioBufferSourceNode.loop = false;
audioBufferSourceNode.start();


// 着火のおまじない
  
const eventName = typeof document.ontouchend !== 'undefined' ? 'touchend' : 'mouseup';
document.addEventListener(eventName, initAudioContext);
function initAudioContext(){
  document.removeEventListener(eventName, initAudioContext);
  // wake up AudioContext
  audioCtx.resume();
  //audioBufferSourceNode.start();
}


console.log('end');

/**
 * シェーダオブジェクトのコンパイル
 * @param {string} source - シェーダのソースコード
 * @param {boolean} isVertexShader - 頂点シェーダかどうか
 * @return {WebGLShader}
 */

function createShader(source, isVertexShader) {
  const type = isVertexShader === true ? gl.VERTEX_SHADER : gl.FRAGMENT_SHADER;
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if(!gl.getShaderParameter(shader, gl.COMPILE_STATUS)){
    let msg = gl.getShaderInfoLog(shader);
    console.log('createShader');
    console.log(msg);
    return false;
  }
  //console.log(`${isVertexShader}: ${source}`);
  return shader;
}

