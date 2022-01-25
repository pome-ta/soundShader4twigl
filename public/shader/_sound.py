vec2 mainSound(float time) {
  float pi = acos(-1.0);
  float pi2 = pi * 2.0;
  float envelope = -1.0;
  
  float wave880 = sin(pi2 * 880.0 * time);
  float env880 = wave880 * fract((envelope / 4.0) * time);
  
  float wave440 = sin(pi2 * 440.0 * time);
  float env440 = wave440 * smoothstep(0.8, 0.9, fract(envelope * time));
  
  //return vec2(wave440 * pow(fract(envelope * time), 4.0));
  //return vec2(mod(env440, wave440));
  //return vec2(wave440, env440);
  return vec2(sin(.2831*256.*time*3.)+pow(fract(5.2831*2.*time*.5),.4) * env440 + env880);
}




/*
float fm(float time){
  return sin(1000.*time+sin(300.*time));
}
float rhy(float time,float f){
  return pow(fract(mod(-time*8.,8.)/3.),6.-3.*f);
}
vec2 dfm(float time,float dt){
    return exp(-3.0*dt)*
        fm(8.*time)*
        vec2(rhy(time-.3*dt,dt),rhy(time-.5*dt,dt));
}
vec2 mainSound(float time){
  vec2 s;
  s += vec2(3.0*sin(3e2*time)*pow(fract(-time*2.),4.));
  s += vec2(0.5*sin(4e5*time)*fract(-time*2.+.5));
  s += dfm(time,0.0);
  s += dfm(time,0.5);
  s += dfm(time,1.0);
  s += dfm(time,2.0);
  return 0.3*s;
}*/




/*
vec2 mainSound(float time) {
  float pi = acos(-1.0);
  float pi2 = pi * 2.0;
  float envelope = -1.0;
  
  float wave880 = sin(pi2 * 880.0 * time);
  float env880 = wave880 * fract((envelope / 4.0) * time);
  
  float wave440 = sin(pi2 * 440.0 * time);
  float env440 = wave440 * fract(envelope * time);
  
  //return vec2(env440);
  //return vec2(wave440 * exp(-1.0 * abs(sin(time) * 4.0)));
  //return vec2((sin(time * 5.0) * 0.7 + 0.3) + env440);
  //return vec2((sin(time * 5.0) * 0.5 + 0.5) + env440) * floor(mod(time, 2.0));
  
  return vec2(wave440 * fract(envelope * abs(sin(time))));
  //return vec2(mod(-time, wave440));
  
}



*/
