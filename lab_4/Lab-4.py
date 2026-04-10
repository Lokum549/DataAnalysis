import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

t = np.linspace(0, 10, 1000)
fs = 100

base_noise = np.random.randn(len(t))

init_amp = 1.0
init_freq = 0.25
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_cutoff = 5.0

def get_harmonic(amp, freq, phase):
    return amp * np.sin(2 * np.pi * freq * t + phase)

def get_noise(mean, cov):
    return mean + np.sqrt(cov) * base_noise

def apply_filter(data, cutoff):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    normal_cutoff = np.clip(normal_cutoff, 0.01, 0.99)
    b, a = butter(3, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(bottom=0.45, right=0.75) 

pure_harmonic = get_harmonic(init_amp, init_freq, init_phase)
current_noise = get_noise(init_noise_mean, init_noise_cov)
noisy_harmonic = pure_harmonic + current_noise
filtered_harmonic = apply_filter(noisy_harmonic, init_cutoff)

line_noisy, = ax.plot(t, noisy_harmonic, label='Зашумлена гармоніка', color='orange', alpha=0.9)
line_pure, = ax.plot(t, pure_harmonic, label='Чиста гармоніка', color='blue', linestyle='--', linewidth=2)
line_filtered, = ax.plot(t, filtered_harmonic, label='Відфільтрована', color='purple', linewidth=2.5)

ax.set_title("Інтерактивна фільтрація зашумленої гармоніки")
ax.set_xlabel("Час (t)")
ax.set_ylabel("Амплітуда (y)")
ax.legend(loc='upper right')
ax.grid(True, linestyle=':', alpha=0.6)

axcolor = 'lightgoldenrodyellow'
ax_amp = plt.axes([0.15, 0.35, 0.55, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.15, 0.30, 0.55, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.15, 0.25, 0.55, 0.03], facecolor=axcolor)
ax_nmean = plt.axes([0.15, 0.15, 0.55, 0.03], facecolor=axcolor) 
ax_ncov = plt.axes([0.15, 0.10, 0.55, 0.03], facecolor=axcolor)
ax_cutoff = plt.axes([0.15, 0.05, 0.55, 0.03], facecolor=axcolor)
s_amp = Slider(ax_amp, 'Amplitude', 0.1, 5.0, valinit=init_amp)
s_freq = Slider(ax_freq, 'Frequency', 0.01, 2.0, valinit=init_freq)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2*np.pi, valinit=init_phase)
s_nmean = Slider(ax_nmean, 'Noise Mean', -2.0, 2.0, valinit=init_noise_mean)
s_ncov = Slider(ax_ncov, 'Noise Covariance', 0.0, 1.0, valinit=init_noise_cov)
s_cutoff = Slider(ax_cutoff, 'Cutoff Frequency', 0.1, 20.0, valinit=init_cutoff)
checkax = plt.axes([0.78, 0.30, 0.15, 0.08])
check_noise = CheckButtons(checkax, ['Show Noise'], [True])

resetax = plt.axes([0.78, 0.22, 0.15, 0.05])
button_reset = Button(resetax, 'Reset', color='lightblue', hovercolor='0.975')

instructions = (
    "Інструкція:\n"
    "1. Слайдери динамічно змінюють форму сигналу.\n"
    "2. Балансуйте Cutoff для ідеальної фільтрації.\n"
    "3. Шум залишається стабільним (не перераховується)."
)
fig.text(0.78, 0.05, instructions, fontsize=10, va='bottom', ha='left',
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.6'))
def update(val):
    new_pure = get_harmonic(s_amp.val, s_freq.val, s_phase.val)
    new_noise = get_noise(s_nmean.val, s_ncov.val)
    new_noisy = new_pure + new_noise
    new_filtered = apply_filter(new_noisy, s_cutoff.val)
    
    line_pure.set_ydata(new_pure)
    line_noisy.set_ydata(new_noisy)
    line_filtered.set_ydata(new_filtered)
    
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_nmean.on_changed(update)
s_ncov.on_changed(update)
s_cutoff.on_changed(update)

def toggle_noise(label):
    line_noisy.set_visible(check_noise.get_status()[0])
    fig.canvas.draw_idle()

check_noise.on_clicked(toggle_noise)

def reset(event):
    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_nmean.reset()
    s_ncov.reset()
    s_cutoff.reset()

button_reset.on_clicked(reset)

plt.show()