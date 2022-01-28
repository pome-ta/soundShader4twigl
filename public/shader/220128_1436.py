// http://countercomplex.blogspot.jp/2011/10/algorithmic-symphonies-from-one-line-of.html
// http://wurstcaptures.untergrund.net/music/

vec2 mainSound(float time )
{
    int t = int(time * 8000.0);
    // https://www.youtube.com/watch?v=GtQdIYUtAHg
    t = t*(((t>>12)|(t>>8))&(63&(t>>4)));
    //t = t*(t>>11&t>>8&123&t>>3);
    //t = t*(t>>8*(t>>15|t>>8)&(20|(t>>19)*5>>t|t>>3));
    // https://www.youtube.com/watch?v=qlrs2Vorw2Y
    //t = (t>>6|t|t>>(t>>16))*10+((t>>11)&7);
    //t = (t|(t>>9|t>>7))*t&(t>>11|t>>9);
    //t = t*5&(t>>7)|t*3&(t*4>>10);
    //t = (t>>7|t|t>>6)*10+4*(t&t>>13|t>>6);
    // https://www.youtube.com/watch?v=tCRPUv8V22o
    //t = (t*5&t>>7)|(t*3&t>>10);
    //t = ((t/2*(15&(0x234568a0>>(t>>8&28))))|t/2>>(t>>11)^t>>12)+(t/16&t&24);
    //t = (t&t/255)-(t*3&t>>13&t>>6);
    //t = (t*9&t>>4|t*5&t>>7|t*3&t/1024)-1;

    return vec2(float(t & 0xff - 128) / 128.);
} 

