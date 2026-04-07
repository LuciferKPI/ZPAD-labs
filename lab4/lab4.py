import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# Початкові параметри
INIT_AMP = 1.0
INIT_FREQ = 0.25
INIT_PHASE = 0.0
INIT_NOISE_MEAN = 0.0
INIT_NOISE_COV = 0.1
INIT_CUTOFF = 5.0

# --- Налаштування часу та частоти дискретизації ---
t = np.linspace(0, 10, 1000)
dt = t[1] - t[0]
fs = 1.0 / dt  # Частота дискретизації

# --- Глобальні стани ---
noise_state = {
    'mean': INIT_NOISE_MEAN,
    'cov': INIT_NOISE_COV,
    'data': np.random.normal(INIT_NOISE_MEAN, np.sqrt(INIT_NOISE_COV), len(t))
}

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance):
    global noise_state
    y_pure = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    
    if noise_mean != noise_state['mean'] or noise_covariance != noise_state['cov']:
        noise_state['mean'] = noise_mean
        noise_state['cov'] = noise_covariance
        noise_state['data'] = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
        
    y_noisy = y_pure + noise_state['data']
    return y_pure, y_noisy

def apply_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs 
    normal_cutoff = cutoff / nyq
    if normal_cutoff >= 1.0: normal_cutoff = 0.99
    elif normal_cutoff <= 0: normal_cutoff = 0.01
        
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y_filtered = filtfilt(b, a, data)
    return y_filtered

# --- Інтерфейс ---
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.08, right=0.7, bottom=0.45, top=0.9) 

y_pure, y_noisy = harmonic_with_noise(t, INIT_AMP, INIT_FREQ, INIT_PHASE, INIT_NOISE_MEAN, INIT_NOISE_COV)
y_filtered = apply_filter(y_noisy, INIT_CUTOFF, fs)

line_noisy, = ax.plot(t, y_noisy, color='orange', label='Noisy Signal', lw=1.5)
line_pure, = ax.plot(t, y_pure, color='blue', linestyle='--', label='Pure Harmonic', lw=2)
line_filtered, = ax.plot(t, y_filtered, color='purple', label='Filtered Signal', lw=2)

ax.set_title('Harmonic Signal Filtering')
ax.set_xlabel('Time (t)')
ax.set_ylabel('Amplitude y(t)')
ax.legend(loc='upper right')

# Прибираємо відступи по боках, щоб графік торкався країв
ax.margins(x=0)
ax.set_xlim(t[0], t[-1])

# --- Інструкція ---
instruction_text = (
    "ІНСТРУКЦІЯ КОРИСТУВАЧА:\n\n"
    "1. Повзунки:\n"
    "   • Amplitude: Амплітуда\n"
    "   • Frequency: Частота\n"
    "   • Phase: Фазовий зсув\n"
    "   • Noise Mean: Зміщення шуму\n"
    "   • Noise Cov: Дисперсія шуму\n"
    "   • Cutoff Freq: Сила фільтра\n\n"
    "2. Прапорець (Чекбокс):\n"
    "    'Show Noise'\n"
    "   Вмикає або вимикає відображення\n"
    "   зашумленого (помаранчевого)\n"
    "   графіка.\n\n"
    "3. Кнопка 'Reset':\n"
    "   Скидає всі параметри до\n"
    "   початкових значень.\n\n"
    "\n"
    "Шум не генерується наново при\n"
    "зміні параметрів самої гармоніки."
)

fig.text(0.72, 0.9, instruction_text, va='top', ha='left', fontsize=10, 
         bbox=dict(boxstyle='round,pad=0.6', facecolor='lightyellow', edgecolor='black', alpha=0.8))

# --- Повзунки ---
ax_amp = plt.axes([0.15, 0.35, 0.5, 0.03])
ax_freq = plt.axes([0.15, 0.30, 0.5, 0.03])
ax_phase = plt.axes([0.15, 0.25, 0.5, 0.03])
ax_noise_mean = plt.axes([0.15, 0.20, 0.5, 0.03])
ax_noise_cov = plt.axes([0.15, 0.15, 0.5, 0.03])
ax_cutoff = plt.axes([0.15, 0.10, 0.5, 0.03])

samp = Slider(ax_amp, 'Amplitude', 0.1, 5.0, valinit=INIT_AMP)
sfreq = Slider(ax_freq, 'Frequency', 0.01, 2.0, valinit=INIT_FREQ)
sphase = Slider(ax_phase, 'Phase', 0.0, 2*np.pi, valinit=INIT_PHASE)
snoise_mean = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=INIT_NOISE_MEAN)
snoise_cov = Slider(ax_noise_cov, 'Noise Cov', 0.0, 1.0, valinit=INIT_NOISE_COV)
scutoff = Slider(ax_cutoff, 'Cutoff Freq', 0.1, 20.0, valinit=INIT_CUTOFF)

# --- Кнопка резет та чекбокс ---
ax_reset = plt.axes([0.15, 0.02, 0.1, 0.05])
btn_reset = Button(ax_reset, 'Reset', hovercolor='0.975')

# --- Чекбокс ---
ax_check = plt.axes([0.3, 0.02, 0.18, 0.05])
check = CheckButtons(ax_check, ['Show Noise'], [True])

# Трохи збільшуємо текст всередині рамки для зручності
for label in check.labels:
    label.set_fontsize(12)

# --- Логіка оновлення ---
def update(val):
    amp = samp.val
    freq = sfreq.val
    phase = sphase.val
    n_mean = snoise_mean.val
    n_cov = snoise_cov.val
    cutoff = scutoff.val
    
    y_p, y_n = harmonic_with_noise(t, amp, freq, phase, n_mean, n_cov)
    y_f = apply_filter(y_n, cutoff, fs)
    
    line_pure.set_ydata(y_p)
    line_noisy.set_ydata(y_n)
    line_filtered.set_ydata(y_f)
    
    # Беремо стан напряму з чекбокса
    line_noisy.set_visible(check.get_status()[0])
    
    ax.relim()
    ax.autoscale_view(scalex=False, scaley=True) 
    fig.canvas.draw_idle()

def reset(event):
    samp.reset()
    sfreq.reset()
    sphase.reset()
    snoise_mean.reset()
    snoise_cov.reset()
    scutoff.reset()
    
    # Якщо галочка знята, повертаємо її
    if not check.get_status()[0]:
        check.set_active(0)

# Підключаємо функції
samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
snoise_mean.on_changed(update)
snoise_cov.on_changed(update)
scutoff.on_changed(update)

# Реагуємо на клік по чекбоксу
check.on_clicked(lambda x: update(None))
btn_reset.on_clicked(reset)

plt.show()