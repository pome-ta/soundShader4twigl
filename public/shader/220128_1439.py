#define BPM 140.
#define A (15./BPM)

float adsr(float t, float a, float d, float s, float r, float gt)
{  
    return max(0.0,
    min(1.0, t/max(1e-4, a)) 
        - min((1.0 - s) ,max(0.0, t - a)*(1.0 - s)/max(1e-4, d))
        - max(0.0, t - gt)*s/max(1e-4, r));
}

float noise(float t)
{
    return fract(sin(t*45678.0)*1234.5)*2.0-1.0;
}

float square(float f)
{
return sign(fract(f)-0.5);
}

float kick(float t){
return sin(315.0*t-10.0*exp(-50.0*t))*adsr(t,0.0, 0.3, 0.0, 0.0, 0.0);
+0.2*square(50.0*t)* adsr(t,0.0, 0.05, 0.0, 0.0, 0.0);
}

float snare(float t)
{
    return noise(t)*adsr(t,0.01, 0.1, 0.0, 0.0, 0.0);
}

float closeHihat(float t)
{
    return noise(t)*adsr(t,0.0, 0.03, 0.0, 0.0, 0.0);
}

float openHihat(float t)
{
    return noise(t)*adsr(t,0.0, 0.05, 0.5, 0.03, 0.03);
}

float sequence(int s,float t)
{
  float n =mod(t,A);
  for(int i=0;i<16;i++){
    if((s>>(int(t/A)-i)%16&1)==1)break;
    n+=A;
  }
  return n;
}

#define Rhythm2Int(v,a)v=0;for(int i=0;i<16;i++)v+=a[i]<<i;

vec2 mainSound( float time )
{   
    
    int[4] r_kick;       // int[](0x0c05,0x0c05,0x0405,0x0c0c)
    int[4] r_snare;      // int[](0x9290,0x9290,0x4290,0x4292)
    int[4] r_closeHihat; // int[](0x5555,0x5555,0x5555,0x5155)
    int[4] r_openHihat;  // int[](0x0000,0x0000,0x0000,0x0400)
    int[4] r_velocity;   // int[](0x3030,0x3030,0x3030,0x3030)
        
    Rhythm2Int( r_kick[0],       int[]( 1,0,1,0, 0,0,0,0, 0,0,1,1, 0,0,0,0 ))
    Rhythm2Int( r_snare[0],      int[]( 0,0,0,0, 1,0,0,1, 0,1,0,0, 1,0,0,1 ))
    Rhythm2Int( r_closeHihat[0], int[]( 1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0 ))
    Rhythm2Int( r_openHihat[0],  int[]( 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0 ))
    Rhythm2Int( r_velocity[0],   int[]( 0,0,0,0, 1,1,0,0, 0,0,0,0, 1,1,0,0 ))
        
    Rhythm2Int( r_kick[1],       int[]( 1,0,1,0, 0,0,0,0, 0,0,1,1, 0,0,0,0 ))
    Rhythm2Int( r_snare[1],      int[]( 0,0,0,0, 1,0,0,1, 0,1,0,0, 1,0,0,1 ))
    Rhythm2Int( r_closeHihat[1], int[]( 1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0 ))
    Rhythm2Int( r_openHihat[1],  int[]( 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0 ))
    Rhythm2Int( r_velocity[1],   int[]( 0,0,0,0, 1,1,0,0, 0,0,0,0, 1,1,0,0 ))

    Rhythm2Int( r_kick[2],       int[]( 1,0,1,0, 0,0,0,0, 0,0,1,0, 0,0,0,0 ))
    Rhythm2Int( r_snare[2],      int[]( 0,0,0,0, 1,0,0,1, 0,1,0,0, 0,0,1,0 ))
    Rhythm2Int( r_closeHihat[2], int[]( 1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0 ))
    Rhythm2Int( r_openHihat[2],  int[]( 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0 ))
    Rhythm2Int( r_velocity[2],   int[]( 0,0,0,0, 1,1,0,0, 0,0,0,0, 1,1,0,0 ))

    Rhythm2Int( r_kick[3],       int[]( 0,0,1,1, 0,0,0,0, 0,0,1,1, 0,0,0,0 ))
    Rhythm2Int( r_snare[3],      int[]( 0,1,0,0, 1,0,0,1, 0,1,0,0, 0,0,1,0 ))
    Rhythm2Int( r_closeHihat[3], int[]( 1,0,1,0, 1,0,1,0, 1,0,0,0, 1,0,1,0 ))
    Rhythm2Int( r_openHihat[3],  int[]( 0,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,0,0 ))
    Rhythm2Int( r_velocity[3],   int[]( 0,0,0,0, 1,1,0,0, 0,0,0,0, 1,1,0,0 ))
    
    int i = int(floor(time/(A*16.)))&3;
    int velocity = r_velocity[i]>>(int(floor(time/A))&15)&1;
    float vol = 0.2 *(1.0+0.5*float(velocity));
    return vec2(
        0.0
+0.4 * kick(sequence(       r_kick[i],       time))
        +0.3 * snare(sequence(      r_snare[i],      time))
        +vol * closeHihat(sequence( r_closeHihat[i], time))
        +vol * openHihat(sequence(  r_openHihat[i],  time))
    );
}
