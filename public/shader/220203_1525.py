#define BPM 120.0
const float PI = acos(-1.0);
const float TAU = PI * 2.0;



/* GLSL */
// 2D Random
float _rnd(in vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}


// Based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float _ns (in vec2 _st) {
  vec2 i = floor(_st);
  vec2 f = fract(_st);

  // Four corners in 2D of a tile
  float a = _rnd(i);
  float b = _rnd(i + vec2(1.0, 0.0));
  float c = _rnd(i + vec2(0.0, 1.0));
  float d = _rnd(i + vec2(1.0, 1.0));

  vec2 u = f * f * (3.0 - 2.0 * f);

  return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

#define NUM_OCTAVES 5
float _fbm ( in vec2 _st) {
  float v = 0.0;
  float a = 0.5;
  vec2 shift = vec2(100.0);
  // Rotate to reduce axial bias
  mat2 rot = mat2(cos(0.5), sin(0.5),
                 -sin(0.5), cos(0.50));
  for (int i = 0; i < NUM_OCTAVES; ++i) {
    v += a * _ns(_st);
    _st = rot * _st * 2.0 + shift;
    a *= 0.5;
  }
  return v;
}


/* sound common */
float timeToBeat(float t) {return t / 60.0 * BPM;}
float beatToTime(float b) {return b / BPM * 60.0;}

float sine(float phase) {
  return sin(TAU * phase );
}
float saw(float phase) {
  return 2.0 * fract(phase) - 1.0;
}
float square(float phase) {
  return fract(phase) < 0.5 ? -1.0 : 1.0;
}
float triangle(float phase) {
  return 1.0 - 4.0 * abs(fract(phase) - 0.5);
}

float pulse(float phase, float duty) {
  return fract(phase) < abs(duty) ? -1.0 : 1.0;
}



float random(float time) {
  float rnd_x = sine(123.4 * time);
  float rnd_y = sine(567.8 * time);
  return 2.0 * _rnd(vec2(rnd_x, rnd_y)) - 1.0;
}


float noise(float time) {
  float rnd_x = sine(123.4 * time);
  float rnd_y = sine(567.8 * time);
  return 2.0 * _ns(vec2(rnd_x, rnd_y)) - 1.0;
}


float fbm(float time) {
  float rnd_x = sine(123.4 * time);
  float rnd_y = sine(567.8 * time);
  return 2.0 * _fbm(vec2(rnd_x, rnd_y)) - 1.0;
}



float adsr(float t, float a, float d, float s, float r, float gt) {
  return max(0.0, min(1.0, t/max(1e-4, a)) - min((1.0 - s) ,max(0.0, t - a)*(1.0 - s)/max(1e-4, d)) - max(0.0, t - gt)*s/max(1e-4, r));
}


float kick(float time) {
  float amp = exp(-0.75 * time);
  float phase = 32.0 * time - 24.0 * exp(-1.25 * time);
  return amp * sine( phase );
}

float snare(float time){
  float s_amp = exp(-32.0 * time);
  float s_phase = 64.0 * time - 32.0 * exp(-8.0 * time);
  
  float n_amp = exp(-48.0 * time);
  float tic = n_amp * random(time * 1e2);
  float rnd = 2.0 * sine(123.4 * time) -1.0;
  float noize = tic * sin(random(rnd));
  
  return s_amp * sine(s_phase + noize);
}

float hihat(float time) {
  float amp = exp(-128.0 * time);
  
  float tic = amp * random(time);
  float rnd = 2.0 * saw(123.4 * time) -1.0;
  float vib = 0.5 * sine(time * .75);
  return tic * sin(random(rnd));
}


float rrr (in vec2 _st) {
    return fract(sin(dot(_st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}

vec2 mainSound(float time) {
  float beat = timeToBeat(time);
  float tempo = sine((mod(beat, 4.0) >= 1.0 ? 440.0 : 880.0) * time) * exp(-1e2 * fract(beat));
  
  
  //return vec2(random(time / 9.0));
  return vec2(_fbm(gl_FragCoord.xy));
}













