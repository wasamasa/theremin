SinOsc sin => dac;
0.5 => dac.gain;
440.0 => float oldFreq;
440.0 => float newFreq;
440.0 => sin.freq;

SinOsc lfo => blackhole;
5 => lfo.freq;

OscIn oscpitch;
6666 => oscpitch.port;
"/pitch" => oscpitch.addAddress;

OscIn oscvol;
6666 => oscvol.port;
"/volume" => oscvol.addAddress;

fun float fmin(float a, float b) {
    return (a < b) ? a : b;
}

fun void interpolate() {
    1.5 => float step;
    while (true) {
        fmin(oldFreq, newFreq) + Math.fabs(oldFreq - newFreq) /
            step => oldFreq;

        oldFreq => sin.freq;
        5::ms => now;
    }
}

fun void wobble() {
    while (true) {
        lfo.last() * 0.01 * oldFreq +=> oldFreq;
        10::ms => now;
    }
}

fun void adjustVolume() {
    while (true) {
        oscvol => now;
        while (oscvol.recv(OscMsg msg)) {
            Std.fabs(msg.getFloat(0)) => dac.gain;
        }
    }
}

spork ~ interpolate();
spork ~ wobble();
spork ~ adjustVolume();

while (true) {
    oscpitch => now;
    while (oscpitch.recv(OscMsg msg)) {
        Std.fabs(msg.getFloat(0)) => float pitch;
        Math.pow(2, pitch * 2 + 8) => newFreq;
    }
}
