vec2 mainSound(float time){
  //return vec2(sin(6.2831*440.*time));
  //return vec2(sin(6.2831*440.*time)*exp(-3.*time));
  //return vec2(sin(6.2831*440.*time)+sin(6.2831*440.*1.5*time));
  //return vec2((fract(sin(time*1e3)*1e6)-.5)*pow(fract(-time*4.),mod(time*4.,2.)*8.));
  
  return vec2(3.0*sin(3e2*time)*pow(fract(-time*2.),4.));
  //return vec2(3.0*sin(2e2*time)*pow(fract(-time*1.25),6.));
  /*
  vec2 hh = vec2(tan((fract(sin(time*1e2)*1e6)-.5)*pow(fract(-time*8.),mod(time*4.,2.)*16.)));
  
  vec2 kik = vec2(4.0*sin(2e2*time)*pow(fract(-time*2.),2.));
  */
  
  //return tan(hh + kik);
  
}

