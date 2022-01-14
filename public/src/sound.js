let VERTEX_SHADER;
let FRAGMENT_SHADER;


VERTEX_SHADER = `#version 300 es
in vec3 p;
void main(){
  gl_Position = vec4(p, 1.0);
}`;

FRAGMENT_SHADER = `#version 300 es
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
`;

const canvas = document.createElement('canvas');
canvas.width = 512;
canvas.height = 512;


const gl = canvas.getContext('webgl2');
const vs = createShader(VERTEX_SHADER, true);

const audioCtx = new AudioContext();

const fs = createShader(FRAGMENT_SHADER, false);

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
attLocation = gl.getAttribLocation(program, 'p');

uniLocation = {
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
gl.viewport(0, 0, 512, 512);



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
  return shader;
}

