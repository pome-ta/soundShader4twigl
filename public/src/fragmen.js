export class Fragmen {
  /**
   * resolution, mouse, time, backbuffer の各種 uniform 定義で動作するクラシックモード
   * @type {number}
   */
  // xxx: `switch` 分岐をどうやってハンドリングするか
  static get MODE_CLASSIC(){return 0;}
  
  /**
   * constructor of fragmen.js
   * @param {object} option - オプション
   * @property {HTMLElement} option.target - insert canvas to
   * @property {HTMLElement} [option.eventTarget=target] - event target element or window
   * @property {boolean} [option.mouse=false] - mouse event enable
   * @property {boolean} [option.escape=false] - keydown event enable
   * @property {boolean} [option.resize=false] - resize event enable
   */
  constructor(option){
    /**
     * WebGL コンテキストに紐づく canvas の挿入先となるエレメント
     * @type {HTMLElement}
     */
    this.target = null;
    /**
     * マウスイベントの対象となるエレメント（もしくは window）
     * @type {window|HTMLElement}
     */
    this.eventTarget = null;
    /**
     * WebGL コンテキストに紐づく canvas
     * @type {HTMLCanvasElement}
     */
    this.canvas = null;
    /**
     * WebGL 2.0 で初期化できたかどうか
     * @type {boolean}
     */
    this.isWebGL2 = false;
    /**
     * WebGL のレンダリングコンテキスト
     * @type {WebGLRenderingContext}
     */
    this.gl = null;
    /**
     * リサイズが発生したかどうかのフラグ
     * @type {boolean}
     */
    this.resize = false;
    /**
     * コンテキストの幅
     * @type {number}
     */
    this.width  = 0;
    /**
     * コンテキストの高さ
     * @type {number}
     */
    this.height = 0;
    /**
     * マウスカーソルの座標
     * @type {Array.<number>}
     */
    this.mousePosition = [0.0, 0.0];
    /**
     * 現在設定されているモード
     * @type {number}
     */
    this.mode = Fragmen.MODE_CLASSIC;
    /**
     * アニメーションさせるかどうかのフラグ（コンパイルは普通に行うが描画だけを止める）
     * @type {boolean}
     */
    this.animation = true;
    /**
     * 実行中かどうかのフラグ
     * @type {boolean}
     */
    this.run = false;
    /**
     * レンダリングを開始した時点でのタイムスタンプ
     * @type {number}
     */
    this.startTime = 0;
    /**
     * レンダリング開始からの経過時間（秒）
     * @type {number}
     */
    this.nowTime = 0;
    /**
     * レンダリング開始からの経過フレーム数
     * @type {number}
     */
    this.frameCount = 0;
    /**
     * シェーダプログラム
     * @type {WebGLProgram}
     */
    this.program = null;
    /**
     * uniform ロケーション
     * @type {object}
     */
    this.uniLocation = null;
    /**
     * attribute ロケーション
     * @type {object}
     */
    this.attLocation = null;
    /**
     * Onomat.js からの周波数の入力値
     * @type {number}
     */
    this.frequency = 0;
    /**
     * 頂点シェーダのソースコード
     * @type {string}
     */
    this.VS = '';
    /**
     * フラグメントシェーダのソースコード
     * @type {string}
     */
    this.FS = '';
    /**
     * 転写用シェーダのプログラム
     * @type {WebGLProgram}
     */
    this.postProgram = null;
    /**
     * 転写用シェーダの uniform ロケーション
     * @type {object}
     */
    this.postUniLocation = null;
    /**
     * 転写用シェーダの attribute ロケーション
     * @type {object}
     */
    this.postAttLocation = null;
    /**
     * 転写用シェーダの頂点シェーダのソースコード
     * @type {string}
     */
    this.postVS = '';
    /**
     * 転写用シェーダのフラグメントシェーダのソースコード
     * @type {string}
     */
    this.postFS = '';
    /**
     * バッファリング用フレームバッファ
     * @type {WebGLFrameBuffer}
     */
    this.fFront = null;
    /**
     * バッファリング用フレームバッファ
     * @type {WebGLFrameBuffer}
     */
    this.fBack = null;
    /**
     * バッファリング用フレームバッファ
     * @type {WebGLFrameBuffer}
     */
    this.fTemp = null;
    /**
     * MRT で gl.drawBuffers に指定するアタッチメント用定数を格納する配列
     * @type {Array.<number>}
     */
    this.buffers = null;
    /*
    // self binding
    this.render    = this.render.bind(this);
    this.rect      = this.rect.bind(this);
    this.reset     = this.reset.bind(this);
    this.draw      = this.draw.bind(this);
    this.mouseMove = this.mouseMove.bind(this);
    this.keyDown   = this.keyDown.bind(this);
    */
    // initial call
    this.init(option);
  }


  /**
   * initialize fragmen.js
   * @param {object} option - options
   */
  init(option){
    // option check
    if(option === null || option === undefined){return;}
    if(!option.hasOwnProperty('target') || option.target === null || option.target === undefined){return;}
    if(!(option.target instanceof HTMLElement)){return;}
    
    // init canvas
    this.target = this.eventTarget = option.target;
    if(this.target.tagName.match(/canvas/i)){
      this.canvas = this.target;
    }else{
      this.canvas = document.createElement('canvas');
      this.target.appendChild(this.canvas);
    }
    
    // init webgl context
    const opt = {alpha: false, preserveDrawingBuffer: true};
    this.gl = this.canvas.getContext('webgl2', opt);
    this.isWebGL2 = this.gl != null;
    if(this.isWebGL2 !== true){
      this.gl = this.canvas.getContext('webgl', opt);
      this.gl.getExtension('OES_standard_derivatives');
    }
    if(this.gl == null){
      console.log('webgl unsupported');
      return;
    }
    
    // check event
    if(option.hasOwnProperty('eventTarget') && option.eventTarget !== null && option.eventTarget !== undefined){
      this.eventTarget = option.eventTarget;
    }
    if(option.hasOwnProperty('mouse') && option.mouse === true){
      this.eventTarget.addEventListener('pointermove', this.mouseMove, false);
    }
    if(option.hasOwnProperty('escape') && option.escape === true){
      window.addEventListener('keydown', this.keyDown, false);
    }
    if(option.hasOwnProperty('resize') && option.resize === true){
      this.resize = true;
      window.addEventListener('resize', this.rect, false);
    }
    // render initial
    this.VS = 'attribute vec3 p;void main(){gl_Position=vec4(p,1.);}';
    
    this.postVS = `
attribute vec3 position;
varying   vec2 vTexCoord;
void main(){
    vTexCoord   = (position + 1.0).xy / 2.0;
    gl_Position = vec4(position, 1.0);
}`;

    this.postFS = `
precision mediump float;
uniform sampler2D texture;
varying vec2      vTexCoord;
void main(){
    gl_FragColor = texture2D(texture, vTexCoord);
}`;

    this.postProgram = this.gl.createProgram();
    let vs = this.createShader(this.postProgram, 0, this.postVS);
    let fs = this.createShader(this.postProgram, 1, this.postFS);
    this.gl.linkProgram(this.postProgram);
    this.gl.deleteShader(vs);
    this.gl.deleteShader(fs);
    this.postUniLocation = {};
    this.postUniLocation.texture = this.gl.getUniformLocation(this.postProgram, 'texture');
    this.postAttLocation = this.gl.getAttribLocation(this.postProgram, 'position');

    this.post300VS = `#version 300 es
in  vec3 position;
out vec2 vTexCoord;
void main(){
    vTexCoord   = (position + 1.0).xy / 2.0;
    gl_Position = vec4(position, 1.0);
}`;

    this.post300FS = `#version 300 es
precision mediump float;
uniform sampler2D drawTexture;
in vec2 vTexCoord;
layout (location = 0) out vec4 outColor;
void main(){
    outColor = texture(drawTexture, vTexCoord);
}`;

    if(this.isWebGL2 === true){
      this.post300Program = this.gl.createProgram();
      vs = this.createShader(this.post300Program, 0, this.post300VS);
      fs = this.createShader(this.post300Program, 1, this.post300FS);
      this.gl.linkProgram(this.post300Program);
      this.gl.deleteShader(vs);
      this.gl.deleteShader(fs);
      this.post300UniLocation = {};
      this.post300UniLocation.texture = this.gl.getUniformLocation(this.post300Program, 'drawTexture');
      this.post300AttLocation = this.gl.getAttribLocation(this.post300Program, 'position');
    }

    this.fFront = this.fBack = this.fTemp = null;
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.gl.createBuffer());
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array([-1,1,0,-1,-1,0,1,1,0,1,-1,0]), this.gl.STATIC_DRAW);
    this.gl.disable(this.gl.DEPTH_TEST);
    this.gl.disable(this.gl.CULL_FACE);
    this.gl.disable(this.gl.BLEND);
    this.gl.clearColor(0.0, 0.0, 0.0, 1.0);
  }
  
  /**
   * rendering hub
   * @param {string} source - fragment shader source
   * @return {object} instance
   */
  render(source){
    if(source === null || source === undefined || source === ''){
      if(this.FS === ''){return;}
    }else{
      this.FS = source;
    }
    this.reset();
    return this;
  }
  
  /**
   * set rect
   */
  rect(){}
  
  /**
   * reset renderer
   */
  reset(){}
  
  /**
   * rendering
   */
  draw(){}
  
  
  /**
   * create and compile shader
   * @param {WebGLProgram} p - target program object
   * @param {number} i - 0 or 1, 0 is vertex shader compile mode
   * @param {string} j - shader source
   * @return {boolean|WebGLShader} compiled shader object or false
   */
  createShader(p, i, j){
    if(!this.gl){return false;}
    const k = this.gl.createShader(this.gl.VERTEX_SHADER - i);
    this.gl.shaderSource(k, j);
    this.gl.compileShader(k);
    const t = getTimeString();
    if(!this.gl.getShaderParameter(k, this.gl.COMPILE_STATUS)){
      let msg = this.gl.getShaderInfoLog(k);
      msg = this.formatErrorMessage(msg);
      console.warn(msg);
      if(this.onBuildCallback != null){
        this.onBuildCallback('error', ` ● [ ${t} ] ${msg}`);
      }
      return false;
    }
    if(this.onBuildCallback != null){
    this.onBuildCallback('success', ` ● [ ${t} ] shader compile succeeded`);
    }
    this.gl.attachShader(p, k);
    const l = this.gl.getShaderInfoLog(k);
    if(l !== ''){console.info('shader info: ' + l);}
    return k;
  }



}

/**
 * 時刻を常に２桁に揃える
 * @return {string}
 */
function getTimeString(){
    const d = new Date();
    const h = (new Array(2).join('0') + d.getHours()).substr(-2, 2);
    const m = (new Array(2).join('0') + d.getMinutes()).substr(-2, 2);
    return `${h}:${m}`;
}

