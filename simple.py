import random
from synthesis import *

class simple_partial(partial):

	def model(self,center,amplitude,note):

		t = self.note.t

		"""
		af = 0.2
		ad = 0.1
		ff = 0.007
		fd = 0.007
		fp = 0
		ap = 0
		"""

		af = 0.01
		ad = 0.005
		ff = 0.0002
		fd = 0.0002
		fp = 0
		ap = 0
		fp = random.random() * np.pi
		ap = random.random() * np.pi

		#sinusoidal amplitude modulation
		am_frequency = af * center
		am_depth = ad * amplitude


		am = am_depth * np.cos(fp+(t * 2 * np.pi * am_frequency))
		am += amplitude

		#sinusoidal frequency modulation
		fm_frequency = ff * center
		fm_depth = fd * center


		fm = fm_depth * np.cos(ap + (t *2 * np.pi * fm_frequency))

		fm += center

		p = np.ones(len(t)) * np.random.random() * np.pi

		"""
		plt.plot(t,p)
		plt.plot(t,fm)
		plt.plot(t,am)
		plt.show()
		"""

		return fm,p,am

class simple_synth(synthesizer):

	def synthesize(self,note):

		centers = note.f * np.array([0.8,1.0,1.5,2.0,3.0,4.0,5.0])
		amplitudes = note.a * np.array([0.2,1.0,0.3,0.3,0.6,0.6,0.1])

		waveform = simple_partial(centers[0],amplitudes[0],note).run()

		for i in range(1,len(centers)):
			wf = simple_partial(centers[i],amplitudes[i],note).run()

			waveform += wf

		return waveform

