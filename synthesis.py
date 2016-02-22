import random
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt


class note(object):
	"""
	Abstraction for a single note to be synthesized. Songs can be
	represented by a list of note objects.
	"""
	def __init__(self,f, duration, a=1.0, samplerate=44100, **opt):
		
		self.f = float(f) # fundamental frequency, Hz
		self.duration = float(duration) # seconds
		self.a = float(a)
		self.samplerate=float(samplerate) # Hz
		self.opt = opt
		
		# time sampling mesh
		self.t = np.linspace(0,duration,samplerate*duration)
		

class amfm(object):
	"""
	An abstract representation of a simultaneously amplitude,
	frequency, and phase modulated oscillator.
	
	Designed to be subclassed to produce different sounds.
	"""
	
	def __init__(self, center, amplitude, note, shape=np.cos):

		
		self.note = note
		self.shape = shape
		self.center = center
		self.amplitude = amplitude
		
	def run(self):
		"""
		Given a center frequency for the partial in Hz and the
		note the that the partial is associated with, return
		a finished time stream for the sound of the partial.        
		"""

		f,p,a = self.model(self.center, self.amplitude, self.note)
		waveform = self.synthesize(f,p,a)
		waveform = self.process(waveform)

		return waveform
	
	def synthesize(self,frequency,phase,amplitude):
		w = 2*np.pi*frequency
		waveform = amplitude*self.shape(w*self.note.t-phase)

		return waveform
	
	def model(self, center,amplitude, note):
		"""
		Calculate the sampled instantaneous frequency,
		phase shift, and amplitude arrays for the partial
		synthesis stage.
		
		Effects that require information about other notes
		near in time can be implemented by storing references
		to the requisite notes in the note's opt member.
		"""
		pass
	
	def process(self,waveform):
		"""
		Any and all post synthesis signal processing goes here.
		"""
		return waveform

class shaped_noise(object):

	def __init__(self, centers, amplitude, note):

		n = int(note.duration * note.samplerate)

		transfer_function = np.zeros(n)

		s = np.min(np.diff(np.sort(centers))) / 2.0

		fr = np.fft.fftfreq(n)

		self.response = np.copy(fr)

		for c in centers:
			self.response  += np.exp( (0.5/s**2)*(abs(fr)-c)**2 )

		self.noise = np.random.normal(loc=0,scale=amplitude,size=(n,))

	def run(self):

		return np.real(np.fft.ifft(self.noise*self.response))

class synthesizer(object):

	def run(self,notes):
		"""
		Take a list of notes and generate a sound waveform as 
		a numpy array of time samples
		"""
		waveform = np.array([0])

		for n in notes:
			waveform = np.concatenate((waveform,
				self.synthesize(n)))

		return self.process(waveform,notes)

	def synthesize(self,note):
		"""
		generate a time stream from a set of contributions
		from partials.
		"""
		pass

	def process(self,waveform,notes):
		"""
		post synthesis signal processing goes here
		"""
		return waveform
		


def inspect(signal, samplerate=44100, windowtime=30, overlap=0.5):
	
	#windowtime milliseconds
	#overlap fraction
	
	dt = 1.0/samplerate    
	t = np.linspace(0, len(signal)*dt, len(signal))
	
	NFFT = int((30 * 1e-3)/dt)
	Fs = int(samplerate)
	noverlap = int(overlap * NFFT)
	
	ax1 = plt.subplot(211)
	plt.plot(t, signal)
	plt.subplot(212, sharex=ax1)
	Pxx, freqs, bins, im = plt.specgram(signal, NFFT=NFFT,
										Fs=Fs,
										noverlap=900,
										cmap=plt.cm.gist_heat)
	plt.show()