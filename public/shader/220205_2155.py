// https://raku-phys.hatenablog.com/entry/2020/04/19/002400

float fm(float time){
  return sin(1000.0 * time + sin(300.0 * time));
}
float rhy(float time, float f){
  return pow(fract(mod(-time * 8.0, 8.0) / 3.0), 6.0 - 3.0 * f);
}
vec2 dfm(float time,float dt){
  return exp(-3.0 * dt) * fm(8.0 * time) *
    vec2(rhy(time - 0.3 * dt, dt),
         rhy(time - 0.5 * dt, dt));
}
vec2 mainSound(float time){
  vec2 s;
  
  // bd
  //s += vec2(3.0 * sin(3e2 * time) * pow(fract(-time * 2.0), 4.0));
  
  // hh
  s += vec2(0.5 * sin(4e5 * time) * fract(-time * 2.0 + 0.5));
  
  //s += dfm(time, 0.0);
  s += dfm(time, 0.5);
  //s += dfm(time, 1.0);
  //s += dfm(time, 2.0);
  return 0.3 * s;
}
