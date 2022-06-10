// memo: https://www.shadertoy.com/view/NsVcDR
// kick

#define saturate(i) clamp(i,0.,1.)
#define clip(i) clamp(i,-1.,1.)
#define lofi(i,j) (floor((i)/(j))*(j))
#define tri(p) (1.-4.*abs(fract(p)-0.5))

const float BPM = 140.0;

// fract( a * step + b )
const float FRACT_STEP_VELOCITY_A = 0.62;
const float FRACT_STEP_VELOCITY_B = 0.67;

// constants
const float PI = acos( -1.0 );
const float TAU = PI * 2.0;
const float SQRT2 = sqrt( 2.0 );

const float BPS = BPM / 60.0;
const float TIME2BEAT = BPS;
const float BEAT2TIME = 1.0 / BPS;


vec2 kick( float t ) {
  float phase = 45.0 * t - 6.0 * exp( -40.0 * t ) - 3.0 * exp( -400.0 * t );
  float decay = exp( -3.0 * t );
  return vec2( decay * sin( TAU * phase ) );
}

vec2 mainSound(float time) {
  
  float beat = time * TIME2BEAT;
    
  vec2 dest = vec2( 0.0 );
    
  float tKick = mod( beat, 1.0 ) * BEAT2TIME;
  dest += 0.5 * kick( tKick );
  
  //return clip( dest );
  return dest;
}



