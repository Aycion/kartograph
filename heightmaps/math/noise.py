"""This module governs generating noise for a 2D array which can be
converted to an image, heightmap, or similar application.

Info sources:
    `Definitions <http://libnoise.sourceforge.net/glossary/>`_

"""

import numpy as np
from opensimplex import OpenSimplex
from noise import perlin
import logging


class Condenser:

    def __init__(self, engine='opensim', wavefn=None):
        self.wavefn = wavefn or WaveFunction()
        if not isinstance(self.wavefn, WaveFunction):
            raise TypeError(
                'The wave function provided must be an instance '
                'of WaveFunction or a descendant.'
            )
        self.cum_amp = 0

        if engine == 'opensim':
            self.engine = OpenSimplex().noise2d
        elif engine == 'perlin':
            self.engine = perlin.SimplexNoise().noise2
        else:
            raise ValueError('Invalid argument for noise engine')

    def configure_wavefn(self, freq=None, amp=None, lacu=None, gain=None):
        self.wavefn.frequency = freq or self.wavefn.frequency
        self.wavefn.amplitude = amp or self.wavefn.amplitude
        self.wavefn.lacunarity = lacu or self.wavefn.lacunarity
        self.wavefn.gain = gain or self.wavefn.gain

    def map_noise_layer(self, dims=None, imarray=None, octave=0):
        """

        :param tuple dims:
        :param np.ndarray imarray:
        :param int octave:
        :return:
        :rtype:
        """
        imarray = imarray if imarray is not None else np.empty(dims[0:2], dtype=np.float64)
        rows, cols = imarray.shape
        octave_wave = self.wavefn.shift_octave(octave)
        """Shift the base wave function by the number given in 
        octave, according to the attributes of the base. 
        For example, shifting a wave with frequency=1 and 
        lacunarity=2 by two octaves returns a wave with equal 
        lacunarity and frequency=1*(2^2)=4. The same relationship
        exists between amplitude and gain.
        
                
        """
        print(f'Wave properties:\n'
              f'    Octave: {octave}\n'
              f'    Amplitude: {octave_wave.amplitude}\n'
              f'    Frequency: {octave_wave.frequency}\n')
        for r in range(rows):
            for c in range(cols):
                imarray[r, c] = self.point_noise(r, c, wave=octave_wave)
        self.cum_amp += octave_wave.amplitude
        return imarray

    def point_noise(self, x, y, wave=None):
        """

        :param int x: The target x-index.
        :param int y: The target y-index.
        :param WaveFunction wave:

        :return np.uint8: The noise value for (x, y)

        """
        wave = wave or self.wavefn

        freq = wave.frequency
        amp = wave.amplitude

        sx, sy = x * freq, y * freq
        """Scale the inputs by the frequency"""
        height = self.engine(sx, sy) * amp
        """Scale the outputs by the amplitude"""

        return height


class WaveFunction:

    def __init__(self, amplitude=1.0, frequency=0.01,
                 gain=0.5, lacunarity=2.0):

        self.amplitude = amplitude
        self.frequency = frequency
        self.gain = gain
        self.lacunarity = lacunarity

    def __setattr__(self, key, value):
        if isinstance(value, (float, int, np.float64)):
            super().__setattr__(key, value)
        else:
            logging.warning(f'Tried to assign attribute illegal value: {value}')

    def shift_octave(self, offset):
        """Shift this wave function by the given ``offset``,
        according to the current function's base attributes.

        For any offset, the new wave has the same gain and
            lacunarity as the current. The new wave's amplitude
            and frequency are equal to a multiple of their base values.
            Frequency is multiplied by lacunarity once for each offset,
            and the same relationship applies to amplitude and gain.

        Simplifying for any offset:
            ``frequency = frequency * (lacunarity ^ offset)``

            ``amplitude = amplitude * (gain ^ offset)``

        For example, shifting a wave with frequency=1 and
            lacunarity=2 by two octaves returns a wave with equal
            lacunarity and frequency=1*(2^2)=4. The same relationship
            exists between amplitude and gain.


        :param int offset: The number of octaves to move up or down from
            the current WaveFunction

        :return: The new WaveFunction according to offset
        :rtype: WaveFunction
        """
        if offset == 0:
            return self

        return WaveFunction(
            amplitude=(self.amplitude * (self.gain ** offset)),
            frequency=(self.frequency * (self.lacunarity ** offset)),
            gain=self.gain, lacunarity=self.lacunarity
        )

    def __repr__(self):
        return (
            'Wave Function with '
            f'(Amplitude={self.amplitude}; '
            f'Gain={self.gain}; '
            f'Frequency={self.frequency}; '
            f'Lacunarity={self.lacunarity})'
        )
