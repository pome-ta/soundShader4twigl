// [20220609_fract step velocity](https://www.shadertoy.com/view/NsVcDR)


#define saturate(i) clamp(i,0.,1.)
#define clip(i) clamp(i,-1.,1.)
#define lofi(i,j) (floor((i)/(j))*(j))
#define tri(p) (1.-4.*abs(fract(p)-0.5))

const float BPM = 140.0;

// fract( a * step + b )
const float FRACT_STEP_VELOCITY_A = 0.62;
const float FRACT_STEP_VELOCITY_B = 0.67;

// constants
const float PI = acos(-1.0);
const float TAU = PI * 2.0;
const float SQRT2 = sqrt(2.0);

const float BPS = BPM / 60.0;
const float TIME2BEAT = BPS;
const float BEAT2TIME = 1.0 / BPS;


float rand(vec2 st) {
  vec2 magic2 = vec2(12.9898, 78.233);
  float _rnd = sin(dot(st, magic2));
  return fract(_rnd * 43758.5453123);
}



vec2 kick( float t ) {
  float phase = 45.0 * t - 6.0 * exp( -40.0 * t ) - 3.0 * exp( -400.0 * t );
  float decay = exp( -3.0 * t );
  return vec2( decay * sin( TAU * phase ) );
}

vec2 hihat( float t, float d ) {
  float decay = exp( -d * t );
  vec2 sig = vec2(1.0 - 2.0 * rand(vec2(t)));
  sig -= vec2(1.0 - 2.0 * rand(vec2(t + 0.007))); // pseudo high pass. shoutouts to aaaidan
  return sig * decay;
}


vec2 mainSound(float time) {
  float beat = time * TIME2BEAT;
  vec2 dest = vec2( 0.0 );
    
  float tKick = mod( beat, 1.0 ) * BEAT2TIME;
  dest += 0.5 * kick( tKick );
  
  float tHihat = mod( beat, 0.25 ) * BEAT2TIME;
  float stepHihat = mod( floor( beat * 4.0 ), 16.0 );
  float velHihat = fract( FRACT_STEP_VELOCITY_A * stepHihat + FRACT_STEP_VELOCITY_B ); // fract step velocity here
  float decayHihat = pow( 2.0, 8.0 - 3.0 * velHihat );
  float ampHihat = mix( 0.7, 1.0, velHihat );
  dest += 0.2 * ampHihat * hihat( tHihat, decayHihat  );

  
  
  
  return clip( dest );
  //return dest;
}



