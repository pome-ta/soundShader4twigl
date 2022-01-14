let VERTEX_SHADER;
let FRAGMENT_SHADER;

attribute vec3 p;
void main(){
  gl_Position=vec4(p,1.);
}


#version 300 es
in vec3 p;
void main(){
  gl_Position = vec4(p, 1.0);
}

const canvas = document.createElement('canvas');
canvas.width = 512;
canvas.height = 512;

const gl = canvas.getContext('webgl2');


console.log(gl)


/**
 * シェーダオブジェクトのコンパイル
 * @param {string} source - シェーダのソースコード
 * @param {boolean} isVertexShader - 頂点シェーダかどうか
 * @return {WebGLShader}
 */
createShader(source, isVertexShader){
  const type = isVertexShader === true ? this.gl.VERTEX_SHADER : this.gl.FRAGMENT_SHADER;
  const shader = this.gl.createShader(type);
  this.gl.shaderSource(shader, source);
  this.gl.compileShader(shader);
  if(!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)){
    let msg = this.gl.getShaderInfoLog(shader);
    console.log('createShader');
    console.log(msg);
    return false;
  }
  return shader;
}
